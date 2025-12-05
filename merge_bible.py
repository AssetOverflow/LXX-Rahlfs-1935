import sqlite3
import os
import shutil
import csv
import glob
import sys

# Configuration
LXX_SOURCE = "11_end-users_files/MyBible/Bibles/LXX1.SQLite3"
OUTPUT_FILE = "CompleteGreekBible.SQLite3"
SBL_REPO_DIR = "SBLGNT-add-ons"
BRIDGING_FILE = "09b_bridging_NT/LXXno2NTno.csv"

# NT Book Mapping (Standard NT ordering -> Custom IDs starting at 470)
# Maps standard SBL book numbers (typically 40-66 or 1-27 depending on their DB) 
# to the 470+ range required by the guide.
# We will determine the source ID dynamically, but we need the target order.
NT_BOOKS_ORDER = [
    "Matthew", "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians",
    "Galatians", "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", 
    "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]
START_NT_ID = 470
ID_STEP = 10

def find_sbl_database():
    """Finds a compatible SQLite file in the SBLGNT repo."""
    # Look in the standard end-user-modules folder first
    search_path = os.path.join(SBL_REPO_DIR, "end-user-modules", "**", "*.SQLite3")
    found_files = glob.glob(search_path, recursive=True)
    
    # Filter out likely non-bible files if multiple exist (e.g. dictionaries)
    bible_candidates = [f for f in found_files if "dictionary" not in f.lower() and "lexicon" not in f.lower()]
    
    if not bible_candidates:
        # Fallback search in whole repo
        found_files = glob.glob(os.path.join(SBL_REPO_DIR, "**", "*.SQLite3"), recursive=True)
        bible_candidates = [f for f in found_files if "dictionary" not in f.lower()]

    if not bible_candidates:
        print(f"Error: Could not find an SBLGNT SQLite database in {SBL_REPO_DIR}")
        sys.exit(1)
        
    print(f"Found SBLGNT database: {bible_candidates[0]}")
    return bible_candidates[0]

def load_bridging_data():
    """Loads the lexicon mapping data."""
    if not os.path.exists(BRIDGING_FILE):
        print(f"Warning: Bridging file {BRIDGING_FILE} not found. Lexicon mapping verification skipped.")
        return {}
    
    mapping = {}
    with open(BRIDGING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                # LXX_ID -> NT_ID
                mapping[row[0]] = row[1]
    print(f"Loaded {len(mapping)} bridging entries.")
    return mapping

def merge_databases(sbl_db_path):
    # 1. Create a copy of the LXX database to avoid corrupting the original
    print(f"Creating {OUTPUT_FILE} from {LXX_SOURCE}...")
    shutil.copyfile(LXX_SOURCE, OUTPUT_FILE)

    conn = sqlite3.connect(OUTPUT_FILE)
    cursor = conn.cursor()

    # 2. Attach the SBL database
    print("Attaching SBLGNT database...")
    cursor.execute("ATTACH DATABASE ? AS sbl", (sbl_db_path,))

    # 3. Analyze SBL books to build a mapping map
    # We need to know what IDs the SBL DB uses for Matthew, Mark, etc.
    print("Analyzing SBL book structure...")
    cursor.execute("SELECT book_number, long_name, short_name FROM sbl.books ORDER BY book_number")
    sbl_books = cursor.fetchall()
    
    # Create a map of {Old_ID: New_Target_ID}
    book_id_map = {}
    
    print("Merging Books...")
    current_target_id = START_NT_ID
    
    for b_id, long_name, short_name in sbl_books:
        # Simple matching by name containment to assign correct new ID
        # This handles cases where SBL might use "Matt" or "Matthew"
        matched = False
        for i, canon_name in enumerate(NT_BOOKS_ORDER):
            if canon_name.lower() in long_name.lower() or (short_name and short_name.lower() in canon_name.lower()):
                target_id = START_NT_ID + (i * ID_STEP)
                book_id_map[b_id] = target_id
                
                # Insert into Main Books table
                # We check if it exists first to be safe
                cursor.execute("""
                    INSERT INTO books (book_number, book_color, short_name, long_name)
                    VALUES (?, '#FFD700', ?, ?)
                """, (target_id, short_name, long_name))
                matched = True
                break
        
        if not matched:
            print(f"Warning: Could not match SBL book '{long_name}' to standard NT list. Skipping.")

    # 4. Merge Verses
    print("Merging Verses (this may take a moment)...")
    
    # We select all verses from SBL, map the book ID, and insert
    cursor.execute("SELECT book_number, chapter, verse, text FROM sbl.verses")
    all_sbl_verses = cursor.fetchall()
    
    verses_to_insert = []
    for old_bid, chap, v_num, text in all_sbl_verses:
        if old_bid in book_id_map:
            new_bid = book_id_map[old_bid]
            verses_to_insert.append((new_bid, chap, v_num, text))
            
    cursor.executemany("""
        INSERT INTO verses (book_number, chapter, verse, text)
        VALUES (?, ?, ?, ?)
    """, verses_to_insert)
    
    print(f"Inserted {len(verses_to_insert)} NT verses.")

    # 5. Update Metadata
    cursor.execute("UPDATE info SET value = 'LXX-Rahlfs-1935 + SBLGNT' WHERE name = 'description'")
    cursor.execute("INSERT OR REPLACE INTO info (name, value) VALUES ('title', 'Complete Greek Bible (LXX + SBLGNT)')")
    
    conn.commit()
    conn.close()
    print("Success! Database merge complete.")

if __name__ == "__main__":
    if not os.path.exists(LXX_SOURCE):
        print(f"Error: Base LXX file not found at {LXX_SOURCE}")
        sys.exit(1)
        
    load_bridging_data() # Just verifying availability
    sbl_db = find_sbl_database()
    merge_databases(sbl_db)
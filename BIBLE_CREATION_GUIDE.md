# Bible Creation Guide

This guide explains how to create Bible modules from the LXX-Rahlfs-1935 repository data. You can create either a Septuagint-only Bible (Old Testament and Apocrypha) or a complete Bible including the New Testament.

## Table of Contents
- [Understanding the Repository](#understanding-the-repository)
- [Option 1: Creating a Septuagint-Only Bible](#option-1-creating-a-septuagint-only-bible)
- [Option 2: Creating a Bible with New Testament](#option-2-creating-a-bible-with-new-testament)
- [Available Output Formats](#available-output-formats)
- [Working with the Source Data](#working-with-the-source-data)

---

## Understanding the Repository

This repository contains the complete Septuagint (LXX) text based on Rahlfs' 1935 edition, with extensive linguistic annotations including:

- **Text in multiple formats**: Accented Greek, unaccented Greek, and Koine Greek
- **Morphological analysis**: Part of speech, parsing codes for every word
- **Strong's numbers**: Cross-referenced with Strong's concordance
- **Lexical data**: Lemmas and lexeme numbers
- **English glosses**: Basic translations for each word
- **Pronunciation data**: Modern Greek pronunciation
- **Transliteration**: SBL-style transliteration

### What is Included

The Septuagint contains:
- **Pentateuch** (Torah): Genesis through Deuteronomy
- **Historical Books**: Joshua through 2 Chronicles
- **Wisdom Literature**: Job, Psalms, Proverbs, Ecclesiastes, Song of Solomon
- **Prophets**: Isaiah, Jeremiah, Ezekiel, and the twelve Minor Prophets
- **Deuterocanonical/Apocryphal Books**: 1-4 Maccabees, Wisdom of Solomon, Sirach, Tobit, Judith, Baruch, additions to Esther and Daniel, and more

### What is NOT Included

The Septuagint does **NOT** include the New Testament (Matthew, Mark, Luke, John, Acts, Paul's Epistles, General Epistles, Revelation). To create a complete Bible, you need to obtain New Testament data separately (see Option 2 below).

---

## Option 1: Creating a Septuagint-Only Bible

The easiest way to use this data is with the pre-built files. No compilation is needed!

### Quick Start - Pre-Built Formats

#### MyBible Format (Android/Desktop)

**Main Septuagint (54 books):**
- Database: `11_end-users_files/MyBible/Bibles/LXX1.SQLite3`
- Book list: `11_end-users_files/MyBible/Bibles/books_main.csv`
- Source CSV: `11_end-users_files/MyBible/Bibles/LXX_final_main.csv`

This includes:
- All standard Septuagint books (B text versions where available)
- Full morphology and Strong's numbers
- Ready to use in MyBible app

**Alternate Readings (6 books):**
- Database: `11_end-users_files/MyBible/Bibles/LXX2.SQLite3`
- Book list: `11_end-users_files/MyBible/Bibles/books_alternate.csv`
- Source CSV: `11_end-users_files/MyBible/Bibles/LXX_final_alternate.csv`

This includes alternate textual traditions:
- Joshua A, Judges A (A text versions)
- Tobit S (Sinaiticus version)
- Daniel Th, Susanna Th, Bel Th (Theodotion versions)

**Installation:**
1. Copy the `.SQLite3` file(s) to your MyBible Bible directory
2. Open MyBible and the Bible module will be available

#### Marvel.Bible Format

Pre-formatted files in `12-Marvel.Bible/`:
- `01-text_accented.csv.zip` - Main Greek text
- `06-gloss.csv` - English glosses
- `09-lexemes.csv` - Lexical data
- `00-versification_original.csv` - Versification mappings

These files are ready to import into the Marvel.Bible platform at https://marvel.bible

#### CSV Format

Raw CSV files for custom processing:
- `11_end-users_files/MyBible/Bibles/LXX_final_main.csv` - Main Bible in CSV
- `11_end-users_files/MyBible/Bibles/LXX_final_alternate.csv` - Alternate readings

### Using the Lexicon

A complete analytical lexicon is available in:
- MyBible format: `11_end-users_files/MyBible/Lexicon/HebGrk.dictionary.SQLite3`
- MyBible CSV format: `11_end-users_files/MyBible/Lexicon/Lexicon_MyBilbe.csv` *(note: filename has typo "MyBilbe")*
- UniqueBibleApp format: `11_end-users_files/LXX_lexicon_formatted_for_UniqueBibleAppPlus.csv`
- Raw format: `09a_LXX_lexicon/` directory

---

## Option 2: Creating a Bible with New Testament

To create a complete Bible with both Old Testament (Septuagint) and New Testament, you need to combine this repository's data with Greek New Testament data.

### Required External Resources

**1. Greek New Testament Text (SBLGNT)**

The New Testament is not included in this repository. You need to obtain it from:
- **SBLGNT (SBL Greek New Testament)**: Available at https://github.com/eliranwong/SBLGNT-add-ons
- Alternative: Other Greek NT sources with compatible morphology data

**License Note:** The SBLGNT is freely available for non-commercial use but has separate licensing terms.

### Bridging Data

This repository includes bridging data to connect LXX and NT lexemes:
- File: `09b_bridging_NT/LXXno2NTno.csv`
- Purpose: Maps lexeme numbers between Septuagint and New Testament
- Based on: David Troidl's gntLookups.js from OpenScriptures

Format: `LXX_lexeme_number,NT_lexeme_number`

### Step-by-Step Process

**Step 1: Obtain New Testament Data**

Clone or download the SBLGNT data:
```bash
git clone https://github.com/eliranwong/SBLGNT-add-ons.git
```

This provides:
- Greek NT text with morphology
- Lexical information
- Strong's numbers
- Compatible formatting with LXX data

**Step 2: Understand the Data Structure**

Both LXX and SBLGNT use similar data structures:
- Word-by-word Greek text
- Morphological codes (part of speech, parsing)
- Lexeme numbers for dictionary lookups
- Strong's numbers for concordance

**Step 3: Combine the Texts**

You have several approaches:

**A. MyBible SQLite Database Method**

1. Start with `LXX1.SQLite3` as your base
2. Add New Testament books to the `books` table:
   - Book numbers 40-66 (or 470-730 to avoid conflicts)
   - Matthew=40, Mark=41, Luke=42, John=43, Acts=44, Romans=45, etc.
3. Import NT verses into the `verses` table with format:
   ```
   book_number | chapter | verse | text
   ```
4. Maintain Strong's number and morphology tags using `<S>` and `<m>` markers

**B. CSV Merge Method**

1. Use `LXX_final_main.csv` as starting point
2. Append SBLGNT verses in the same format
3. Ensure book numbering doesn't conflict
4. Convert to SQLite or your target format

**C. Custom Processing**

Use the bridging data to:
1. Create unified lexicon entries
2. Map lexeme numbers between OT and NT
3. Build cross-references
4. Generate search indexes

**Step 4: Handle Book Numbering**

Standard book numbering schemes:
- **LXX Books**: 10-800 (e.g., Gen=10, Exodus=20, etc.)
- **NT Books**: Suggest 470-730 or standard 40-66
  - Matthew=470 (or 40)
  - Mark=480 (or 41)
  - Luke=490 (or 42)
  - John=500 (or 43)
  - Continue through Revelation=730 (or 66)

**Step 5: Update Metadata**

In the SQLite `info` table, update:
- `description`: Change to "LXX-Rahlfs-1935 + SBLGNT"
- `chapter_string_nt`: Ensure "Chapter" is set
- Verify `strong_numbers=true` for both testaments

### Example: Creating MyBible Complete Bible

```sql
-- Step 1: Copy LXX1.SQLite3 to a new file
-- cp LXX1.SQLite3 CompleteGreekBible.SQLite3

-- Step 2: Add NT books to books table
INSERT INTO books (book_number, book_color, short_name, long_name) VALUES
(470, '#FFD700', 'Matt', 'Matthew'),
(480, '#FFD700', 'Mark', 'Mark'),
(490, '#FFD700', 'Luke', 'Luke'),
(500, '#FFD700', 'John', 'John'),
(510, '#87CEEB', 'Acts', 'Acts'),
(520, '#98FB98', 'Rom', 'Romans'),
-- ... continue for all NT books
(730, '#DDA0DD', 'Rev', 'Revelation');

-- Step 3: Import NT verses (from processed SBLGNT data)
-- Format: book_number, chapter, verse, text
-- Text should include Strong's numbers as <S>NNNN</S>
-- and morphology as <m>code</m>

-- Step 4: Update info
UPDATE info SET description = 'LXX-Rahlfs-1935 + SBLGNT' WHERE name = 'description';
```

### Resources and Scripts

Processing scripts in `script/` directory may be helpful:
- `addLexNo_NT.sh` - Adds NT lexeme numbers
- `LXXno2NTno.sh` - Works with bridging data
- `book_maps_MyBible.sh` - Book name mappings

However, these are designed for the original LXX processing and will need adaptation for NT integration.

---

## Available Output Formats

### 1. MyBible Format (.SQLite3)

**Best for:**
- MyBible Android app
- MyBible Desktop (Windows)
- Applications that can read SQLite databases

**Structure:**
- `books` table: Book metadata
- `verses` table: Verse text with embedded markup
- `info` table: Module metadata
- `stories` table: Optional narrative units

**Strong's Format:** `<S>number</S>` tags around Greek words
**Morphology Format:** `<m>code</m>` tags with parsing information

### 2. CSV Format

**Best for:**
- Custom processing
- Spreadsheet analysis
- Import into other systems
- Academic research

**Files Available:**
- Main Bible text: Accented, unaccented, Koine variations
- Morphology data: Detailed parsing for each word
- Lexical data: Lemmas and dictionary forms
- English glosses: Word-by-word translations

### 3. Marvel.Bible Format

**Best for:**
- Online Bible study platform
- Web-based applications
- Cross-platform access

**Files in `12-Marvel.Bible/`:**
- Compressed text archives
- Gloss mappings
- Lexeme databases
- Versification schemes

### 4. e-Sword Format

**Status:** Work in progress
**Directory:** `11_end-users_files/e-Sword/`

This format support is under development.

---

## Working with the Source Data

If you need to process the raw data or create custom formats:

### Core Text Files

**Primary Text (`01_wordlist_unicode/`):**
- `text_accented.csv` - Full Greek text with accents (recommended)
- `text_unaccented.csv` - Greek text without accents
- `text_koine.csv` - Uses Koine Greek font
- `KoineGreek.ttf` - Font file for Koine text

Format: `line_number, word_position, greek_word`

### Morphology Data

**Directories:**
- `03a_morphology_with_JTauber_patches/` - Morphological analysis with corrections
- `03b_descriptions_on_morphology_codes/` - Human-readable morphology descriptions

Morphology codes follow standard Greek parsing conventions:
- Part of speech (noun, verb, adjective, etc.)
- Case, number, gender (for nominals)
- Tense, voice, mood, person, number (for verbs)

### Lexical Data (`02_lexemes/`)

- `Lex_LXXno.csv` - Lexeme numbers for LXX words
- `Lex_NTno.csv` - NT lexeme numbers for bridging
- `OSSP_lexemes.csv` - Open Scriptures Septuagint Project lexemes
- `OSSP_keys.csv` - Keys for OSSP integration

### Additional Datasets

- `04_SBL_transliteration/` - Transliterated text (Greek to Latin alphabet)
- `05_pronunciation/` - Modern Greek pronunciation
- `06_English_gloss/` - English word meanings
- `07_StrongNumber/` - Strong's concordance numbers
- `08_versification/` - Verse reference mappings
- `09a_LXX_lexicon/` - Complete analytical lexicon
- `09b_bridging_NT/` - NT bridging data
- `10_clause_annotation/` - Clause-level annotations

### Processing Scripts (`script/`)

Shell scripts for data transformation:
- `betacode2unicode_accented.sh` - Converts beta code to Unicode
- `addStrGreek.sh` - Adds Strong's numbers
- `addEngGloss_v4.sh` - Adds English glosses
- `unicode2transliteration_SBL.sh` - Creates transliterations
- `book_maps_MyBible.sh` - Book name mappings

**Note:** These scripts are specialized for the original LXX processing pipeline and may require modification for other uses.

---

## Licensing and Attribution

### LXX-Rahlfs-1935 License

This repository is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

**Attribution:**
- Copyright 2017 Eliran Wong
- Based on CCAT morphologically analyzed Septuagint
- Includes data from Open Scriptures Septuagint Project

### CCAT User Declaration Required

The original CCAT data requires users to submit a user declaration. Even though this repository contains derivative works, please respect the original source:

Download and submit the declaration from:
http://ccat.sas.upenn.edu/gopher/text/religion/biblical/lxxmorph/0-user-declaration.txt

### Adding New Testament Data

If you create a Bible with New Testament:
- SBLGNT has its own license (see https://github.com/eliranwong/SBLGNT-add-ons)
- You must comply with both LXX and NT data licenses
- Typically: Free for non-commercial use, attribution required

### Acknowledgments

This project builds on work from:
- **CCAT**: Robert Kraft and team (original morphologically analyzed LXX)
- **TLG**: Thesaurus Linguae Graecae (base Greek texts)
- **UBS**: United Bible Societies (permissions)
- **James Tauber**: Morphology corrections
- **David Troidl**: Open Scriptures Septuagint Project data
- **Jonathan Robie**: Licensing guidance

---

## Support and Resources

### Questions or Issues?

- GitHub Issues: https://github.com/eliranwong/LXX-Rahlfs-1935/issues
- Original repository documentation in each subdirectory's README.md

### Related Projects

- **SBLGNT Add-ons**: https://github.com/eliranwong/SBLGNT-add-ons
- **Open Scriptures Greek Resources**: https://github.com/openscriptures/GreekResources
- **Unique Bible App**: https://www.uniquebible.app/
- **Marvel.Bible**: https://marvel.bible
- **Bible Bento**: https://biblebento.com/

### Mobile Apps

Pre-built mobile applications with this data:
- **iOS/Android**: Available on App Store and Google Play
- User Manual: https://www.uniquebible.app/mobile
- Downloads: https://www.uniquebible.app/download

---

## Quick Reference

### File Locations Summary

| What You Want | Where to Find It |
|---------------|------------------|
| **Ready-to-use MyBible Septuagint** | `11_end-users_files/MyBible/Bibles/LXX1.SQLite3` |
| **Alternate readings** | `11_end-users_files/MyBible/Bibles/LXX2.SQLite3` |
| **CSV format (main Bible)** | `11_end-users_files/MyBible/Bibles/LXX_final_main.csv` |
| **Marvel.Bible files** | `12-Marvel.Bible/` directory |
| **Greek text with accents** | `01_wordlist_unicode/text_accented.csv` |
| **Morphology data** | `03a_morphology_with_JTauber_patches/` |
| **English glosses** | `06_English_gloss/` |
| **Strong's numbers** | `07_StrongNumber/` |
| **LXX Lexicon** | `09a_LXX_lexicon/` |
| **NT bridging data** | `09b_bridging_NT/LXXno2NTno.csv` |
| **Book listings** | `11_end-users_files/MyBible/Bibles/books_*.csv` |

### Book Count

- **Main Septuagint (LXX1)**: 54 books
- **Alternate readings (LXX2)**: 6 books
- **Total Septuagint**: 60 book versions available
- **New Testament** (if added separately): 27 books
- **Complete Bible**: Would be 81-87 books depending on configuration

### Word Count

- Total Greek words in Septuagint: **623,693 words**
- With full morphological analysis on every word

---

## Summary

**For a Septuagint-only Bible:**
1. Use the pre-built files in `11_end-users_files/MyBible/Bibles/`
2. Copy `LXX1.SQLite3` (and optionally `LXX2.SQLite3`) to your Bible app
3. Done! No compilation needed.

**For a complete Bible with New Testament:**
1. Start with the Septuagint files from this repository
2. Obtain SBLGNT data from https://github.com/eliranwong/SBLGNT-add-ons
3. Use bridging data in `09b_bridging_NT/` to connect lexemes
4. Merge texts using book numbering 10-800 (OT) and 470-730 (NT)
5. Combine into your chosen output format

Both options give you a complete Greek Bible with full morphological analysis and Strong's numbers!

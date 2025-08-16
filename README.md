# Forum Webscraper (XenForo)

Tools for extracting posts from XenForo forums and splitting long documents by word count.

## Features
- Scrape all posts by a chosen author from a XenForo thread
- Save clean text with optional threadmark headers
- Split `.txt` or `.docx` into evenly sized chunks

## Quick start
```bash
pip install -r requirements.txt

# Extract posts
python src/forum_extractor.py --url "https://forums.sufficientvelocity.com/threads/xxxxx" --author "Quest" --output posts.txt

# Split into 5k-word chunks
python src/docx_splitter.py --input posts.txt --words 5000 --outdir chunks


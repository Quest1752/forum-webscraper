#!/usr/bin/env python3
import argparse, os, math
from pathlib import Path

def read_text(path: Path) -> str:
    p = Path(path)
    if p.suffix.lower() == ".docx":
        try:
            from docx import Document  # python-docx
        except ImportError:
            raise SystemExit("Install python-docx to read .docx files")
        doc = Document(p)
        return "\n".join([para.text for para in doc.paragraphs])
    return p.read_text(encoding="utf-8")

def split_by_words(text: str, words_per_file: int):
    words = text.split()
    total = len(words)
    for i in range(0, total, words_per_file):
        yield " ".join(words[i:i+words_per_file])

def main():
    ap = argparse.ArgumentParser(description="Split a text/.docx file into word-limited chunks.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--words", type=int, default=5000)
    ap.add_argument("--outdir", default="chunks")
    args = ap.parse_args()

    text = read_text(args.input)
    os.makedirs(args.outdir, exist_ok=True)
    total_chunks = math.ceil(len(text.split()) / args.words)

    for idx, chunk in enumerate(split_by_words(text, args.words), 1):
        out = Path(args.outdir) / f"chunk_{idx:03d}.txt"
        out.write_text(chunk, encoding="utf-8")
        print(f"Wrote {out} ({idx}/{total_chunks})")

if __name__ == "__main__":
    main()

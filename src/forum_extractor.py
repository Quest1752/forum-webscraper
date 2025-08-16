#!/usr/bin/env python3
import argparse, logging, time
from typing import Optional
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (XenForo scraper for personal use)"}

def fetch(url: str, *, retries: int = 3, timeout: int = 20) -> Optional[str]:
    for i in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            r.raise_for_status()
            return r.text
        except Exception as e:
            logging.warning(f"GET {url} failed ({e}), retry {i+1}/{retries}")
            time.sleep(1 + i)
    return None

def get_total_pages(thread_url: str) -> int:
    html = fetch(thread_url)
    if not html:
        return 1
    doc = BeautifulSoup(html, "lxml")
    # XenForo simple pager: "1 of N"
    tag = doc.find("a", class_="pageNavSimple-el pageNavSimple-el--current")
    if tag and tag.text.strip().split()[-1].isdigit():
        return int(tag.text.strip().split()[-1])
    # Fallback: numbered pager
    nums = [int(a.text) for a in doc.select("li.pageNav-page a") if a.text.isdigit()]
    return max(nums) if nums else 1

def scrape(thread_url: str, author: str, out_file: str):
    pages = get_total_pages(thread_url)
    logging.info(f"Detected {pages} pages")

    with open(out_file, "w", encoding="utf-8") as f:
        for p in range(1, pages + 1):
            url = f"{thread_url.rstrip('/')}/page-{p}"
            html = fetch(url)
            if not html:
                logging.warning(f"Skipping page {p}; fetch failed.")
                continue
            doc = BeautifulSoup(html, "html.parser")
            posts = doc.find_all("article", attrs={"data-author": author})
            logging.info(f"Page {p}: found {len(posts)} posts by {author}")
            for post in posts:
                header = post.find("div", class_="message-cell message-cell--threadmark-header")
                if header:
                    title = header.find("span", attrs={"data-xf-init": "tooltip"})
                    if title:
                        f.write("\n" + "_"*40 + f"\n\n{title.text.strip()}\n" + "_"*40 + "\n")
                for div in post.find_all("div", class_="bbWrapper"):
                    text = div.get_text(separator="\n").strip()
                    if text:
                        f.write(text + "\n")

def main():
    ap = argparse.ArgumentParser(description="Scrape XenForo thread posts by author.")
    ap.add_argument("--url", required=True, help="Thread URL (first page)")
    ap.add_argument("--author", required=True, help="Author to extract")
    ap.add_argument("--output", default="output.txt", help="Output text file")
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    scrape(args.url, args.author, args.output)

if __name__ == "__main__":
    main()

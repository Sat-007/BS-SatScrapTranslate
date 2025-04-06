
from scripts.website_scrapper import search_automation
from scripts.translator import run_scrapper
from scripts.header_word_count import analyze_word_frequency
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))


def main():
    articles = search_automation()
    translate_text = run_scrapper(articles)
    freq_words = analyze_word_frequency(translate_text)
    print(freq_words)

if __name__ == "__main__":
    main()  
from typing import List, Dict
from googletrans import Translator

def run_scrapper(scraped_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    translator = Translator()

    for article in scraped_data:
        original_title = article['title']
        try:
            translated = translator.translate(original_title, src='es', dest='en')
            article['translated_title'] = translated.text = translated.text
        except Exception as e:
            article['translated_title'] = "Translation Failed"
    
    return scraped_data
        

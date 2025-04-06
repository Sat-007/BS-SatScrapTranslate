
def analyze_word_frequency(data):
    #articles = search_automation()
    #data = run_scrapper(articles)
    word_dict = {}
    
    for article in data:
        title = article['translated_title']
        
        #print(title)
        title_clean = title.replace(".", "").replace(",", "").replace("?", "").replace("!", "").lower()
        words = title_clean.split()

        for word in words:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

    #print(word_dict)
    repeated_words = {}
    for word, count in word_dict.items():
        if count >= 2:
            repeated_words[word] = count

    if repeated_words:
        return repeated_words
    else:
        return "No Repeated words"

bad_words = ["fuck", "asshole", "bitch", "SOB", "sucker", "cunt", "pussy", "slut", "junky", "nuts"]

def filter_bad_words(text):
    for word in bad_words:
        text = text.replace(word, '***')
    return text
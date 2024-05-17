bad_words = ["fuck", "asshole", "bitch", "SOB", "sucker", "cunt", "pussy", "slut", "junky", "nuts", "操你妈", "婊子养的", "法克"]

def filter_bad_words(text):
    for word in bad_words:
        text = text.replace(word, '***')
    return text
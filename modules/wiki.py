import wikipedia
from re import sub

wikipedia.set_lang("es")


def search_wiki(text):
    suggestion = wikipedia.suggest(text)

    article = wikipedia.summary(text)

    article = sub(r'\[.*?\]+', '', article)

    return article[0:1000]

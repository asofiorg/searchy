import wikipedia

wikipedia.set_lang("es")


def search_wiki(text):
    suggestion = wikipedia.suggest(text)

    return wikipedia.summary(text, sentences=1)

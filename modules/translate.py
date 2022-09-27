from googletrans import Translator

translator = Translator()


def translate(text):
    translation = translator.translate(text, dest="en")

    return translation.text

from googletrans import Translator

translator = Translator()


def translate(text, dest_locale="en"):
    translation = translator.translate(text, dest=dest_locale)

    return translation.text

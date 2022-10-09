from transformers import pipeline

task = "zero-shot-classification"
model = "Recognai/bert-base-spanish-wwm-cased-xnli"

classifier = pipeline(task, model)
labels = ["búsqueda", "noticias", "traducción", "clima"]
translate_tags = ["traducir a inglés", "traducir a español"]


def classify(text):
    result = classifier(text, labels)

    if result["labels"][0] != "traducción":
        return result["labels"][0]

    translate_result = classifier(text, translate_tags)

    return translate_result["labels"][0]

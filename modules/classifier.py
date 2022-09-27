from transformers import pipeline

task = "zero-shot-classification"
model = "facebook/bart-large-mnli"

classifier = pipeline(task, model)
labels = ["búsqueda", "noticias", "traducción"]

def classify(text):
    result = classifier(text, labels)

    return result["labels"][0]

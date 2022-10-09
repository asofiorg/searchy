INITIAL_ROUTE = "/voice"
START_ROUTE = "/start"
TRANSLATE_ROUTE="/translate"
WEATHER_ROUTE="/weather"
NEWSLETTER_ROUTE="/newsletter"
ADD_NEWSLETTER_ROUTE="/add-newsletter"
FINAL_NEWSLETTER_ROUTE="/final-newsletter"

ES_WELCOME = "Hola soy serchi, dime que quieres hacer y luego presiona numeral"

ES_NEXT_STEP_TRANSLATE="dime que quieres traducir y luego presiona numeral"

ES_NOT_FOUND = "Lo siento, no hemos podido encontrar una respuesta a eso, intentalo de nuevo"

ES_FEEDBACK = "Gracias por usar searhcy ;), Si quieres mandar feedback envia un mensaje a @scidroidpriv en instagram"

ES_THANKS = "Gracias por usar serchi!, Te enviare un SMS con los datos de tu consulta para que puedas revisarlos mas tarde"

ES_NEWS_HEADLINE = "Las 5 noticias mas importantes de hoy"

ES_TRANSLATE = "Menciona el texto que quieres traducir y luego presiona numeral"

ES_TRANSLATE_RESULT = "La traducción es"

ES_WEATHER_PROMPT = "dime de donde quieres saber el clima y luego presiona numeral"

ES_ASK_NEWSLETTER = "si quieres recibir actualizaciones de noticias y clima cada dia pulsa uno, si no pulsa dos"

ES_ASK_LOCATION = "para unirte menciona el nombre del lugar en donde vives y luego pulsa numeral"

ES_DONE_NEWSLETTER = "todo esta listo, ahora recibiras a diario las actualizaciones basadas en tu zona"

def get_sms_result(text):
    return f"Tu resultado de Searchy: {text[:1000]}..."

def get_weather_result(data):
    return f"En {data['name']} hay {data['description']} con una temperatura de {data['temperature']} grados centigrados"

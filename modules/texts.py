INITIAL_ROUTE = "/voice"
START_ROUTE = "/start"
TRANSLATE_ROUTE="/translate"

ES_WELCOME = "Hola soy serchi, ¿que quieres que haga?"

ES_NEXT_STEP_TRANSLATE="dime que quieres traducir"

ES_NOT_FOUND = "Lo siento, no hemos podido encontrar una respuesta a eso, intentalo de nuevo"

ES_FEEDBACK = "Gracias por usar searhcy ;), Si quieres mandar feedback envia un mensaje a @scidroidpriv en instagram"

ES_THANKS = "Gracias por usar serchi!, Te enviare un SMS con los datos de tu consulta para que puedas revisarlos mas tarde"

ES_NEWS_HEADLINE = "Las 5 noticias mas importantes de hoy"

ES_TRANSLATE = "Menciona el texto que quieres traducir"

ES_TRANSLATE_RESULT = "La traducción es"

def get_sms_result(text):
    return f"Tu resultado de Searchy: {text[:1000]}..."

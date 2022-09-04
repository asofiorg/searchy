INITIAL_ROUTE = "/voice"
GATHER_ROUTE = "/gather"

ES_WELCOME = "Hola bienvenido a la prueba alfa de serchi, di el nombre del concepto que quieres buscar"

ES_NOT_FOUND = "Lo siento, no hemos podido encontrar una respuesta a eso, intentalo de nuevo"

ES_FEEDBACK = "Gracias por usar searhcy ;), Si quieres mandar feedback envia un mensaje a @scidroidpriv en instagram"

ES_THANKS = "Gracias por usar serchi!, Te enviare un SMS con los datos de tu consulta para que puedas revisarlos mas tarde"

def get_sms_result(locale: str, text: str) -> str:
    LOCALE = "Tu resultado de Searchy:" if locale == "es" else "Your Searchy result:"

    return f"{LOCALE} {text[:250]}..."

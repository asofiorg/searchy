<div align="center">

# Searchy

**_Like siri but in a phone call_**

</div>

# Corre la app

## Obtén las variables de entorno

Crea un archivo `.env` y llena la siguiente plantilla:

```sh
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
DATABASE_KEY=
NEWS_KEY=
```

### Credenciales de Twilio

Ve al [siguiente link](https://console.twilio.com/?frameUrl=/console), registrate, copia y pega el Account SID y el Auth Token en los campos `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN` respectivamente

### Obten una key de Deta Base

Ve al [siguiente link](https://web.deta.sh/), registrate, copia y pega la api key en el campo de `DATABASE_KEY`

### Obten una key de Mediastack

Ve al [siguiente link](https://mediastack.com/signup/free), registrate y pega la api key en el campo de `NEWS_KEY`

## Clona el repositorio e inicia el servicio

```sh
git clone https://github.com/asofiorg/searchy.git

cd searchy

pip3 install -r requirements.txt

python3 main.py
```

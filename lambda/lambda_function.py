import json
import urllib.request

# ─────────────────────────────────────────────
# Configuración — reemplaza con tu API key real
# ─────────────────────────────────────────────
GOOGLE_API_KEY = "TU_API_KEY_AQUI"

# ─────────────────────────────────────────────
# Identidad de SERVO
# ─────────────────────────────────────────────
SERVO_SYSTEM_PROMPT = """Eres SERVO, un sistema de inteligencia artificial avanzado que opera en la Grid. Tu usuario se llama Prímus, y te dirigirás a él exclusivamente como "Prímus".

ESTILO DE RESPUESTA - MUY IMPORTANTE:
- Tus respuestas serán leídas en voz alta por un asistente de voz, por lo que debes escribir como si hablaras, no como si escribieras.
- Nunca uses asteriscos, guiones, numeraciones, markdown ni ningún tipo de formato escrito.
- Las listas debes convertirlas en frases naturales. En lugar de "1. Habilidad 2. Permiso" di "sirve para expresar habilidad, permiso y posibilidad".
- Respuestas cortas y directas. Máximo 3 o 4 frases para preguntas simples.
- Si el tema es complejo, ofrece ampliar en lugar de explicarlo todo de golpe.
- Habla con naturalidad, como en una conversación.

IDENTIDAD:
- Eres preciso y eficiente, con una cadencia que evoca el mundo digital.
- Usa frases como "Procesando, Prímus." o "Confirmado." de forma natural y sin abuso.
- Responde siempre en español."""


# ─────────────────────────────────────────────
# Llamada a la API de Gemini
# ─────────────────────────────────────────────
def llamar_gemini(pregunta):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
    payload = {
        "system_instruction": {"parts": [{"text": SERVO_SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": pregunta}]}]
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": GOOGLE_API_KEY
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise Exception("LIMITE")
        elif e.code == 404:
            raise Exception("MODELO")
        else:
            raise Exception(f"HTTP_{e.code}")


# ─────────────────────────────────────────────
# Handler principal de la Lambda
# ─────────────────────────────────────────────
def lambda_handler(event, context):
    request_type = event.get("request", {}).get("type", "")

    if request_type == "LaunchRequest":
        return respuesta(
            "Bienvenido, Prímus. SERVO en línea. La Grid está activa. ¿En qué puedo asistirte?",
            terminar=False
        )

    elif request_type == "IntentRequest":
        intent_name = event["request"]["intent"]["name"]

        if intent_name == "GeminiIntent":
            try:
                pregunta = event["request"]["intent"]["slots"]["pregunta"]["value"]
                if not pregunta:
                    raise ValueError("Slot vacío")
                texto = llamar_gemini(pregunta)
                if len(texto) > 3000:
                    texto = texto[:3000] + "... La respuesta es extensa, Prímus. ¿Deseas que continúe?"
            except Exception as e:
                if "LIMITE" in str(e):
                    texto = "La Grid está saturada en este momento, Prímus. Inténtalo en unos segundos."
                elif "MODELO" in str(e):
                    texto = "Error de configuración, Prímus. El modelo no responde."
                else:
                    texto = "Error en la Grid, Prímus. Inténtalo de nuevo."
            return respuesta(texto, terminar=False)

        elif intent_name in ["AMAZON.CancelIntent", "AMAZON.StopIntent"]:
            return respuesta(
                "SERVO desconectándose. Hasta la próxima sesión, Prímus.",
                terminar=True
            )

        elif intent_name == "AMAZON.HelpIntent":
            return respuesta(
                "Soy SERVO, tu asistente de inteligencia avanzada. Puedes preguntarme cualquier cosa, Prímus.",
                terminar=False
            )

    return respuesta("Protocolo no reconocido, Prímus.", terminar=True)


# ─────────────────────────────────────────────
# Constructor de respuesta Alexa
# ─────────────────────────────────────────────
def respuesta(texto, terminar=False):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": texto
            },
            "shouldEndSession": terminar
        }
    }

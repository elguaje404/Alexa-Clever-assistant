# SERVO — Asistente de IA con Alexa + Gemini

> *"SERVO en línea. La Grid está activa."*

SERVO es una Alexa Skill privada que conecta un dispositivo Echo con la API de Google Gemini, creando un asistente de IA avanzado con identidad propia. Coste total de infraestructura: **0€/mes**.

---

## Concepto

SERVO es un asistente de voz construido sobre Alexa, pero con el cerebro de Gemini. A diferencia de Alexa estándar, SERVO puede razonar, analizar y responder preguntas complejas gracias al modelo de lenguaje de Google. La identidad del sistema está inspirada en la estética digital de Tron y Matrix.

- **Nombre del asistente:** SERVO (del latín servir)
- **Nombre del usuario:** Prímus (del latín "el primero")
- **Invocation name:** "unidad servo"
- **Idioma:** Español (España)

---

## Arquitectura

```
[Echo Dot] → [Alexa Console] → [AWS Lambda Alexa-hosted] → [Gemini API]
```

- **Echo Dot** — Dispositivo físico que captura voz y reproduce respuestas
- **Alexa Developer Console** — Gestiona la skill privada y el modelo de interacción
- **AWS Lambda Alexa-hosted** — Ejecuta el código Python (gratuito, gestionado por Amazon)
- **Gemini API** — Genera las respuestas de IA (capa gratuita de Google)

---

## Costes

| Servicio | Plan | Coste |
|---|---|---|
| Alexa Developer Console | Skill privada | Gratis |
| AWS Lambda Alexa-hosted | Gestionado por Amazon | Gratis |
| Google Gemini Flash | 15 RPM / 1M tokens día | Gratis |
| **Total** | | **0€/mes** |

---

## Requisitos previos

- Dispositivo Amazon Echo (cualquier generación)
- Cuenta Amazon (la misma vinculada al Echo)
- Cuenta Google (para la API key de Gemini)

---

## Instalación

### 1. Obtener API key de Gemini

1. Entra en [aistudio.google.com](https://aistudio.google.com)
2. Crea un proyecto nuevo
3. Ve a **Get API Key** → **Create API key**
4. Copia y guarda la clave — empieza por `AIza`

### 2. Crear la Skill en Alexa Developer Console

1. Entra en [developer.amazon.com/alexa/console/ask](https://developer.amazon.com/alexa/console/ask) con el **mismo email** de tu Echo
2. Clic en **Create Skill**
3. Configura:
   - **Skill name:** Servo 
   - **Primary locale:** Spanish (ES)
   - **Model:** Custom
   - **Hosting:** Alexa-hosted (Python)
4. En Templates selecciona **Hello World Skill** o **Start from scratch**
5. Clic en **Create Skill**

### 3. Configurar el modelo de interacción

1. Ve a **Build → Interaction Model → JSON Editor**
2. Borra el contenido y pega el archivo `interaction_model/es-ES.json` de este repositorio
3. Clic en **Save Model** → **Build Model**
4. Espera a que compile (~2 minutos)

> **Nota:** El invocation name es `unidad servo`. Alexa requiere mínimo dos palabras para el nombre de invocación.

### 4. Subir el código

1. Ve a la pestaña **Code**
2. Abre `lambda/lambda_function.py` y reemplaza con el contenido de este repositorio
3. Abre `lambda/requirements.txt` y déjalo vacío (no se necesitan dependencias externas)

```
GOOGLE_API_KEY=tu_api_key_aqui
```

> **Importante:** El archivo `.env` está en `.gitignore`. Nunca subas tu API key a un repositorio público.

5. Clic en **Save** → **Deploy**

### 5. Activar y probar

1. Ve a la pestaña **Test**
2. Cambia el selector de **Off** a **Development**
3. Escribe `abre unidad servo`
4. SERVO debería responder: *"Bienvenido, Prímus. SERVO en línea. La Grid está activa."*

---

## Estructura del repositorio

```
servo-alexa/
├── README.md
├── .gitignore
├── interaction_model/
│   └── es-ES.json          # Modelo de interacción (intents y utterances)
└── lambda/
    ├── lambda_function.py  # Código principal de la skill
    └── requirements.txt    # Dependencias (vacío — usa solo stdlib de Python)
```

---

## Uso

Una vez activa la skill, interactúa con SERVO así:

```
"Alexa, abre unidad servo"
→ SERVO en línea. ¿En qué puedo asistirte?

"dime cuántos planetas hay en el sistema solar"
→ Hay ocho planetas, Prímus: Mercurio, Venus, la Tierra...

"Alexa, para"
→ SERVO desconectándose. Hasta la próxima sesión, Prímus.
```

---

## Personalización

### Cambiar la identidad de SERVO

Edita la variable `SERVO_SYSTEM_PROMPT` en `lambda_function.py`. Puedes modificar el nombre del asistente, el nombre del usuario, el estilo de respuesta o el idioma.

### Cambiar el modelo de Gemini

En `lambda_function.py`, modifica la URL en la función `llamar_gemini`:

```python
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
```

Modelos disponibles en la capa gratuita: `gemini-flash-latest`, `gemini-2.0-flash`

### Cambiar el invocation name

En **Build → Invocations → Skill Invocation Name**. Alexa requiere mínimo dos palabras y no permite nombres de marcas registradas.

---

## Limitaciones conocidas

- **Sin memoria entre sesiones** — Cada conversación empieza desde cero. Para añadir memoria persistente se necesitaría DynamoDB (tiene capa gratuita).
- **Timeout de 8 segundos** — Preguntas muy complejas pueden tardar. Si SERVO no responde, es probable un timeout de la Lambda.
- **Rate limit de Gemini** — 15 peticiones por minuto en la capa gratuita. Para uso personal es más que suficiente.
- **Voz de Alexa** — La skill usa la voz predeterminada de Alexa en español. Voces alternativas como ElevenLabs requieren integración adicional con S3.

---

## Posibles mejoras futuras

- **Memoria de sesión** — Historial de conversación dentro de la misma sesión
- **Memoria persistente** — Usando DynamoDB para recordar contexto entre sesiones
- **Integración con calendario** — Conectar con Google Calendar via API
- **Control del hogar** — Integrar con Alexa Smart Home API
- **Voz personalizada** — ElevenLabs para síntesis de voz propia

---

## Tecnologías

- Python 3.x (stdlib únicamente — sin dependencias externas)
- Amazon Alexa Skills Kit
- AWS Lambda (Alexa-hosted)
- Google Gemini API

---

## Licencia

Proyecto personal de uso privado. La skill está configurada como privada y solo es accesible desde la cuenta Amazon del desarrollador.

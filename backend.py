import openai
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar la clave API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Función para obtener la respuesta del modelo GPT-4o
def get_gpt4o_response(conversation):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=conversation,
            max_tokens=150,
            temperature=1
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        return f"Error en la solicitud: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

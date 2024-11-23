import openai
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Proporciona tu clave API aquí
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prueba con el modelo gpt-4o
try:
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Cambiamos el modelo a gpt-4o
        messages=[
            {"role": "user", "content": "Hola, ¿qué puedes hacer?"}
        ],
        max_completion_tokens=100,  # Ajusta este valor según sea necesario
        temperature=1  # gpt-4o admite este valor predeterminado
    )
    print("Respuesta del modelo gpt-4o:")
    print(response["choices"][0]["message"]["content"])
except openai.error.InvalidRequestError as e:
    print(f"Solicitud inválida: {e}")
except openai.error.AuthenticationError:
    print("Error de autenticación: verifica tu clave API.")
except Exception as e:
    print(f"Error inesperado: {e}")

import openai
from dotenv import load_dotenv
import os
# Cargar variables de entorno desde .env
load_dotenv()

# Proporciona tu clave API aquí
openai.api_key = os.getenv("OPENAI_API_KEY")
# Ejemplo: listar modelos
models = openai.Model.list()
print(models)

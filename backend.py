from langchain.chat_models import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.cache import BaseCache
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Definir la base del modelo de caché
class SimpleCache(BaseCache):
    pass

# Registrar la caché si es necesario
SimpleCache()

# 1. Configurar la clave API de OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# 2. Cargar la base de datos
db = SQLDatabase.from_uri("sqlite:///ecommerce.db")

# 3. Crear el modelo de lenguaje (LLM)
llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

# 4. Crear la cadena usando `SQLDatabaseChain`
SQLDatabaseChain.model_rebuild()  # Reconstruir el modelo
db_chain = SQLDatabaseChain.from_llm(llm=llm, database=db, verbose=True)

# 5. Definir una función para realizar consultas
def consulta(input_usuario):
    resultado = db_chain.run(input_usuario)
    return resultado

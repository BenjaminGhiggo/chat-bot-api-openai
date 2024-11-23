import openai
import os
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar la clave API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Conexión a la base de datos PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        dbname=os.getenv("DATABASE"),
        port=os.getenv("PORT")
    )

# Función para obtener respuesta del modelo GPT-4o con datos de la base de datos
def get_gpt4o_response(conversation):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=conversation,
            max_tokens=300,  # Reducido para limitar la longitud de la respuesta
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except openai.error.OpenAIError as e:
        return f"Error en la solicitud: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

# Función para manejar la lógica del agente de mercado
def market_agent(user_input, categoria=None, ubicacion=None):
    # Establecer conexión con la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener datos relevantes de la base de datos
    data = query_market_data(user_input, cursor, categoria, ubicacion)

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Construir la conversación
    conversation = [
        {
            "role": "system",
            "content": (
                "Eres un analista de mercado experto que proporciona insights basados en datos. "
                "Las respuestas deben ser concisas y no exceder los 3 párrafos."
            ),
        },
        {
            "role": "user",
            "content": f"Pregunta: {user_input}\nDatos relevantes: {data}"
        }
    ]

    # Obtener respuesta del modelo
    assistant_reply = get_gpt4o_response(conversation)
    return assistant_reply

def query_market_data(question, cursor, categoria=None, ubicacion=None):
    if "precio promedio" in question.lower() and "producto similar" in question.lower():
        if categoria:
            cursor.execute("""
                SELECT AVG(precio) FROM agente_mercado
                WHERE categoria = %s;
            """, (categoria,))
            avg_price = cursor.fetchone()[0]
            if avg_price:
                return f"El precio promedio de productos similares en la categoría '{categoria}' es ${avg_price:.2f}."
            else:
                return f"No se encontraron datos para la categoría '{categoria}'."
        else:
            return "Categoría del producto no proporcionada."
    elif "competitivo" in question.lower() and "mi zona" in question.lower():
        if ubicacion:
            cursor.execute("""
                SELECT COUNT(*) FROM agente_mercado
                WHERE ubicacion_geografica = %s;
            """, (ubicacion,))
            competitors = cursor.fetchone()[0]
            return f"En tu zona ({ubicacion}), hay {competitors} competidores en tu categoría de producto."
        else:
            return "Ubicación geográfica no proporcionada."
    elif "mercados internacionales" in question.lower() and "interesados" in question.lower():
        cursor.execute("""
            SELECT mercados_internacionales FROM agente_mercado;
        """)
        rows = cursor.fetchall()
        mercados = set()
        for row in rows:
            mercados.update(map(str.strip, row[0].split(",")))
        return f"Mercados internacionales potenciales: {', '.join(mercados)}."
    # Agregar más condiciones para otras preguntas
    else:
        return "No se encontraron datos específicos para tu pregunta, pero puedo proporcionarte insights generales de mercado."

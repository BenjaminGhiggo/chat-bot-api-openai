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
            max_tokens=500,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        return f"Error en la solicitud: {e}"
    except Exception as e:
        return f"Error inesperado: {e}"

# Función para manejar la lógica del agente de marketing
def marketing_agent(user_input, producto=None, objetivo=None, presupuesto=None):
    # Establecer conexión con la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener datos relevantes de la base de datos
    data = query_marketing_data(user_input, cursor, producto, objetivo, presupuesto)

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Construir la conversación
    conversation = [
        {"role": "system", "content": "Eres un experto en marketing que proporciona consejos y estrategias basadas en datos."},
        {"role": "user", "content": f"Pregunta: {user_input}\nDatos relevantes: {data}"}
    ]

    # Obtener respuesta del modelo
    assistant_reply = get_gpt4o_response(conversation)
    return assistant_reply

def query_marketing_data(question, cursor, producto, objetivo, presupuesto):
    if "crear" in question.lower() and "campaña de marketing" in question.lower():
        if producto and objetivo and presupuesto is not None:
            cursor.execute("""
                SELECT plataformas_utilizadas, tipo_anuncio, estrategias_utilizadas
                FROM agente_marketing
                WHERE presupuesto <= %s
                ORDER BY presupuesto DESC LIMIT 1;
            """, (presupuesto,))
            row = cursor.fetchone()
            if row:
                return f"Basado en campañas exitosas, se recomienda para el producto '{producto}' con el objetivo '{objetivo}' y presupuesto ${presupuesto:.2f} usar plataformas '{row[0]}', tipo de anuncio '{row[1]}' y estrategias '{row[2]}'."
            else:
                return "No se encontraron campañas similares para sugerir."
        else:
            return "Faltan datos necesarios para proporcionar una respuesta completa."
    elif "promocionar mi producto en redes sociales" in question.lower():
        cursor.execute("""
            SELECT DISTINCT plataformas_utilizadas FROM agente_marketing;
        """)
        rows = cursor.fetchall()
        plataformas = set()
        for row in rows:
            plataformas.update(map(str.strip, row[0].split(",")))
        return f"Puedes promocionar tu producto en las siguientes plataformas: {', '.join(plataformas)}."
    elif "tipo de anuncios funcionan mejor" in question.lower() and "redes sociales" in question.lower():
        cursor.execute("""
            SELECT tipo_anuncio, COUNT(*) AS conteo FROM agente_marketing
            GROUP BY tipo_anuncio ORDER BY conteo DESC LIMIT 1;
        """)
        row = cursor.fetchone()
        if row:
            return f"El tipo de anuncio que funciona mejor en redes sociales es '{row[0]}'."
        else:
            return "No se encontró información sobre el tipo de anuncios."
    else:
        return "No se encontraron datos específicos para tu pregunta, pero puedes proporcionar más detalles."

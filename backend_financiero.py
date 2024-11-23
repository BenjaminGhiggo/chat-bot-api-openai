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

# Función para manejar la lógica del agente financiero
def financial_agent(user_input):
    # Establecer conexión con la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener datos relevantes de la base de datos
    data = query_financial_data(user_input, cursor)

    # Cerrar la conexión a la base de datos
    cursor.close()
    conn.close()

    # Construir la conversación
    conversation = [
        {"role": "system", "content": "Eres un asesor financiero experto que proporciona respuestas detalladas basadas en los datos proporcionados."},
        {"role": "user", "content": f"Pregunta: {user_input}\nDatos relevantes: {data}"}
    ]

    # Obtener respuesta del modelo
    assistant_reply = get_gpt4o_response(conversation)
    return assistant_reply

def query_financial_data(question, cursor):
    # Analizar la pregunta y extraer información relevante
    if "financiamiento" in question.lower() and "negocio pequeño" in question.lower():
        # Obtener opciones de financiamiento para negocios pequeños
        cursor.execute("""
            SELECT opciones_financiamiento FROM agente_financiero
            WHERE tipo_negocio = 'Pequeño';
        """)
        rows = cursor.fetchall()
        opciones = set()
        for row in rows:
            opciones.update(map(str.strip, row[0].split(",")))
        return f"Opciones de financiamiento para negocios pequeños: {', '.join(opciones)}"
    elif "califico para un préstamo" in question.lower():
        # Proporcionar información general sobre calificación para préstamos
        cursor.execute("""
            SELECT nivel_endeudamiento, ingresos_mensuales FROM agente_financiero;
        """)
        rows = cursor.fetchall()
        niveles = [row[0] for row in rows]
        ingresos = [row[1] for row in rows]
        promedio_ingresos = sum(ingresos) / len(ingresos)
        return f"El nivel de endeudamiento promedio es {niveles.count('Bajo') / len(niveles) * 100}% bajo. Los ingresos mensuales promedio son ${promedio_ingresos:.2f}."
    elif "documentos necesito" in question.lower() and "préstamo" in question.lower():
        cursor.execute("""
            SELECT DISTINCT documentos_necesarios FROM agente_financiero;
        """)
        rows = cursor.fetchall()
        documentos = set()
        for row in rows:
            documentos.update(map(str.strip, row[0].split(",")))
        return f"Documentos necesarios para pedir un préstamo: {', '.join(documentos)}"
    # Agregar más condiciones para otras preguntas
    else:
        return "No se encontraron datos específicos para tu pregunta, pero puedes proporcionar más detalles."


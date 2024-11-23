import openai
from dotenv import load_dotenv
import os
import asyncio

# Cargar variables de entorno desde .env
load_dotenv()

# Configurar la clave API
openai.api_key = os.getenv("OPENAI_API_KEY")

async def chat_with_gpt4o():
    print("Inicia un chat con GPT-4o. Escribe 'salir' para terminar.")
    conversation = []  # Para almacenar el contexto del chat

    while True:
        # Solicitar entrada del usuario
        user_input = input("Tú: ")

        if user_input.lower() == "salir":
            print("¡Adiós!")
            break

        # Añadir mensaje del usuario al contexto
        conversation.append({"role": "user", "content": user_input})

        try:
            # Llamar al modelo GPT-4o
            response = await openai.ChatCompletion.acreate(
                model="gpt-4o",
                messages=conversation,
                max_tokens=150,
                temperature=1
            )

            # Obtener la respuesta
            assistant_reply = response.choices[0].message.content
            print(f"GPT-4o: {assistant_reply}")

            # Añadir la respuesta del asistente al contexto
            conversation.append({"role": "assistant", "content": assistant_reply})

        except openai.error.OpenAIError as e:
            print(f"Error de OpenAI: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    asyncio.run(chat_with_gpt4o())

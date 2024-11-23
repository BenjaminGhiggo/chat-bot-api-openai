import streamlit as st
from chat_terminal import get_gpt4o_response

# Configuración de la página
st.set_page_config(page_title="Chat GPT-4o", page_icon="💬", layout="wide")

# Título de la aplicación
st.title("Chat GPT-4o 💬")
st.markdown("Interactúa con el modelo GPT-4o directamente desde esta interfaz.")

# Área de conversación
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Entrada del usuario
user_input = st.text_input("Escribe tu mensaje:", key="user_input")

# Manejo de la interacción
if st.button("Enviar"):
    if user_input.strip():
        # Añadir mensaje del usuario al contexto
        st.session_state.conversation.append({"role": "user", "content": user_input})
        
        # Obtener respuesta del modelo
        assistant_reply = get_gpt4o_response(st.session_state.conversation)
        
        # Añadir respuesta del asistente al contexto
        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

# Mostrar la conversación
st.markdown("### Conversación:")
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**Tú:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**GPT-4o:** {msg['content']}")

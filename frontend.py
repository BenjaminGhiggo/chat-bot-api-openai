import streamlit as st
from backend import get_gpt4_response

# Inicializar conversación en el estado de la sesión
if "conversation" not in st.session_state:
    st.session_state.conversation = []
    # Añadir un mensaje inicial del sistema si es necesario
    st.session_state.conversation.append({"role": "system", "content": "Eres un asistente que proporciona información financiera, de mercado y marketing basándote en los datos proporcionados."})

# Título y descripción
st.title("Chat con Agentes Especializados 💬")
st.markdown("Interactúa con agentes financieros, de mercado y marketing directamente desde esta interfaz.")

# Entrada del usuario
user_input = st.text_input("Escribe tu mensaje:", key="user_input")

# Manejo de la interacción
if st.button("Enviar") or st.session_state.get('enter_pressed'):
    if user_input.strip():
        # Añadir el mensaje del usuario a la conversación
        st.session_state.conversation.append({"role": "user", "content": user_input})

        # Obtener respuesta del modelo
        assistant_reply = get_gpt4_response(st.session_state.conversation)

        # Añadir respuesta del modelo a la conversación
        st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})

        # Limpiar el input después de enviar
        st.session_state.user_input = ""
        st.session_state.enter_pressed = False

# Capturar el evento de presionar "Enter"
def on_enter():
    st.session_state.enter_pressed = True

st.text_input("Escribe tu mensaje:", key="user_input", on_change=on_enter)

# Mostrar la conversación
st.markdown("### Conversación:")
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**Tú:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Asistente:** {msg['content']}")
    elif msg["role"] == "system":
        # Puedes optar por no mostrar los mensajes del sistema en la interfaz
        pass

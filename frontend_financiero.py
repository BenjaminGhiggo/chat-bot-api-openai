import streamlit as st
from backend_financiero import financial_agent

# Inicializar conversación en el estado de la sesión
if "conversation_financiero" not in st.session_state:
    st.session_state.conversation_financiero = []

# Título y descripción
st.title("Agente Financiero 💰")
st.markdown("Haz tus preguntas financieras y recibe asesoramiento experto.")

# Entrada del usuario
user_input = st.text_input("Escribe tu pregunta:", key="user_input_financiero")

# Manejo de la interacción
if st.button("Enviar", key="send_button_financiero"):
    if user_input.strip():
        # Obtener respuesta del agente financiero
        assistant_reply = financial_agent(user_input)

        # Añadir a la conversación
        st.session_state.conversation_financiero.append({"role": "user", "content": user_input})
        st.session_state.conversation_financiero.append({"role": "assistant", "content": assistant_reply})

# Mostrar la conversación
st.markdown("### Conversación:")
for msg in st.session_state.conversation_financiero:
    if msg["role"] == "user":
        st.markdown(f"**Tú:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Agente Financiero:** {msg['content']}")

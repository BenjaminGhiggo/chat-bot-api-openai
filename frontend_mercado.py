import streamlit as st
from backend_mercado import market_agent

# Inicializar conversación en el estado de la sesión
if "conversation_mercado" not in st.session_state:
    st.session_state.conversation_mercado = []

# Título y descripción
st.title("Agente de Mercado 📊")
st.markdown("Realiza consultas sobre el mercado y obtén análisis especializados.")

# Variables para almacenar datos adicionales
categoria = None
ubicacion = None

# Entrada del usuario
user_input = st.text_input("Escribe tu pregunta:", key="user_input_mercado")

# Si la pregunta requiere datos adicionales, solicitarlos al usuario
if user_input:
    if "precio promedio" in user_input.lower() and "producto similar" in user_input.lower():
        categoria = st.text_input("Ingresa la categoría de tu producto:", key="categoria")
    elif "competitivo" in user_input.lower() and "mi zona" in user_input.lower():
        ubicacion = st.text_input("Ingresa tu ubicación geográfica:", key="ubicacion")

# Manejo de la interacción
if st.button("Enviar", key="send_button_mercado"):
    if user_input.strip():
        with st.spinner("Obteniendo respuesta..."):
            # Obtener respuesta del agente de mercado
            assistant_reply = market_agent(user_input, categoria, ubicacion)

            # Añadir a la conversación
            st.session_state.conversation_mercado.append({"role": "user", "content": user_input})
            st.session_state.conversation_mercado.append({"role": "assistant", "content": assistant_reply})

    # Mostrar la conversación
    st.markdown("### Conversación:")
    for msg in st.session_state.conversation_mercado:
        if msg["role"] == "user":
            st.markdown(f"**Tú:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Agente de Mercado:** {msg['content']}")

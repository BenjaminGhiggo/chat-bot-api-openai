import streamlit as st
from backend_marketing import marketing_agent

# Inicializar conversación en el estado de la sesión
if "conversation_marketing" not in st.session_state:
    st.session_state.conversation_marketing = []

# Título y descripción
st.title("Agente de Marketing 📣")
st.markdown("Haz tus preguntas sobre marketing y recibe consejos expertos.")

# Variables para almacenar datos adicionales
producto = None
objetivo = None
presupuesto = None

# Entrada del usuario
user_input = st.text_input("Escribe tu pregunta:", key="user_input_marketing")

# Si la pregunta requiere datos adicionales, solicitarlos al usuario
if user_input:
    if "crear" in user_input.lower() and "campaña de marketing" in user_input.lower():
        st.markdown("### Información adicional requerida:")
        producto = st.text_input("Ingresa el nombre de tu producto:", key="producto")
        objetivo = st.text_input("Ingresa el objetivo de tu campaña:", key="objetivo")
        presupuesto = st.number_input("Ingresa tu presupuesto:", min_value=0.0, key="presupuesto")

# Manejo de la interacción
if st.button("Enviar", key="send_button_marketing"):
    if user_input.strip():
        with st.spinner("Obteniendo respuesta..."):
            # Obtener respuesta del agente de marketing
            assistant_reply = marketing_agent(user_input, producto, objetivo, presupuesto)

            # Añadir a la conversación
            st.session_state.conversation_marketing.append({"role": "user", "content": user_input})
            st.session_state.conversation_marketing.append({"role": "assistant", "content": assistant_reply})

    # Mostrar la conversación
    st.markdown("### Conversación:")
    for msg in st.session_state.conversation_marketing:
        if msg["role"] == "user":
            st.markdown(f"**Tú:** {msg['content']}")
        elif msg["role"] == "assistant":
            st.markdown(f"**Agente de Marketing:** {msg['content']}")

# Lanzar la aplicación con el comando "streamlit run c_front_end.py" en el terminal
import backend  # Importar el módulo backend que contiene la lógica de procesamiento de consultas
import streamlit as st  # Importar la biblioteca Streamlit para crear la interfaz de usuario
from streamlit_chat import message  # Importar la función message para mostrar mensajes de chat en Streamlit

# Establecer el título de la aplicación
st.title("Bienvenido al sistema de consultas")
# Añadir una descripción debajo del título
st.write("¡Puedes hacerme a mi todas las preguntas")

# Inicializar el estado de la sesión para almacenar preguntas si no existe
if 'preguntas' not in st.session_state:
    st.session_state.preguntas = []
# Inicializar el estado de la sesión para almacenar respuestas si no existe
if 'respuestas' not in st.session_state:
    st.session_state.respuestas = []

# Definir la función que se ejecuta al hacer clic en el botón de enviar
def click():
    # Verificar si el input del usuario no está vacío
    if st.session_state.user != '':
        # Obtener la pregunta del usuario
        pregunta = st.session_state.user
        # Obtener la respuesta llamando a la función consulta del módulo backend
        respuesta = backend.consulta(pregunta)

        # Añadir la pregunta y la respuesta al estado de la sesión
        st.session_state.preguntas.append(pregunta)
        st.session_state.respuestas.append(respuesta)

        # Limpiar el input de usuario después de enviar la pregunta
        st.session_state.user = ''

# Crear un formulario en Streamlit
with st.form('my-form'):
   # Añadir un campo de texto para que el usuario ingrese su pregunta
   query = st.text_input('¿En qué te puedo ayudar?:', key='user', help='Pulsa Enviar para hacer la pregunta')
   # Añadir un botón de submit que ejecuta la función click cuando se hace clic
   submit_button = st.form_submit_button('Enviar', on_click=click)

# Verificar si hay preguntas en el estado de la sesión
if st.session_state.preguntas:
    # Mostrar las respuestas en orden inverso (de la más reciente a la más antigua)
    for i in range(len(st.session_state.respuestas)-1, -1, -1):
        message(st.session_state.respuestas[i], key=str(i))

    # Añadir una opción para que el usuario continúe la conversación
    continuar_conversacion = st.checkbox('¿Quieres hacer otra pregunta?')
    # Si el usuario no quiere continuar, limpiar las preguntas y respuestas del estado de la sesión
    if not continuar_conversacion:
        st.session_state.preguntas = []
        st.session_state.respuestas = []


import streamlit as st
from datetime import datetime, timedelta

if 'retos' not in st.session_state:
    st.session_state.retos = []

if 'apuestas' not in st.session_state:
    st.session_state.apuestas = []

st.title("FAILBANK - Apuesta contra ti mismo")

menu = st.sidebar.selectbox("Menú", ["Crear reto", "Ver retos", "Mis apuestas"])

def crear_reto():
    st.header("Crea un reto personal")

    nombre = st.text_input("Tu nombre")
    descripcion = st.text_area("Describe tu reto")
    monto = st.number_input("¿Cuánto apuestas? (€)", min_value=1, step=1)
    dias = st.number_input("Plazo para cumplir (días)", min_value=1, max_value=30, step=1)

    if st.button("Publicar reto"):
        fecha_limite = datetime.now() + timedelta(days=dias)
        reto = {
            "id": len(st.session_state.retos) + 1,
            "nombre": nombre,
            "descripcion": descripcion,
            "monto": monto,
            "fecha_limite": fecha_limite,
            "creador": nombre,
            "cumplido": None
        }
        st.session_state.retos.append(reto)
        st.success(f"Reto creado! Plazo hasta {fecha_limite.strftime('%d/%m/%Y')}")

def ver_retos():
    st.header("Retos disponibles para apostar contra")

    if len(st.session_state.retos) == 0:
        st.info("No hay retos activos. ¡Crea uno!")
        return

    for reto in st.session_state.retos:
        if reto['cumplido'] is None:
            st.write(f"**Reto #{reto['id']} - {reto['descripcion']}**")
            st.write(f"Apuesta del creador: {reto['monto']}€")
            st.write(f"Fecha límite: {reto['fecha_limite'].strftime('%d/%m/%Y')}")
            apostar = st.number_input(f"Apuesta en contra del reto #{reto['id']} (€)", min_value=0, step=1, key=f"apostar_{reto['id']}")
            if st.button(f"Apostar contra Reto #{reto['id']}", key=f"btn_apostar_{reto['id']}"):
                if apostar > 0:
                    apuesta = {
                        "reto_id": reto['id'],
                        "apostador": "Usuario",
                        "monto": apostar
                    }
                    st.session_state.apuestas.append(apuesta)
                    st.success(f"Apostaste {apostar}€ contra el reto #{reto['id']}")
                else:
                    st.error("Debes apostar más de 0€")

def mis_apuestas():
    st.header("Mis retos y estado")

    for reto in st.session_state.retos:
        st.write(f"**Reto #{reto['id']} - {reto['descripcion']}**")
        st.write(f"Creado por: {reto['creador']} - Apuesta: {reto['monto']}€")
        st.write(f"Fecha límite: {reto['fecha_limite'].strftime('%d/%m/%Y')}")
        estado = "Pendiente"
        if reto['cumplido'] == True:
            estado = "Cumplido ✅"
        elif reto['cumplido'] == False:
            estado = "Fallado ❌"
        st.write(f"Estado: {estado}")

        if reto['cumplido'] is None:
            cumplio = st.radio(f"¿Cumpliste el reto #{reto['id']}?", ("Pendiente", "Sí", "No"), key=f"cumplido_{reto['id']}")
            if cumplio == "Sí":
                reto['cumplido'] = True
                st.success(f"Marcaste como cumplido el reto #{reto['id']}")
            elif cumplio == "No":
                reto['cumplido'] = False
                st.error(f"Marcaste como fallado el reto #{reto['id']}")

    st.subheader("Apuestas ganadoras")
    for apuesta in st.session_state.apuestas:
        reto = next((r for r in st.session_state.retos if r['id'] == apuesta['reto_id']), None)
        if reto and reto['cumplido'] is not None:
            if (reto['cumplido'] == False and apuesta['reto_id'] == reto['id']):
                st.write(f"El apostador ganó {apuesta['monto']}€ en el reto #{reto['id']}")

st.write("---")

if menu == "Crear reto":
    crear_reto()
elif menu == "Ver retos":
    ver_retos()
elif menu == "Mis apuestas":
    mis_apuestas()
elif menu == "Azahara":
    Azahara()

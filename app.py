
import streamlit as st
from PIL import Image
from fpdf import FPDF
import os
import datetime

# 🔒 Blocco password (semplice protezione)
PASSWORD = "15092001"  # ← puoi cambiarla come vuoi
password = st.text_input("🔒 Inserisci la password per accedere all'app", type="password")
if password != PASSWORD:
    st.warning("❌ Password errata o non inserita.")
    st.stop()
    
# Titolo dell'app
st.set_page_config(page_title="Radiology AI - Referto PDF Demo", layout="centered")
st.title("🧠 Radiology AI – Referto PDF Demo")

# Caricamento immagine
st.subheader("🖼️ Carica un'immagine radiologica")
uploaded_file = st.file_uploader("Carica un'immagine radiologica", type=["jpg", "jpeg", "png"])

# Selezione del distretto anatomico
st.subheader("📍 Seleziona il distretto anatomico")
distretto = st.selectbox("Distretto", ["Torace", "Addome", "Cranio", "Colonna vertebrale", "Arti superiori", "Arti inferiori"])

# Generazione del referto
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Immagine caricata", use_container_width=True)

    # Referto simulato
    st.subheader("📝 Referto AI")
    referto = f"Possibili anomalie riscontrate nel distretto {distretto.lower()}: infiltrati, edema, anomalie strutturali.\n"
    referto += "Si consiglia correlazione clinica e confronto con immagini precedenti."

    st.text_area("Referto", referto, height=150)

    # Bottone per generare il PDF
    if st.button("📄 Genera PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Referto Radiologico AI", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt=f"Distretto Anatomico: {distretto}", ln=True)
        pdf.ln(5)

        pdf.set_font("Arial", size=12)
        for riga in referto.split("\n"):
            pdf.multi_cell(0, 10, riga)

        filename = f"referto_{distretto.lower().replace(' ', '_')}.pdf"
        pdf.output(filename)

        with open(filename, "rb") as f:
            st.download_button("📥 Scarica PDF", f, file_name=filename)

        os.remove(filename)



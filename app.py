
import streamlit as st
from PIL import Image
import pydicom
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uuid
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# 🔐 Password (semplice protezione)
PASSWORD = "15092001"
password = st.text_input("🔒 Inserisci la password per accedere all'app", type="password")
if password != PASSWORD:
    st.warning("❌ Password errata o non inserita.")
    st.stop()

st.set_page_config(page_title="Radiology AI – Autoapprendimento", layout="centered")
st.title("🧠 Radiology AI – Referto con Autoapprendimento")

# Upload immagine
uploaded_file = st.file_uploader("📤 Carica immagine DICOM o PNG/JPG", type=["dcm", "jpg", "jpeg", "png"])
img = None

# Selezione distretto
distretto = st.selectbox("📍 Seleziona il distretto", [
    "Torace", "Addome", "Cranio", "Colonna vertebrale", "Arti superiori", "Arti inferiori"
])

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext == "dcm":
        dcm = pydicom.dcmread(uploaded_file)
        pixel_array = dcm.pixel_array
        norm_img = (pixel_array - np.min(pixel_array)) / (np.max(pixel_array) - np.min(pixel_array))
        norm_img = (norm_img * 255).astype(np.uint8)
        img = Image.fromarray(norm_img)
        st.image(img, caption="🩻 Immagine DICOM", use_container_width=True)
    else:
        img = Image.open(uploaded_file)
        st.image(img, caption="🖼️ Immagine caricata", use_container_width=True)

    # Referto simulato
    st.subheader("📝 Referto AI")
    referto = f"Possibili anomalie nel distretto {distretto.lower()}: Infiltrati (0.68), Edema (0.64), Polmonite (0.54).\n"
    referto += "Si consiglia correlazione clinica."
    st.text_area("Referto generato", referto, height=150)

    # Feedback utente
    st.subheader("🧬 Feedback dell'utente")
    feedback = st.radio("Il referto è corretto?", ["✅ Sì", "❌ No"])
    note = st.text_area("📝 Note o correzioni (facoltative)")

    # Pulsante salvataggio PDF + feedback
    if st.button("💾 Salva referto + feedback e genera PDF"):
        # PDF
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        x, y = 50, height - 50
        c.setFont("Helvetica", 12)
        c.drawString(x, y, "Referto AI – Radiologia Multiorgano")
        y -= 20
        c.drawString(x, y, f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        y -= 20
        c.drawString(x, y, f"Distretto: {distretto}")
        y -= 30
        for line in referto.split("\n"):
            c.drawString(x, y, line)
            y -= 20
        c.showPage()
        c.save()
        buffer.seek(0)

        st.download_button("📄 Scarica PDF referto", buffer, file_name=f"referto_{distretto.lower()}.pdf", mime="application/pdf")

        # Salvataggio feedback
        log_row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "distretto": distretto,
            "referto_ai": referto.replace("\n", " "),
            "feedback": feedback,
            "note": note
        }
        log_file = "feedback_log.csv"
        if os.path.exists(log_file):
            df = pd.read_csv(log_file)
            df = pd.concat([df, pd.DataFrame([log_row])], ignore_index=True)
        else:
            df = pd.DataFrame([log_row])
        df.to_csv(log_file, index=False)
        st.success("✅ Feedback salvato correttamente.")


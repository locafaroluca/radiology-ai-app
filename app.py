
import streamlit as st
from PIL import Image
import uuid
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

st.set_page_config(page_title="Radiology AI", page_icon="🧠")
st.title("🧠 Radiology AI – Referto PDF Demo")

# Caricamento immagine
uploaded_file = st.file_uploader("📤 Carica un'immagine radiologica", type=["jpg", "jpeg", "png"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Immagine caricata", use_container_width=True)

    # Simulazione referto
    predictions = {
        "Infiltrati": 0.68,
        "Polmonite": 0.54,
        "Edema": 0.64
    }

    referto_lines = [
        "Referto AI",
        f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Possibili anomalie riscontrate:"
    ] + [f"- {k}: {v}" for k, v in predictions.items()] + [
        "",
        "Si consiglia correlazione clinica."
    ]
    referto_text = "\n".join(referto_lines)

    st.subheader("📝 Referto")
    st.text(referto_text)

    # Funzione per creare PDF
    def genera_pdf_referto(referto_text, image):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        x_margin = 50
        y_position = height - 50

        for line in referto_text.split("\n"):
            c.drawString(x_margin, y_position, line)
            y_position -= 20

        # Converti e salva immagine temporaneamente
        img_id = f"temp_{uuid.uuid4().hex}.jpg"
        image = image.convert("RGB")
        image.save(img_id)

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    # Download del PDF
    pdf_buffer = genera_pdf_referto(referto_text, img)
    st.download_button(
        label="📄 Scarica referto in PDF",
        data=pdf_buffer,
        file_name="referto_ai.pdf",
        mime="application/pdf"
    )



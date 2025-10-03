
import streamlit as st
import os
import uuid
import json
from PIL import Image
import random

st.set_page_config(page_title="Radiology AI – All-in-One", page_icon="🧠")
st.title("🧠 Radiology AI – All-in-One")
st.markdown("Carica un'immagine radiologica (RX, TAC, ecc.) e seleziona il distretto da analizzare:")

DISTRETTI = [
    "Torace", "Addome", "Cranio", "Colonna vertebrale", "Arti superiori", "Arti inferiori"
]

uploaded_file = st.file_uploader("📤 Carica un'immagine", type=["jpg", "png", "jpeg"])
distretto = st.selectbox("📍 Distretto anatomico", DISTRETTI)

if uploaded_file and distretto:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Immagine caricata", use_column_width=True)

    st.subheader("🧠 Analisi AI in corso...")

    # Finta AI: risultati casuali
    possibili_anomalie = {
        "Torace": ["Infiltrati", "Polmonite", "Edema", "Versamento pleurico", "Massa"],
        "Addome": ["Occlusione", "Masse addominali", "Perforazione", "Calcificazioni", "Distensione"],
        "Cranio": ["Emorragia", "Frattura", "Edema cerebrale", "Lesione occupante spazio"],
        "Colonna vertebrale": ["Frattura vertebrale", "Ernia del disco", "Stenosi", "Spondilolistesi"],
        "Arti superiori": ["Frattura", "Lussazione", "Osteoporosi", "Infiammazione articolare"],
        "Arti inferiori": ["Frattura", "Artrosi", "Infiammazione", "Trombosi"]
    }

    anomalie = random.sample(possibili_anomalie.get(distretto, []), k=2)
    risultati = {a: round(random.uniform(0.6, 0.95), 2) for a in anomalie}

    st.success("✅ Referto AI generato con successo")
    for k, v in risultati.items():
        st.write(f"- {k}: {v}")

    referto = f"Nel distretto {distretto} si rilevano possibili anomalie: " +               ", ".join([f"{k} ({v})" for k, v in risultati.items()]) + ". Si consiglia correlazione clinica."

    st.markdown("### 📝 Referto finale")
    st.write(referto)

    # Salvataggio
    if st.button("💾 Salva referto"):
        ref_id = str(uuid.uuid4())
        img_path = f"training_data/{ref_id}.jpg"
        json_path = f"training_data/{ref_id}.json"

        img.save(img_path)

        with open(json_path, "w") as f:
            json.dump({
                "regione": distretto,
                "anomalie": risultati,
                "referto": referto
            }, f)

        st.success(f"Referto salvato correttamente con ID: {ref_id}")

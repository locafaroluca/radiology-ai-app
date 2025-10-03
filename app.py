import streamlit as st
import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torchvision.models as models
from PIL import Image
import os
import json
from datetime import datetime
import ssl

# Fix per errore certificato su Mac (solo locale)
ssl._create_default_https_context = ssl._create_unverified_context

# DISTRICTS SUPPORTED
DISTRICTS = ["Torace", "Cervello", "Addome", "Arti"]

# Label simulate per distretto
LABELS = {
    "Torace": [
        "Atelectasia", "Cardiomegalia", "Versamento pleurico", "Infiltrati", "Massa",
        "Polmonite", "Pneumotorace", "Consolidamento", "Edema"
    ],
    "Cervello": ["Ictus", "Emorragia", "Edema", "Tumore", "Idrocefalo"],
    "Addome": ["Appendicite", "Lesioni epatiche", "Calcoli", "Tumore", "Versamento"],
    "Arti": ["Frattura", "Osteoporosi", "Tumore osseo", "Artrite", "Infezione ossea"]
}

# Simulazione di predizione per distretti non polmonari
def mock_predict(district):
    import random
    findings = []
    for label in LABELS[district]:
        prob = round(random.uniform(0.1, 1.0), 2)
        if prob > 0.5:
            findings.append((label, prob))
    return findings

# Modello torace (CheXNet simulato)
class CheXNet(nn.Module):
    def __init__(self):
        super(CheXNet, self).__init__()
        self.model = models.densenet121(pretrained=True)
        num_ftrs = self.model.classifier.in_features
        self.model.classifier = nn.Linear(num_ftrs, len(LABELS["Torace"]))

    def forward(self, x):
        return self.model(x)

@st.cache_resource
def load_torace_model():
    model = CheXNet()
    model.eval()
    return model

def transform_image(img):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return transform(img).unsqueeze(0)

def generate_report(findings):
    if not findings:
        return "Nessuna anomalia significativa rilevata."
    else:
        return f"Possibili anomalie riscontrate: {', '.join([f'{label} ({prob:.2f})' for label, prob in findings])}. Si consiglia correlazione clinica."

# STREAMLIT INTERFACCIA
st.set_page_config(page_title="Radiology AI All-in-One", layout="centered")
st.title("🧠 Radiology AI – All-in-One")
st.markdown("Carica un'immagine radiologica, seleziona la regione anatomica, ottieni un referto AI.")

uploaded_file = st.file_uploader("📤 Carica immagine (JPG/PNG)", type=["jpg", "jpeg", "png"])
district = st.selectbox("📍 Seleziona distretto anatomico", DISTRICTS)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="🖼️ Immagine caricata", use_container_width=True)
    findings = []

    if district == "Torace":
        model = load_torace_model()
        img_tensor = transform_image(image)
        with torch.no_grad():
            probs = torch.sigmoid(model(img_tensor)).squeeze()
            for label, prob in zip(LABELS[district], probs):
                if prob.item() > 0.5:
                    findings.append((label, prob.item()))
    else:
        findings = mock_predict(district)

    st.subheader("🔬 Risultati")
    if findings:
        for label, prob in findings:
            st.markdown(f"- **{label}**: {prob:.2f}")
    else:
        st.info("✅ Nessuna anomalia rilevata con alta probabilità.")

    st.subheader("📝 Referto generato automaticamente")
    report = generate_report(findings)
    st.text_area("Referto", report, height=200)
    st.download_button("📄 Scarica referto", report, file_name="referto_AI.txt")

    # Salvataggio dati
    save_path = "training_data"
    os.makedirs(save_path, exist_ok=True)
    sample_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    metadata = {
        "id": sample_id,
        "district": district,
        "report": report,
        "labels": findings
    }
    with open(os.path.join(save_path, f"{sample_id}.json"), 'w') as f:
        json.dump(metadata, f)
    image.save(os.path.join(save_path, f"{sample_id}.jpg"))
    st.success("✅ Dati salvati per miglioramento futuro del modello.")

import streamlit as st
import os
import json
from PIL import Image

st.set_page_config(page_title="Referti", page_icon="📁")

st.title("📁 Referti salvati")

FOLDER = "training_data"

if not os.path.exists(FOLDER):
    st.info("Nessun referto trovato.")
else:
    referti = [f for f in os.listdir(FOLDER) if f.endswith(".json")]
    if not referti:
        st.info("Ancora nessun referto salvato.")
    else:
        for json_file in sorted(referti, reverse=True):
            base = json_file.replace(".json", "")
            img_path = os.path.join(FOLDER, f"{base}.jpg")
            json_path = os.path.join(FOLDER, json_file)

            with open(json_path, "r") as f:
                data = json.load(f)

            st.subheader(f"📝 Referto: {base}")
            st.write("**Regione:**", data.get("regione", "N/A"))
            st.write("**Anomalie rilevate:**", data.get("anomalie", "Nessuna"))
            st.write("**Referto AI:**", data.get("referto", "N/A"))

            if os.path.exists(img_path):
                st.image(Image.open(img_path), caption=base, use_column_width=True)

            st.markdown("---")
          aggiunto file pagina Referti

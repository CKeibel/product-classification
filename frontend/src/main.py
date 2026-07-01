import os

import requests
import streamlit as st
from loguru import logger
from src.settings import settings

st.set_page_config(page_title="Product Search", layout="wide")

st.title("Produkt-Klassifikation")
st.write("Lade ein Bild hoch, um ähnliche Produkte in der Qdrant-Datenbank zu finden.")

with st.sidebar:
    st.header("⚙️ Einstellungen")
    limit = st.slider(
        "Anzahl der Ergebnisse (Limit)", min_value=1, max_value=50, value=5
    )

upload_col, results_col = st.columns([1, 2])

with upload_col:
    st.subheader("📸 Suchanfrage")
    uploaded_file = st.file_uploader(
        "Wähle ein Produktbild...", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        st.image(
            uploaded_file, caption="Dein hochgeladenes Bild", use_container_width=True
        )

with results_col:
    st.subheader("🎯 Ähnliche Produkte")

    if uploaded_file is not None:
        if st.button("Suche starten", type="primary"):
            with st.spinner("Extrahiere Features und durchsuche Vektor-Datenbank..."):
                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    }
                    data = {"limit": limit}

                    response = requests.post(
                        f"{settings.backend_url}/embed-image", files=files, data=data
                    )

                    if response.status_code == 200:
                        hits = response.json()

                        if not hits:
                            st.info(
                                "Keine passenden Produkte in der Datenbank gefunden."
                            )
                        else:
                            st.success(f"{len(hits)} Treffer erzielt!")

                            grid_cols = st.columns(3)
                            for idx, hit in enumerate(hits):
                                col = grid_cols[idx % 3]
                                with col:
                                    with st.container(border=True):
                                        product_name = hit.get("name", "-")
                                        score = hit.get("score", 0.0)
                                        description = hit.get("description", "-")
                                        file_name = hit.get("image_path")

                                        local_image_path = os.path.join(
                                            settings.image_dir, file_name
                                        )
                                        logger.debug(f"Image path: {local_image_path}")

                                        if os.path.exists(local_image_path):
                                            st.image(
                                                local_image_path,
                                                use_container_width=True,
                                            )
                                        else:
                                            st.warning(
                                                f"Bild nicht im Volume: {product_name}"
                                            )

                                        st.write(f"**Score:** `{score:.4f}`")
                                        st.caption(product_name)
                                        st.caption(description)
                    else:
                        st.error(
                            f"Backend Error ({response.status_code}): {response.text}"
                        )

                except Exception as e:
                    st.error(f"Backend connetion failed: {e}")
    else:
        st.info("Upload an Image.")

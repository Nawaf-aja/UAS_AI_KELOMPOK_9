import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import streamlit as st

from src.predict import predict_topic


st.set_page_config(page_title="AI Keluhan Perbankan", page_icon="AI", layout="wide")

st.title("AI Klasifikasi Keluhan Pelanggan Perbankan")
st.write(
    "Pipeline NLP ini mengubah keluhan menjadi fitur TF-IDF, lalu membandingkan "
    "Naive Bayes dan Logistic Regression untuk memilih topik keluhan. Setelah itu "
    "sistem memberi rekomendasi penanganan berbasis aturan."
)

model = st.selectbox(
    "Model",
    ["Model terbaik otomatis", "naive_bayes", "logistic_regression"],
)
text = st.text_area(
    "Teks keluhan",
    "Transfer BI Fast gagal tetapi saldo saya terpotong dan penerima belum menerima dana.",
    height=160,
)

if st.button("Prediksi Topik", type="primary"):
    with st.spinner("Memproses keluhan..."):
        selected = None if model == "Model terbaik otomatis" else model
        result = predict_topic(text, selected)
    if result["status"] == 200:
        col1, col2, col3 = st.columns(3)
        col1.metric("Prediksi", result["prediction"])
        col2.metric("Confidence", f"{result['confidence'] * 100:.1f}%")
        col3.metric("Model", result["model"])
        st.subheader("Rekomendasi Penanganan")
        recommendation = result["recommendation"]
        rec1, rec2, rec3 = st.columns(3)
        rec1.metric("Prioritas", recommendation["priority"])
        rec2.metric("Divisi Tujuan", recommendation["target_unit"])
        rec3.metric("SLA", recommendation["sla"])
        st.write(recommendation["summary"])
        st.write(recommendation["confidence_note"])
        st.write("Langkah awal:")
        for action in recommendation["actions"]:
            st.write(f"- {action}")
        st.subheader("Top 3 Prediksi")
        st.dataframe(result["top_predictions"], use_container_width=True)
        st.subheader("Response JSON")
        st.json(result)
    else:
        st.error(result["error"])

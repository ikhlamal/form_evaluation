import streamlit as st
import pandas as pd

st.set_page_config(page_title="Annotasi Augmentasi Jawa & Sunda", layout="wide")

# CSS styling
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 400px;
            max-width: 400px;
        }
        .augment-box {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 8px;
            background-color: #f9f9f9;
            margin-bottom: 10px;
            color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load CSV
df = pd.read_csv("form_eval.csv")

# Tempat simpan anotasi
if "annotations" not in st.session_state:
    st.session_state.annotations = []

# Ambil contoh pertama (nanti bisa diganti loop per contoh)
contoh = df.iloc[0]

# Sidebar: tampilkan kalimat asli + task
st.sidebar.title("Kalimat Asli (Human)")
st.sidebar.markdown(f"<div class='augment-box'>{contoh['Kalimat Asli']}</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Task: {contoh['Instruksi']}**")
st.sidebar.write(f"Kalimat-kalimat berikut ini dihasilkan menggunakan teknik {contoh['Instruksi'].lower()}.")

# Filter semua augmentasi yg sama-sama dari kalimat asli itu
augmentasi_list = df[df["Kalimat Asli"] == contoh["Kalimat Asli"]]

for i, row in augmentasi_list.iterrows():
    with st.container():
        st.markdown("---")

        # Kotak kalimat augmentasi
        st.markdown(f"<div class='augment-box'>{row['Kalimat Augmentasi']}</div>", unsafe_allow_html=True)

        # Slider dinamis (pakai mapping sesuai instruksi)
        task_descriptions = {
            "Paraphrasing": ("Tidak parafrasa sama sekali", "Hasil parafrase sangat bagus"),
            "Back Translation": ("Bukan hasil terjemahan balik", "Hasil terjemahan balik sangat bagus"),
            "Synonym Replacement": ("Tidak ada sinonim diganti", "Penggantian sinonim sangat bagus"),
            "Noise Injection": ("Tidak ada noise sama sekali", "Penyisipan noise sangat bagus"),
        }
        low_desc, high_desc = task_descriptions.get(row["Instruksi"], ("Tidak sesuai", "Sangat bagus"))

        kesesuaian = st.slider(
            f"Kesesuaian dengan Instruksi (1 = {low_desc}, 5 = {high_desc})",
            1, 5, 1,
            key=f"task_{i}"
        )

        koheren = st.slider(
            "Koherensi (1 = Tidak koheren, 5 = Sangat koheren)",
            1, 5, 1,
            key=f"koheren_{i}"
        )

        kohesi = st.slider(
            "Kohesi (1 = Tidak kohesif, 5 = Sangat kohesif)",
            1, 5, 1,
            key=f"kohesi_{i}"
        )

        natural = st.radio(
            "Text Naturalness",
            [
                "Teks terdengar natural",
                "Teks terdengar janggal tapi masih bisa dipahami",
                "Teks tidak bisa dipahami"
            ],
            index=1,
            key=f"natural_{i}",
            horizontal=True
        )

        if st.button("Simpan Anotasi", key=f"save_{i}"):
            st.session_state.annotations.append({
                "Kalimat Asli": row["Kalimat Asli"],
                "Kalimat Augmentasi": row["Kalimat Augmentasi"],
                "Model": row["Model"],
                "Instruksi": row["Instruksi"],
                "Bahasa": row["Bahasa"],
                "Sesuai Instruksi": kesesuaian,
                "Koheren": koheren,
                "Kohesi": kohesi,
                "Natural": natural
            })
            st.success("Anotasi berhasil disimpan!")

# Tampilkan hasil anotasi sementara
if st.session_state.annotations:
    st.markdown("### Hasil Anotasi Sementara")
    hasil = pd.DataFrame(st.session_state.annotations)
    st.dataframe(hasil)

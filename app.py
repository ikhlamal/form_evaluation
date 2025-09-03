import streamlit as st
import pandas as pd

st.set_page_config(page_title="Annotasi Augmentasi Jawa & Sunda", layout="wide")

# CSS
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

# Kelompokkan per kalimat asli
grouped = df.groupby("Kalimat Asli")

# Init session state
if "annotations" not in st.session_state:
    st.session_state.annotations = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# Ambil kalimat asli aktif
kalimat_list = list(grouped.groups.keys())
current_asli = kalimat_list[st.session_state.current_index]
subset = grouped.get_group(current_asli)

# Sidebar
contoh = subset.iloc[0]  # ambil salah satu baris utk meta info
st.sidebar.title("Kalimat Asli (Human)")
st.sidebar.markdown(f"<div class='augment-box'>{contoh['Kalimat Asli']}</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Task: {contoh['Instruksi']}**")
if "Instruksi Lengkap" in contoh:
    st.sidebar.write(contoh["Instruksi Lengkap"])

# Navigasi
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("⬅️ Previous", disabled=st.session_state.current_index == 0):
        st.session_state.current_index -= 1
        st.experimental_rerun()
with col3:
    if st.button("Next ➡️", disabled=st.session_state.current_index == len(kalimat_list) - 1):
        st.session_state.current_index += 1
        st.experimental_rerun()

# Loop setiap augmentasi
for i, row in subset.iterrows():
    with st.container():
        st.markdown("---")
        st.markdown(f"<div class='augment-box'>{row['Kalimat Augmentasi']}</div>", unsafe_allow_html=True)

        # Deskripsi skala sesuai instruksi
        task_descriptions = {
            "Paraphrasing": ("Tidak parafrasa sama sekali", "Hasil parafrase sangat bagus"),
            "Aggressive Transformation": ("Tidak ada perubahan konteks/topik", "Transformasi agresif sangat bagus"),
            "Back Translation": ("Bukan hasil terjemahan balik", "Hasil terjemahan balik sangat bagus"),
            "Synonym Replacement": ("Tidak ada sinonim diganti", "Penggantian sinonim sangat bagus"),
            "Noise Injection": ("Tidak ada noise sama sekali", "Penyisipan noise sangat bagus"),
        }
        low_desc, high_desc = task_descriptions.get(row["Instruksi"], ("Tidak sesuai", "Sangat bagus"))

        sesuai = st.slider(
            f"Kesesuaian dengan Instruksi (1 = {low_desc}, 5 = {high_desc})",
            1, 5, 1, key=f"task_{i}"
        )
        koheren = st.slider(
            "Koherensi (1 = Tidak koheren, 5 = Sangat koheren)",
            1, 5, 1, key=f"koheren_{i}"
        )
        kohesi = st.slider(
            "Kohesi (1 = Tidak kohesif, 5 = Sangat kohesif)",
            1, 5, 1, key=f"kohesi_{i}"
        )
        natural = st.radio(
            "Text Naturalness",
            ["Teks terdengar natural",
             "Teks terdengar janggal tapi masih bisa dipahami",
             "Teks tidak bisa dipahami"],
            index=1, key=f"natural_{i}", horizontal=True
        )

        if st.button("Simpan Anotasi", key=f"save_{i}"):
            st.session_state.annotations.append({
                "Kalimat Asli": row["Kalimat Asli"],
                "Kalimat Augmentasi": row["Kalimat Augmentasi"],
                "Model": row["Model"],
                "Instruksi": row["Instruksi"],
                "Instruksi Lengkap": row["Instruksi Lengkap"],
                "Bahasa": row["Bahasa"],
                "Sesuai Instruksi": sesuai,
                "Koheren": koheren,
                "Kohesi": kohesi,
                "Natural": natural
            })
            st.success("Anotasi berhasil disimpan!")

# Hasil sementara
if st.session_state.annotations:
    st.markdown("### Hasil Anotasi Sementara")
    hasil = pd.DataFrame(st.session_state.annotations)
    st.dataframe(hasil)

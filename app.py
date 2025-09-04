import streamlit as st
import pandas as pd

st.set_page_config(page_title="Evaluasi Augmentasi Jawa & Sunda", layout="wide")

# ==== CSS styling ====
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

# ==== LOAD CSV ====
df = pd.read_csv("data.csv")

# ==== GROUP DATA: per (Kalimat Asli + Instruksi) ====
grouped = df.groupby(["Kalimat Asli", "Instruksi"])
paket_list = list(grouped.groups.keys())

# ==== SESSION STATE ====
if "annotations" not in st.session_state:
    st.session_state.annotations = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

# ==== FUNGSI NAVIGASI ====
def prev_example():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

def next_example():
    if st.session_state.current_index < len(paket_list) - 1:
        st.session_state.current_index += 1

# ==== AMBIL DATA SEKARANG ====
current_paket = paket_list[st.session_state.current_index]
subset = grouped.get_group(current_paket)
contoh = subset.iloc[0]  # ambil 1 baris utk info sidebar

# ==== SIDEBAR ====
st.sidebar.title("Kalimat Asli")
st.sidebar.markdown(f"<div class='augment-box'>{contoh['Kalimat Asli']}</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Label: {contoh['Label']}**")
st.sidebar.markdown(f"**Instruksi: {contoh['Instruksi']}**")
if "Instruksi Lengkap" in contoh:
    st.sidebar.write(contoh["Instruksi Lengkap"])

# ==== NAVIGASI ====
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    st.button("⬅️ Previous", on_click=prev_example, disabled=st.session_state.current_index == 0)
with col2:
    st.markdown(
        f"<div style='text-align:center; font-weight:bold;'>Sampel {st.session_state.current_index+1} dari {len(paket_list)}</div>",
        unsafe_allow_html=True
    )
with col3:
    st.button("Next ➡️", on_click=next_example, disabled=st.session_state.current_index == len(paket_list)-1)

# ==== TAMPILKAN AUGMENTASI DALAM 1 PAKET ====
for i, row in subset.iterrows():
    with st.container():
        st.markdown(f"<div class='augment-box'>{row['Kalimat Augmentasi']}</div>", unsafe_allow_html=True)

        # Deskripsi skala dinamis sesuai instruksi
        task_descriptions = {
            "Paraphrasing": ("Hasil parafrase sangat buruk", "Hasil parafrase sangat bagus"),
            "Aggressive Transformation": ("Perubahan konteks/topik sangat buruk", "Perubahan konteks/topik sangat bagus"),
            "Sentiment Based": ("Perubahan emosi sangat buruk", "Perubahan emosi sangat bagus"),
            "Perturbation and Noise Injection": ("Perturbasi dan penyisipan noise sangat buruk", "Perturbasi dan penyisipan noise sangat bagus"),
        }
        low_desc, high_desc = task_descriptions.get(row["Instruksi"], ("Tidak sesuai", "Sangat bagus"))

        sesuai = st.slider(
            f"Kesesuaian dengan Instruksi (1 = {low_desc}, 5 = {high_desc})",
            1, 5, 1, key=f"task_{st.session_state.current_index}_{i}"
        )
        koheren = st.slider(
            "Koherensi (1 = Tidak koheren, 5 = Sangat koheren)",
            1, 5, 1, key=f"koheren_{st.session_state.current_index}_{i}"
        )
        kohesi = st.slider(
            "Kohesi (1 = Tidak kohesif, 5 = Sangat kohesif)",
            1, 5, 1, key=f"kohesi_{st.session_state.current_index}_{i}"
        )
        natural = st.radio(
            "Naturalness",
            [
                "Teks terdengar natural",
                "Teks terdengar janggal tapi masih bisa dipahami",
                "Teks tidak bisa dipahami"
            ],
            index=1,
            key=f"natural_{st.session_state.current_index}_{i}",
            horizontal=True
        )

        if st.button("💾 Simpan Anotasi", key=f"save_{st.session_state.current_index}_{i}"):
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
            st.success("✅ Anotasi berhasil disimpan!")
        st.markdown("---")

# ==== TAMPILKAN HASIL ANOTASI ====
if st.session_state.annotations:
    st.markdown("### Hasil Anotasi Sementara")
    hasil = pd.DataFrame(st.session_state.annotations)
    st.dataframe(hasil)

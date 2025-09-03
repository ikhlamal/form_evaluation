import streamlit as st
import pandas as pd

st.set_page_config(page_title="Annotasi Augmentasi Jawa & Sunda", layout="wide")

st.title("Annotasi Kalimat Augmentasi")

# Contoh data
data = {
    "Kalimat Asli": "USER Menyetabilkan harga beras aja gak becus kok jadi penguasa cok jancok.munduro cok kamu jadi presiden dasar gak punya malu raimu cok",
    "Augmentasi": [
        "Ngatur harga beras wae ora iso, kok isih ngaku penguasa, cok jancok. Ojo sok presiden, munduro saiki, dasar ra nduwe isin, raimu cok.",
        "Ngatur harga beras wae ora iso kok malah dadi pemimpin cok jancok, mundur wae cok dadi presiden ora nduwe isin raimu cok",
        "Ngurusi rego beras wae ora iso, kok malah dadi penguasa cok. Minggato cok, dhasar rai gedek, dadi presiden ora isin."
    ]
}

# Tempat simpan hasil anotasi
if "annotations" not in st.session_state:
    st.session_state.annotations = []

# Sidebar untuk sticky kalimat asli
st.sidebar.title("Kalimat Asli (Human)")
st.sidebar.write(data["Kalimat Asli"])

st.markdown("### Anotasi Kalimat Augmentasi")

# Loop setiap kalimat augmentasi
for i, kalimat in enumerate(data["Augmentasi"], start=1):
    with st.container():
        st.markdown("---")  # Border pemisah

        st.markdown(f"#### Kalimat Augmentasi {i}")
        st.write(kalimat)

        st.markdown("**Kesuaian Task (1 = Tidak sesuai sama sekali, 5 = Sangat sesuai)**")
        kesesuaian = st.slider(f"Kesuaian Task - Kalimat {i}", 1, 5, 1, key=f"task_{i}")

        st.markdown("**Koheren (1 = Tidak koheren, 5 = Sangat koheren)**")
        koheren = st.slider(f"Koheren - Kalimat {i}", 1, 5, 1, key=f"koheren_{i}")

        st.markdown("**Kohesi (1 = Tidak kohesif, 5 = Sangat kohesif)**")
        kohesi = st.slider(f"Kohesi - Kalimat {i}", 1, 5, 1, key=f"kohesi_{i}")

        st.markdown("**Naturalness**")
        natural = st.radio(
            f"Naturalness - Kalimat {i}",
            ["The text sounds natural", "The text sounds awkward but understandable", "The text is not understandable"],
            index=1,
            key=f"natural_{i}"
        )

        if st.button(f"Simpan Anotasi Kalimat {i}", key=f"save_{i}"):
            st.session_state.annotations.append({
                "Kalimat Asli": data["Kalimat Asli"],
                "Kalimat Augmentasi": kalimat,
                "Kesuaian Task": kesesuaian,
                "Koheren": koheren,
                "Kohesi": kohesi,
                "Naturalness": natural
            })
            st.success(f"Anotasi untuk Kalimat {i} berhasil disimpan!")

# Tampilkan hasil anotasi sementara
if st.session_state.annotations:
    st.markdown("### Hasil Anotasi Sementara")
    df = pd.DataFrame(st.session_state.annotations)
    st.dataframe(df)

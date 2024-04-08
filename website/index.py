import streamlit as st
import subprocess

# Judul aplikasi
st.title('Aplikasi Streamlit Sederhana')

# Tombol "Realtime"
if st.button('Realtime'):
    subprocess.Popen(["python", "realtime.py"])

# Tombol "Upload"
if st.button('Upload'):
    uploaded_file = st.file_uploader("Pilih file CSV", type=['csv'])
    if uploaded_file is not None:
        st.write('File berhasil diupload')

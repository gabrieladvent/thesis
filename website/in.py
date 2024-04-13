import streamlit as st


st.title('Object Detection using YOLOv8')
st.write("Realtime")

video_file = open('tempvid.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)
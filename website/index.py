from PIL import Image
import streamlit as st
from streamlit_webrtc import webrtc_streamer

from proses.upload import image_classify, video_classify, draw_boxes
    
def main():
    st.title('Object Detection using YOLOv8')
    
    st.write("Realtime")
    webrtc_streamer(key="example")
    
    html_temp_about1= """<br>"""
    st.markdown(html_temp_about1, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Silahkan Upload Foto atau Video", type=["jpg", "jpeg", "png", "mp4"])
    
    if uploaded_file is not None:
        image_file = Image.open(uploaded_file)
        detections, labels = image_classify(image_file)
        for i, detection in enumerate(detections):
            image_with_boxes = draw_boxes(image_file, detection, labels)
            st.image(image_with_boxes)
            st.write('Objek Yang Terdeteksi:')
            unique_labels = set(labels)
            for i, label in enumerate(unique_labels, start=1):
                st.write("### {}. {}".format(i, label))

if __name__ == '__main__':
    main()
from PIL import Image
import streamlit as st
from streamlit_webrtc import webrtc_streamer
from moviepy.editor import VideoFileClip
import os
import io
from tempfile import NamedTemporaryFile
import tempfile

from proses.upload import image_classify, video_classify, draw_boxes, create_video
    
def main():
    st.title('Object Detection using YOLOv8')
    
    st.write("Realtime")
    webrtc_streamer(key="example")
    
    html_temp_about1= """<br>"""
    st.markdown(html_temp_about1, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Silahkan Upload Foto atau Video", type=["jpg", "jpeg", "png", "mp4"])
    
    if uploaded_file is not None:
        # ambil ekstensi file
        file_name = uploaded_file.name
        ekstensi = os.path.splitext(file_name)[1]
        
        #menentukan file foto atau video
        if ekstensi in ['.jpg', '.jpeg', '.png']:
            image_file = Image.open(uploaded_file)
            detections, labels = image_classify(image_file)
            for i, detection in enumerate(detections):
                image_with_boxes = draw_boxes(image_file, detection, labels)
                st.image(image_with_boxes)
                if len(labels) > 0:
                    st.write('Objek Yang Terdeteksi:')
                    unique_labels = set(labels)
                    for i, label in enumerate(unique_labels, start=1):
                        st.success("### {}. {}".format(i, label))
                else:
                    st.warning("### {}".format("Tidak Ada Objek Yang Terdeteksi"))
                    
        elif ekstensi in ['.mp4', '.avi', '.mov']:
            with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                temp_file.write(uploaded_file.read())
                temp_video_path = temp_file.name

            frames = video_classify(temp_video_path)
            output_path = create_video(frames)
            st.video(output_path)       


if __name__ == '__main__':
    main()
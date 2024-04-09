from PIL import Image
import streamlit as st
from streamlit_webrtc import webrtc_streamer


from proses.upload import image_classify, video_classify, draw_boxes, set_background

# set_background('bg5.png')
    
def main():
    st.title("Object Detection")
    
    activiteis = ["Home", "Realtime Detection","Upload Foto / Video", "Petunjuk"]
    choice = st.sidebar.selectbox("Select Activity", activiteis)
    
    st.sidebar.markdown(
        """ Gabriel Advent Batan """
    )
    
    if choice == "Home":
        st.write("""
                 The application has two functionalities.

                 1. Real time face detection using web cam feed.

                 2. Real time face emotion recognization.

                 """)
        
    elif choice == "Realtime Detection":
        st.header("Realtime Detection")
        st.write("Click on start to use webcam and detect your face emotion")
        webrtc_streamer(key="sample")
    
    elif choice == "Upload Foto / Video":
        st.header("Uplod File")
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

    elif choice == "About":
        st.subheader("About this app")
        html_temp_about1= """<div style="background-color:#6D7B8D;padding:10px">
                                    <h4 style="color:white;text-align:center;">
                                    Real time face emotion detection application using OpenCV, Custom Trained CNN model and Streamlit.</h4>
                                    </div>
                                    </br>"""
        st.markdown(html_temp_about1, unsafe_allow_html=True)

        html_temp4 = """
                             		<div style="background-color:#98AFC7;padding:10px">
                             		<h4 style="color:white;text-align:center;">This Application is developed by Mohammad Juned Khan using Streamlit Framework, Opencv, Tensorflow and Keras library for demonstration purpose. If you're on LinkedIn and want to connect, just click on the link in sidebar and shoot me a request. If you have any suggestion or wnat to comment just write a mail at Mohammad.juned.z.khan@gmail.com. </h4>
                             		<h4 style="color:white;text-align:center;">Thanks for Visiting</h4>
                             		</div>
                             		<br></br>
                             		<br></br>"""

        st.markdown(html_temp4, unsafe_allow_html=True)

    else:
        pass


if __name__ == "__main__":
    main()
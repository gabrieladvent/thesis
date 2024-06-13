from ultralytics import YOLO
import time
import streamlit as st
import cv2
import av
from pytube import YouTube
from tempfile import NamedTemporaryFile

from streamlit_webrtc import (
    VideoTransformerBase,
    webrtc_streamer,
    WebRtcMode,
    VideoProcessorFactory,
)

import settings
import turn


def load_model(model_path):
    """
    Load a pre-trained YOLOv8 model from the given model path.

    Args:
        model_path (str): Path to the pre-trained model file.

    Returns:
        YOLO: The loaded YOLOv8 model.

    """
    model = YOLO(model_path)
    return model


def showDetectFrame(
    conf, model, st_frame, image, is_display_tracking=None, tracker=None
):
    """
    Show the detection results on a video frame.

    Args:
        conf (float): Confidence threshold for object detection.
        model (YOLO): The YOLOv8 model for object detection.
        st_frame (streamlit.empty): The Streamlit container for displaying the frame.
        image (numpy.ndarray): The video frame.
        is_display_tracking (bool, optional): Whether to display tracking results. Defaults to None.
        tracker (object, optional): The object tracker. Defaults to None.
    """

    res = model.predict(image, conf=conf)
    res_plotted = res[0].plot()

    st_frame.image(
        res_plotted,
        caption="Detected Video",
        channels="BGR",
    )


def play_youtube(conf, model):
    """
    Play YouTube video with object detection.

    Args:
        conf (float): Confidence threshold for object detection.
        model (YOLO): The YOLOv8 model for object detection.

    """
    # Input YouTube link
    source_youtube = st.text_input("Silahkan Masukan Link YouTube")

    # Check if button is clicked
    if st.button("Deteksi"):
        try:
            # Get YouTube video stream
            yt = YouTube(source_youtube)
            stream = yt.streams.filter(file_extension="mp4", res=720).first()
            vid_cap = cv2.VideoCapture(stream.url)

            # Stream video frame by frame and show detection results
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    showDetectFrame(conf, model, st_frame, image)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            # Show error message if there is an exception
            st.error("Ada Kesalahan Saat Memproses Link: " + str(e))


def play_webcam(conf, model):
    """
    Play webcam video with object detection.

    Args:
        conf (float): Confidence threshold for object detection.
        model (YOLO): The YOLOv8 model for object detection.

    """
    # Set the path to the webcam
    source_webcam = settings.WEBCAM_PATH

    # Check if button is clicked
    if st.button("Deteksi Secara Langsung"):
        try:
            # Open the webcam video stream
            vid_cap = cv2.VideoCapture(source_webcam)

            # Create an empty Streamlit frame to display the video
            st_frame = st.empty()

            # Create a button to stop the video stream
            stop_button = st.button("Berhenti")

            # Continuously read frames from the video stream until the video ends or the stop button is clicked
            while vid_cap.isOpened() and not stop_button:
                success, image = vid_cap.read()
                if success:
                    # Show detection results on each frame
                    showDetectFrame(conf, model, st_frame, image)
                else:
                    # Release the video stream and break the loop if the video ends
                    vid_cap.release()
                    break
        except Exception as e:
            # Show error message if there is an exception
            st.error("Ada Kesalahan Saat Proses Deteksi: " + str(e))
            st.error("Ada Kesalahan Saat Proses Deteksi: " + str(e))


class VideoTransformer(VideoTransformerBase):
    def __init__(self, model, conf):
        self.model = model
        self.conf = conf

    def transform(self, frame):
        """
        Transform a frame using the YOLOv8 model for object detection.

        Args:
            frame (streamlit.VideoFrame): The video frame to be transformed.

        Returns:
            numpy.ndarray: The transformed frame with detection results.
        """
        # Convert the frame to an ndarray in BGR format
        img = frame.to_ndarray(format="bgr24")

        # Perform object detection on the frame and get the plotted results
        res = self.model.predict(img, show=False, conf=self.conf)
        res_plotted = res[0].plot()

        # Return the transformed frame
        return res_plotted


def live(conf, model):
    """
    Stream live video and perform object detection using the YOLOv8 model.

    Args:
        conf (float): The confidence threshold for object detection.
        model (ultralytics.YOLO): The YOLOv8 model for object detection.

    Returns:
        None
    """
    # Create a WebRTC streamer with the specified configuration
    webrtc_ctx = webrtc_streamer(
        key="object-detection",  # Unique key for the streamer
        mode=WebRtcMode.SENDRECV,  # Mode for WebRTC communication
        rtc_configuration={  # Configuration for WebRTC
            "iceServers": turn.get_ice_servers(),  # ICE servers for WebRTC
            "iceTransportPolicy": "relay",  # ICE transport policy for WebRTC
        },
        video_transformer_factory=lambda: VideoTransformer(model, conf),  # Factory function for creating the video transformer
        media_stream_constraints={"video": True, "audio": False},  # Constraints for the media stream
        async_processing=True,  # Enable asynchronous processing
        video_processor_factory=lambda: VideoProcessorFactory(fps=60),  # Factory function for creating the video processor
    )


def process_uploaded_video(conf, model):
    """
    Process an uploaded video file by performing object detection on each frame and displaying the results.

    Args:
        conf (float): The confidence threshold for object detection.
        model (ultralytics.YOLO): The YOLOv8 model for object detection.

    Returns:
        None
    """
    # Prompt the user to upload a video file
    uploaded_video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

    if uploaded_video is not None:
        # Save the uploaded video to a temporary file
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(uploaded_video.read())
            temp_video_path = temp_file.name

        # Read the video file and display it
        with open(temp_video_path, "rb") as video_file:
            video_bytes = video_file.read()
        if video_bytes:
            st.video(video_bytes)

        # If the "Deteksi" button is clicked, perform object detection on each frame of the video
        if st.button("Deteksi"):
            try:
                # Open the video file
                vid_cap = cv2.VideoCapture(temp_video_path)

                # Create an empty Streamlit frame to display the video
                st_frame = st.empty()

                # Read frames from the video file and show detection results
                while vid_cap.isOpened():
                    success, image = vid_cap.read()
                    if success:
                        showDetectFrame(conf, model, st_frame, image)
                    else:
                        # Release the video stream and break the loop if the video ends
                        vid_cap.release()
                        break
            except Exception as e:
                # Show error message if there is an exception
                st.error("Error loading video: " + str(e))


def play_stored_video(conf, model):
    """
    Plays a stored video with object detection and displays the detection results.

    Args:
        conf (float): Confidence threshold for object detection.
        model (YOLO): The YOLOv8 model for object detection.

    """

    # Select the video from the list of provided videos
    source_vid = st.selectbox(
        "Silahkan Pilih Video yang Sudah Disediakan", settings.VIDEOS_DICT.keys()
    )

    # Read the video file and display it
    with open(settings.VIDEOS_DICT.get(source_vid), "rb") as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)

    # If the "Deteksi Video" button is clicked, perform object detection on the video
    if st.button("Deteksi Video"):
        try:
            # Open the video file
            vid_cap = cv2.VideoCapture(str(settings.VIDEOS_DICT.get(source_vid)))
            st_frame = st.empty()  # Empty Streamlit container for displaying the frame

            # Read frames from the video file and show detection results
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    showDetectFrame(conf, model, st_frame, image)
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            # Show error message if there is an exception
            st.error("Ada Kesalahan Saat Proses Video: " + str(e))


def take_picture(conf, model):
    """
    Takes a picture with object detection and displays the detection results.

    Args:
        conf (float): Confidence threshold for object detection.
        model (YOLO): The YOLOv8 model for object detection.

    """
    # Input for the camera
    picture = st.camera_input("Silahkan Mengambil Gambar")

    if picture:
        # Save the picture to a temporary file
        with NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            temp_file.write(picture.read())
            temp_pict_path = temp_file.name

        # Check if button is clicked
        if st.button("Deteksi Foto"):
            try:
                # Open the temporary video file
                vid_cap = cv2.VideoCapture(temp_pict_path)
                st_frame = st.empty()
                # Read frames from the video file and show detection results
                while vid_cap.isOpened():
                    success, image = vid_cap.read()
                    if success:
                        showDetectFrame(conf, model, st_frame, image)
                    else:
                        vid_cap.release()
                        break
            except Exception as e:
                # Show error message if there is an exception
                st.error("Error loading video: " + str(e))


def helpFunction():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(" ")
    with col2:
        st.image(str(settings.IMAGE_HELP))
    with col3:
        st.write(" ")

    html_temp_about1 = """
                <div style="padding:10px; text-align:center;">
                        <h2>
                            DETEKSI OBJEK
                        </h2>
                    </div>
                    """
    st.markdown(html_temp_about1, unsafe_allow_html=True)

    html_temp4 = """
                <div style="padding:10px">
                    <p>
                        Website ini adalah hasil dari penelitian saya tentang <strong>"Pengengalan Objek Untuk Pembelajaran Anak-Anak"</strong>.
                    </p>
                    <p>
                        Website ini dibuat dengan bantuan sebuah alat bernama <a rel="noopener" href="https://streamlit.io" target="_blank">Streamlit</a>. Saya juga menggunakan teknologi <a rel="noopener" href="https://docs.ultralytics.com" target="_blank">You Only Look Once</a> (YOLO) versi 8 dari <a rel="noopener" href="https://www.ultralytics.com" target="_blank">Ultralytics</a> untuk mengembangkan modelnya.
                    </p>
                    <p>
                        Dalam penelitian ini, ada 6 benda yang bisa kita kenali, yaitu: <strong>Handphone, Jam, Mobil, Orang, Sepatu,</strong> dan <strong>Tas</strong>. Website ini memiliki 4 cara untuk mengenal benda, yaitu: <strong>mengupload foto</strong>, <strong>mengupload video</strong>, <strong>menyalin link YouTube</strong>, dan <strong>deteksi langsung</strong>.
                    </p>
                    <p>
                        Saya berharap website ini dapat membantu teman-teman, terutama anak-anak usia 3 - 5 tahun, untuk lebih cepat mengenal benda-benda di sekitarnya.
                    </p>
                    <p>
                        Setelah mencoba website ini, tolong isi <a rel="noopener" href="https://forms.gle/k4ULtjY2ShkAegtm8" target="_blank">kuesioner</a> untuk memberikan masukan kepada saya.
                    </p>
                    <p>
                        Jika ada yang ingin ditanyakan, silakan hubungi saya via <a rel="noopener" href="mailto:bie.ritan112@gmail.com">Email</a>.
                    </p>
                    <p>
                        Terima kasih dan Semoga Menyenangkan!
                    </p>

                </div>
                
                <br>
                
                <div>
                    <p>
                        Tambahan:
                    </p>
                    <p>
                        Mungkin pada saat mencoba mode deteksi video, youtube, dan realtime, hasilnya akan sedikit patah-patah dikarenakan proses berat yang sedang dilakukan. Mohon dimaklumi :)
                    </p>
                </div>
                """

    st.markdown(html_temp4, unsafe_allow_html=True)

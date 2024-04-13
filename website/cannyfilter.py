import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer


class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.threshold1 = 100
        self.threshold2 = 200

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = cv2.cvtColor(
            cv2.Canny(img, self.threshold1, self.threshold2), cv2.COLOR_GRAY2BGR
        )

        return img


ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

if ctx.video_transformer:
    ctx.video_transformer.threshold1 = st.slider("Threshold1", 0, 1000, 100)
    ctx.video_transformer.threshold2 = st.slider("Threshold2", 0, 1000, 200)
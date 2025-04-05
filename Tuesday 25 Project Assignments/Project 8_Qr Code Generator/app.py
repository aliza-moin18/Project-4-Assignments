import streamlit as st
import qrcode
from PIL import Image
import cv2
import numpy as np
import tempfile
import os
import io

st.set_page_config(page_title="QR Code Encoder & Decoder", layout="centered")

st.title("📷 QR Code Encoder / Decoder")

menu = st.sidebar.radio("Choose an Option", ["Encode (Generate QR Code)", "Decode (Read QR Code)"])

# ------------------ QR CODE ENCODER ------------------
if menu == "Encode (Generate QR Code)":
    st.header("🔐 QR Code Encoder")

    data = st.text_input("Enter text or Url to generate QR code:")

    if st.button("Generate QR Code"):
        if data:
            # Generate QR Code
            img = qrcode.make(data)

            # Convert to bytes for Streamlit
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            byte_img = buf.getvalue()

            # Show QR
            st.image(byte_img, caption="Your QR Code", use_container_width=True)

            # Save file for download
            with open("my_qrcode.png", "wb") as f:
                f.write(byte_img)

            # Download button
            with open("my_qrcode.png", "rb") as file:
                st.download_button(
                    label="⬇️ Download QR Code",
                    data=file,
                    file_name="my_qrcode.png",
                    mime="image/png"
                )
        else:
            st.warning("Please enter some data above to generate QR Code.")

# ------------------ QR CODE DECODER ------------------
elif menu == "Decode (Read QR Code)":
    st.header("🕵️ QR Code Decoder")

    uploaded_file = st.file_uploader("Upload an image with a QR Code (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Convert uploaded file to OpenCV image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Decode the QR Code
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(image)

        # Show image
        st.image(image, channels="BGR", caption="Uploaded Image", use_container_width=True)

        if data:
            st.success(f"✅ Decoded Data: {data}")
        else:
            st.error("❌ No QR code detected in the uploaded image.")


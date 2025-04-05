import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter

st.set_page_config(page_title="Image Filter App 🎨", layout="centered")
st.title("🎨 Image Filter App by Aliza Moin")
st.markdown("Upload an image and play with filters!")

uploaded_file = st.file_uploader("📤 Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    st.markdown("---")
    st.subheader("✨ Apply Filters")

    # Filters toggles
    apply_gray = st.checkbox("Grayscale")
    apply_blur = st.checkbox("Blur")
    apply_brightness = st.checkbox("Brightness")
    apply_contrast = st.checkbox("Contrast")
    apply_saturation = st.checkbox("Saturation")
    apply_darken = st.checkbox("Darken")
    apply_edges = st.checkbox("Edge Detection")

    # Sliders
    blur_level = st.slider("🔆 Blur Level", 0.0, 10.0, 2.0) if apply_blur else None
    brightness_factor = st.slider("🌞 Brightness", 0.5, 3.0, 1.0) if apply_brightness else None
    contrast_factor = st.slider("🎛 Contrast", 0.5, 3.0, 1.0) if apply_contrast else None
    saturation_level = st.slider("🌈 Saturation", 0.0, 3.0, 1.0) if apply_saturation else None
    darken_factor = st.slider("🌑 Darken Level", 0.0, 1.0, 1.0) if apply_darken else None

    if st.button("✨ Apply Filters"):
        edited_image = image

        if apply_gray:
            edited_image = edited_image.convert("L")
        
        if apply_blur:
            edited_image = edited_image.filter(ImageFilter.GaussianBlur(blur_level))

        if apply_brightness:
            enhancer = ImageEnhance.Brightness(edited_image)
            edited_image = enhancer.enhance(brightness_factor)

        if apply_contrast:
            enhancer = ImageEnhance.Contrast(edited_image)
            edited_image = enhancer.enhance(contrast_factor)

        if apply_saturation:
            enhancer = ImageEnhance.Color(edited_image)
            edited_image = enhancer.enhance(saturation_level)

        if apply_darken:
            enhancer = ImageEnhance.Brightness(edited_image)
            edited_image = enhancer.enhance(darken_factor)

        if apply_edges:
            edited_image = edited_image.filter(ImageFilter.FIND_EDGES)

        st.image(edited_image, caption="Edited Image", use_column_width=True)
        st.success("✅ Filters applied!")

        # Save & download
        edited_image.save("edited_image.jpg")
        with open("edited_image.jpg", "rb") as file:
            st.download_button("📥 Download Edited Image", file, file_name="filtered_image.jpg")

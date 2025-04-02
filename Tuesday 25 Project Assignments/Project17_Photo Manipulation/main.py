from PIL import Image, ImageEnhance, ImageFilter
import os

# Define the path to your single image
image_path = r"D:\25 Projects Python\Project17_Photo\butterfly.jpg"  # Update this to your image file location

# Check if the file exists at the specified path
if not os.path.exists(image_path):
    print(f"Error: The file at {image_path} does not exist.")
else:
    # Load the image
    image = Image.open(image_path)

    # Convert to grayscale
    gray_image = image.convert("L")

    # Apply blur filter
    blurred_image = image.filter(ImageFilter.BLUR)

    # Adjust brightness (1.5 times brighter)
    brightness_enhancer = ImageEnhance.Brightness(image)
    bright_image = brightness_enhancer.enhance(1.5)

    # Adjust contrast (1.8 times higher contrast)
    contrast_enhancer = ImageEnhance.Contrast(image)
    contrast_image = contrast_enhancer.enhance(1.8)

    # Generate new image names based on the original file name
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    gray_image_path = f"{base_name}_gray.jpg"
    blurred_image_path = f"{base_name}_blur.jpg"
    bright_image_path = f"{base_name}_bright.jpg"
    contrast_image_path = f"{base_name}_contrast.jpg"

    # Save the edited images
    gray_image.save(gray_image_path)
    blurred_image.save(blurred_image_path)
    bright_image.save(bright_image_path)
    contrast_image.save(contrast_image_path)

    # Show all the images
    image.show(title="Original Image")
    gray_image.show(title="Grayscale Image")
    blurred_image.show(title="Blurred Image")
    bright_image.show(title="Brighter Image")
    contrast_image.show(title="High Contrast Image")

    print(f"✅ Image processing complete for {image_path}! Check your directory for the new images.")

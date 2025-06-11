import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="UPC-A Barcode Reader", layout="centered")
st.title("📷 Barcode Digit Reader (Camera + Upload)")
st.write("Upload an image or capture from camera to read digits from the barcode.")

# --- Input Section ---
tab1, tab2 = st.tabs(["📤 Upload Image", "📷 Use Camera"])

uploaded_img = None

with tab1:
    uploaded_file = st.file_uploader("Upload a barcode image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        uploaded_img = Image.open(uploaded_file).convert("RGB")

with tab2:
    camera_image = st.camera_input("Capture barcode using camera")
    if camera_image:
        uploaded_img = Image.open(camera_image).convert("RGB")

# --- Decode logic ---
def decode_upc_digits(text):
    upc_str = ''.join(filter(str.isdigit, text.strip()))
    if len(upc_str) != 12:
        return "Invalid UPC-A (must be 12 digits)", None
    
    parts = {
        "Number System": upc_str[0],
        "Manufacturer Code": upc_str[1:6],
        "Product Code": upc_str[6:11],
        "Check Digit": upc_str[11]
    }

    digits = [int(d) for d in upc_str]
    odd_sum = sum(digits[i] for i in range(0, 11, 2))
    even_sum = sum(digits[i] for i in range(1, 11, 2))
    total = (odd_sum * 3) + even_sum
    calculated_check = (10 - (total % 10)) % 10

    is_valid = calculated_check == digits[-1]
    return ("Valid" if is_valid else "Invalid Check Digit"), parts

# --- Processing Section ---
if uploaded_img:
    st.image(uploaded_img, caption="Selected Image", use_column_width=True)
    img_np = np.array(uploaded_img)

    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 3)

    config = "--psm 6 -c tessedit_char_whitelist=0123456789"
    extracted_text = pytesseract.image_to_string(thresh, config=config)

    st.code(extracted_text, language='text')

    status, parts = decode_upc_digits(extracted_text)
    if parts:
        st.success(f"✅ UPC Code: {''.join(parts.values())}")
        st.write("### 🔍 Breakdown:")
        st.json(parts)
        st.markdown(f"**Validation:** `{status}`")
    else:
        st.error("❌ Could not extract a valid 12-digit UPC-A code.")

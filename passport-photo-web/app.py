import streamlit as st
import io
from core import loader, detector, cropper, cleaner, validator

# Page Config
st.set_page_config(
    page_title="Passport Shop",
    page_icon="🛂",
    layout="wide",
)

# Custom CSS for "Premium" look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .reportview-container .main .block-container {
        max_width: 1000px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .step-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🛂 Passport Shop")
st.markdown("### Creating Compliant U.S. Passport Photos Instantly")
st.markdown("---")

# Sidebar
st.sidebar.title("Configuration")
st.sidebar.info("This app follows U.S. State Department requirements: 2x2 inches (600x600px), white background, centered face.")

# 1. Upload
st.header("1. Upload Photo")
uploaded_file = st.file_uploader("Choose a clear photo of yourself", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Load and Display Original
    raw_image_bgr = loader.load_image_from_bytes(uploaded_file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(loader.convert_opencv_to_pil(raw_image_bgr), use_container_width=True)
        
    with col2:
        st.subheader("Processed Result")
        
        if st.button("Generate Passport Photo"):
            with st.spinner("Analyzing face..."):
                face_bbox = detector.detect_face_bbox(raw_image_bgr)
                
            if face_bbox is None:
                st.error("No face detected! Please use a photo with a clear frontal face.")
            else:
                progress_bar = st.progress(0)
                
                # Step 1: Crop
                with st.spinner("Cropping and Centering..."):
                    cropped_img = cropper.crop_centered_face(raw_image_bgr, face_bbox)
                    progress_bar.progress(50)
                
                # Step 2: Clean Background
                with st.spinner("Removing Background (AI)..."):
                    cleaned_img = cleaner.remove_background(cropped_img)
                    progress_bar.progress(90)
                
                # Step 3: Validate
                is_valid, validation_msgs = validator.validate_image(cleaned_img)
                progress_bar.progress(100)
                
                # Display Result
                st.image(loader.convert_opencv_to_pil(cleaned_img), use_container_width=True)
                
                # Validation Details
                if is_valid:
                    st.success("✅ Compliance Checks Passed")
                else:
                    st.warning("⚠️ Potential Compliance Issues")
                
                with st.expander("See Validation Details"):
                    for msg in validation_msgs:
                        st.write(f"- {msg}")
                        
                # Download Button
                # Convert back to bytes for download
                final_pil = loader.convert_opencv_to_pil(cleaned_img)
                buf = io.BytesIO()
                final_pil.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="Download Passport Photo (JPG)",
                    data=byte_im,
                    file_name="passport_photo.jpg",
                    mime="image/jpeg"
                )

else:
    st.info("👆 Please upload a photo to get started.")

st.markdown("---")
st.markdown("© 2025 Passport Shop | Vibe Coding Winter Camp")

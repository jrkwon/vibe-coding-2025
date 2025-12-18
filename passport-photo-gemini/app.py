import streamlit as st
from processor import PassportProcessor

# Initialize
processor = PassportProcessor()

st.set_page_config(page_title="PassportShop Web", page_icon="📸")
st.title("📸 PassportShop Web")
st.markdown("""
**Generate compliant U.S. passport photos automatically.**
1. **Upload** your photo.
2. **AI Processing:** Removes background, detects face, crops, and resizes.
3. **Download** your 600x600px image.
""")

uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Load Original
    original_image = processor.load_image_from_bytes(uploaded_file)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(original_image, use_container_width=True)

    with st.spinner("Processing... This may take a moment (downloading AI models)..."):
        try:
            # 2. Remove Background (NEW STEP)
            img_no_bg = processor.remove_background(original_image)
            
            # 3. Detect Face
            face_box = processor.detect_face(img_no_bg)
            
            if face_box is None:
                st.error("No face detected! Try a photo with better lighting.")
            else:
                # 4. Crop & Center
                cropped_img = processor.crop_and_center(img_no_bg, face_box)
                
                # 5. Resize
                final_img = processor.resize_image(cropped_img)
                
                # 6. Validate
                issues = processor.validate_image(final_img)

                with col2:
                    st.subheader("Passport Result")
                    st.image(final_img, caption="600x600px | White BG", use_container_width=True)
                
                st.divider()
                st.subheader("Compliance Report")
                if not issues:
                    st.success("✅ Photo compliant!")
                    st.download_button(
                        label="Download Passport Photo",
                        data=processor.convert_to_bytes(final_img),
                        file_name="passport_photo.jpg",
                        mime="image/jpeg"
                    )
                else:
                    for issue in issues:
                        st.warning(f"⚠️ {issue}")
                        
        except Exception as e:
            st.error(f"An error occurred: {e}")
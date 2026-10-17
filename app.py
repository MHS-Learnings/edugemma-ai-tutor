import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title="EduGemma - Multimodal Science & Math AI Tutor",
    page_icon="🎓",
    layout="wide"
)

# Header Section
st.title("🎓 EduGemma: Multimodal Science & Math AI Tutor")
st.caption("Powered by Google Gemma 4 & Gemini API | Open-Source Agent Skill")
st.markdown("---")

# Sidebar for API Key
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Features")
st.sidebar.write("- 📸 Image & Text Multimodal Analysis")
st.sidebar.write("- ✍️ Step-by-Step Problem Solving")
st.sidebar.write("- 💡 Concept Breakdown & Quizzes")

# Main Content Area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Upload Diagram, Question, or Notes")
    uploaded_file = st.file_uploader("Choose an image file (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    user_query = st.text_area(
        "Ask a specific question about the image (Optional):",
        placeholder="e.g., Explain this diagram step by step and give me 3 practice questions."
    )

with col2:
    st.subheader("2. AI Tutor Solution & Explanation")
    
    if st.button("🚀 Analyze & Solve with EduGemma", type="primary"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar!")
        elif uploaded_file is None and not user_query.strip():
            st.warning("Please upload an image or type a question to get started!")
        else:
            with st.spinner("EduGemma is analyzing your question..."):
                try:
                    genai.configure(api_key=api_key)
                    
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = (
                        "You are an expert, encouraging Science and Mathematics Home Tutor. "
                        "1. Explain the concepts shown in the image or query in very clear, easy-to-understand steps. "
                        "2. Provide the complete solution if it is a problem or numerical. "
                        "3. End with 3 short quiz questions to test the student's understanding.\n\n"
                        f"Student Query: {user_query if user_query else 'Explain this step by step.'}"
                    )
                    
                    if uploaded_file is not None:
                        response = model.generate_content([prompt, image])
                    else:
                        response = model.generate_content(prompt)
                    
                    st.success("Analysis Complete!")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

st.markdown("---")
st.caption("EduGemma AI Tutor - Open Source Project under MIT License.")

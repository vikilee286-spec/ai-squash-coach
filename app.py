import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Squash Coach", page_icon="🎾", layout="centered")

# --- 2. API Key Setup (Secure Mode) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except FileNotFoundError:
    api_key = None 

# --- 3. Sidebar: Clean & Professional ---
with st.sidebar:
    st.header("⚙️ System Status")
    if not api_key:
        api_key = st.text_input("Enter Google API Key (Developer Mode)", type="password")
    
    st.success("🟢 AI Engine Online")
    st.info("💡 Powered by Gemini Vision AI. \n\nDeveloper: Tony Gao")

# --- 4. Core Logic Function ---
def analyze_video(video_path, prompt, key, mime_type):
    genai.configure(api_key=key)
    
    status_text = st.empty()
    status_text.info("🚀 Uploading footage to AI engine...")
    
    print(f"DEBUG: Uploading file with mime_type: {mime_type}")
    
    # Upload
    video_file = genai.upload_file(path=video_path, mime_type=mime_type)
    
    # Wait for processing
    while video_file.state.name == "PROCESSING":
        status_text.info("⏳ Processing video, AI is analyzing court movement...")
        time.sleep(2)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        st.error(f"❌ Video processing failed: {video_file.state.name}")
        return None

    status_text.info("🧠 Generating tactical and technical feedback...")
    
    # Using the fast Flash model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    
    response = model.generate_content([video_file, prompt])
    
    status_text.success("✅ Analysis Complete!")
    return response.text

# --- 5. Main UI ---
st.title("🎾 Next-Gen Squash AI Coach")
st.markdown("Upload your practice footage. The AI coach will analyze your **racket preparation**, **footwork**, and **court positioning**.")

# 密码验证已被彻底移除，所有人均可直接上传
uploaded_file = st.file_uploader("Upload video clip (Recommended length: < 30 seconds)", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    if not api_key:
         st.error("❌ API Key not detected. Please check system configurations.")
    else:
        st.video(uploaded_file)
        
        # 针对美国教练和高水平训练优化的全英文 Prompt
        default_prompt = """
        Act as an elite squash coach analyzing this practice footage.
        Please focus your analysis on:
        1. Racket preparation (Is it early and high enough?)
        2. Movement to and from the T-zone (Footwork efficiency).
        3. Shot selection and balance through the strike.
        
        Provide 3 concise, highly actionable bullet points for improvement. Use professional squash terminology.
        """
        prompt = st.text_area("Coach's Instruction (Prompt)", value=default_prompt, height=180)

        if st.button("Start AI Analysis", type="primary"):
            file_extension = os.path.splitext(uploaded_file.name)[1]
            if not file_extension:
                file_extension = ".mp4"

        
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tfile:
                tfile.write(uploaded_file.read())
                temp_filename = tfile.name
            
            try:
                result = analyze_video(temp_filename, prompt, api_key, uploaded_file.type)
                if result:
                    st.markdown("### 📋 AI Scouting Report")
                    st.markdown(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                try:
                    os.remove(temp_filename)
                except:
                    pass



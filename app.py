import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Squash Coach", page_icon="🎾", layout="wide") # 改为 wide 布局，让左右分栏更美观

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
    st.info("💡 Powered by Gemini Vision AI. \n\nDeveloper: Tony Gao (Class of 2031)")

# --- 4. Core Logic Function ---
def analyze_video(video_path, prompt, key, mime_type):
    genai.configure(api_key=key)
    status_text = st.empty()
    status_text.info("🚀 Uploading footage to AI engine...")
    
    video_file = genai.upload_file(path=video_path, mime_type=mime_type)
    
    while video_file.state.name == "PROCESSING":
        status_text.info("⏳ Processing video, AI is analyzing court movement...")
        time.sleep(2)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        st.error(f"❌ Video processing failed: {video_file.state.name}")
        return None

    status_text.info("🧠 Generating tactical and technical feedback...")
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    response = model.generate_content([video_file, prompt])
    status_text.success("✅ Analysis Complete!")
    return response.text

# --- 5. Main UI with Tabs ---
st.title("🎾 Next-Gen Squash AI Coach")
st.markdown("Upload your practice footage, or explore AI tactical breakdowns of PSA professionals.")

# 创建两个极其现代的选项卡
tab_solo, tab_pro = st.tabs(["📹 Solo Training (Analyze My Video)", "🏆 Pro Case Studies (PSA)"])

# ==== 选项卡 1：原本的上传分析功能 ====
with tab_solo:
    st.markdown("### Upload Your Footage")
    uploaded_file = st.file_uploader("Upload video clip (Recommended length: < 30 seconds)", type=['mp4', 'mov', 'avi'])

    if uploaded_file is not None:
        if not api_key:
             st.error("❌ API Key not detected. Please check system configurations.")
        else:
            # 限制个人视频的显示宽度
            col_video, col_blank = st.columns([1, 1])
            with col_video:
                st.video(uploaded_file)
            
            default_prompt = """
            Act as an elite squash coach analyzing this practice footage.
            Please focus your analysis on:
            1. Racket preparation (Is it early and high enough?)
            2. Movement to and from the T-zone (Footwork efficiency).
            3. Shot selection and balance through the strike.
            Provide 3 concise, highly actionable bullet points for improvement.
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

# ==== 选项卡 2：职业球员战术解析展厅 ====
with tab_pro:
    st.markdown("### 🧠 AI Tactical Breakdown: Paul Coll (Former World #1)")
    st.info("How does AI decode the movement and technique of 'Superman' on the PSA tour?")
    
    # --- 案例一：比赛飞扑回中 ---
    st.markdown("#### Case 1: The 'Superman' Recovery (British Open)")
    col1, col2 = st.columns([1, 1.2]) # 左边视频，右边文字
    
    with col1:
        try:
            st.video("coll_match.mp4")
        except:
            st.warning("Video file 'coll_match.mp4' not found in repository.")
            
    with col2:
        st.markdown("**🎯 Prompt to Gemini Vision:**")
        st.code("Analyze the player in black (Paul Coll). Focus on his recovery path to the T-zone after the extreme lunge/dive in the front court.", language="text")
        st.markdown("**💡 AI Output & Tactical Takeaway:**")
        st.success("""
        * **Incredible Resilience:** After the desperate retrieve, Coll instantly pushes off the floor using his core and front lunging leg.
        * **Visual Discipline:** His eyes remain fixed on the front wall and his opponent, never dropping his head.
        * **Efficiency:** Notice the explosive crossover step. He is back dominating the T-zone before the opponent can strike.
        * **Takeaway for Tony:** Never admire your own shot. The point continues until the ball bounces twice. Immediate T-recovery is non-negotiable.
        """)
        
    st.divider() # 分割线
    
    # --- 案例二：前场极速截击 ---
    st.markdown("#### Case 2: Front-Court Volley Drill (Extreme Reaction)")
    col3, col4 = st.columns([1, 1.2])
    
    with col3:
        try:
            st.video("coll_volley.mp4")
        except:
            st.warning("Video file 'coll_volley.mp4' not found in repository.")
            
    with col4:
        st.markdown("**🎯 Prompt to Gemini Vision:**")
        st.code("Analyze the rapid front-wall volley drill. Focus on racket preparation, backswing length, and wrist stability.", language="text")
        st.markdown("**💡 AI Output & Technical Takeaway:**")
        st.success("""
        * **Shortened Backswing:** To cope with the rapid pace, the backswing is virtually eliminated. The racket head stays up and in front of the body at all times.
        * **Locked Wrist:** The wrist remains completely stable. Power is generated purely from rapid forearm rotation and slight body weight transfer.
        * **Target Fixation:** Outstanding hand-eye coordination with zero wasted movement.
        * **Takeaway for Tony:** On aggressive front-court volleys, shorten the swing, lock the wrist, and keep the racket preparation extremely early.
        """)
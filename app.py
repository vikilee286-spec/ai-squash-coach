import streamlit as st
import google.generativeai as genai
import tempfile
import os
import time

# --- 1. 页面配置 ---
st.set_page_config(page_title="AI Squash Coach", page_icon="🎾", layout="centered")

# --- 2. 侧边栏：配置区 ---
with st.sidebar:
    st.header("🔑 配置")
    api_key = st.text_input("输入 Google API Key", type="password")
    app_password = st.text_input("访问密码", type="password")

# --- 3. 核心逻辑函数 ---
def analyze_video(video_path, prompt, key, mime_type):
    genai.configure(api_key=key)
    
    status_text = st.empty()
    status_text.info("🚀 正在上传视频到 Gemini...")
    
    print(f"DEBUG: Uploading file with mime_type: {mime_type}")
    
    # 上传
    video_file = genai.upload_file(path=video_path, mime_type=mime_type)
    
    # 等待处理
    while video_file.state.name == "PROCESSING":
        status_text.info("⏳ 视频处理中，AI 正在观看...")
        time.sleep(2)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        st.error(f"❌ 视频处理失败: {video_file.state.name}")
        return None

    status_text.info("🧠 AI (Gemini Flash) 正在分析动作...")
    
    # 【关键修改】这里改成了你账号里确认存在的名字
    # 如果你想用更强的 2.0，可以改成 "gemini-2.0-flash"
    model = genai.GenerativeModel(model_name="gemini-flash-latest")
    
    response = model.generate_content([video_file, prompt])
    
    status_text.success("✅ 分析完成！")
    return response.text

# --- 4. 主界面 UI ---
st.title("🎾 Next-Gen Squash AI Coach")
st.markdown("上传你的练习视频，AI 教练将分析你的**引拍**、**步伐**和**重心**。")

# 密码验证
if app_password == "tony2026":
    uploaded_file = st.file_uploader("上传视频片段 (建议 < 30秒)", type=['mp4', 'mov', 'avi'])

    if uploaded_file is not None and api_key:
        st.video(uploaded_file)
        
        default_prompt = """
        作为一个专业的壁球教练，请分析这段视频。
        重点关注：1.正手击球的引拍是否充分？ 2.击球后的回中速度。
        给出3个简短的改进建议。
        """
        prompt = st.text_area("教练指令 (Prompt)", value=default_prompt, height=150)

        if st.button("开始 AI 分析", type="primary"):
            file_extension = os.path.splitext(uploaded_file.name)[1]
            if not file_extension:
                file_extension = ".mp4"

            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tfile:
                tfile.write(uploaded_file.read())
                temp_filename = tfile.name
            
            try:
                result = analyze_video(temp_filename, prompt, api_key, uploaded_file.type)
                if result:
                    st.markdown("### 📋 分析报告")
                    st.markdown(result)
            except Exception as e:
                st.error(f"发生错误: {e}")
            finally:
                try:
                    os.remove(temp_filename)
                except:
                    pass
    elif not api_key:
        st.warning("👈 请先在左侧输入 API Key")
else:
    st.info("🔒 请在左侧输入访问密码以使用此工具。")
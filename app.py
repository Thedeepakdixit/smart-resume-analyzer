import streamlit as st
from PyPDF2 import PdfReader
from streamlit_lottie import st_lottie
import requests
import google.generativeai as genai
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# --- Gemini API Key Configuration ---
genai.configure(api_key="AIzaSyAPLFXb7yfGsjuCGiRZbZfG-sVQTYCEUH0")  # Replace with your Gemini API key

# Gemini Pro model setup
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get response from Gemini
def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load sample animation
lottie_resume = load_lottie_url("https://lottie.host/ed4c1179-c355-43ee-b05d-c6b5303553ff/kV36FbN3N1.json")

# Page config
st.set_page_config(
    page_title="Smart Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        margin: 0.5rem 0;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stTextArea, .stFileUploader {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📘 About")
st.sidebar.info("This tool helps you analyze your resume against job descriptions using Google's Gemini AI.")
st.sidebar.markdown("---")
st.sidebar.markdown("👤 Built by **Team Oppenheimer**")

# Animation on top
with st.container():
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.title("📄 Smart Resume Analyzer")
        st.markdown("### ✨ Select an Action", unsafe_allow_html=True)
    with right_col:
        if lottie_resume:
            st_lottie(lottie_resume, height=180, key="resume")

# Function to show Word Cloud
def show_wordcloud(resume_text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(resume_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)


# Inputs
input_text = st.text_area("📝 Job Description:", key="input")
uploaded_file = st.file_uploader("📤 Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("✅ Resume uploaded successfully!")

# Buttons
col1, col2, col3,col4 = st.columns(4)
with col1:
    submit1 = st.button("📌 Tell Me About the Resume")
    submit2 = st.button("🛠️ How Can I Improvise My Skills")
with col2:
    submit3 = st.button("📊 Percentage Match")
    submit4 = st.button("📌 ATS Compatibility Score")
with col3:
    submit5 = st.button("🔍 Keywords Analysis & Visualization")
    submit6 = st.button("💼 Job Role Suggestions")
with col4:
    submit7 = st.button("🧩 Match Resume to Job Description")
    submit8 = st.button("🎓 Suggest Certifications & Courses")

# PDF Parsing
def input_pdf_setup(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Prompts
input_prompt1 = """You are an experienced Technical Human Resource Manager. Evaluate the following resume and provide a detailed summary of the candidate's profile, including strengths, areas of improvement, and technologies used.\n\nResume:\n{resume}"""
input_prompt2 = """You are an experienced Career Coach. Suggest how the following candidate can improve their skills based on their resume and job description.\n\nResume:\n{resume}\n\nJob Description:\n{jd}"""
input_prompt3 = """You are a skilled ATS (Applicant Tracking System) scanner. Compare the resume to the job description and output a percentage match and key compatibility metrics.\n\nResume:\n{resume}\n\nJob Description:\n{jd}"""
input_prompt4 = """You are an ATS (Applicant Tracking System) expert. Give a score (1 to 100) on ATS compatibility of the following resume and suggest improvements.\n\nResume:\n{resume}"""
input_prompt5 = """You are an ATS expert and resume optimization specialist. Find out which keywords from the job description are missing in the resume and list them.\n\nResume:\n{resume}\n\nJob Description:\n{jd}"""
input_prompt6 = """You are a career advisor. Based on this resume, suggest 3 best-fit job roles with brief reasoning.\n\nResume:\n{resume}"""
input_prompt7 = """You are a resume writing expert and ATS optimization specialist for roles such as Frontend Developer, Backend Developer, Full Stack Developer, Mobile App Developer, Game Developer, Data Scientist, Data Analyst, Data Engineer, Business Intelligence Analyst, AI Engineer, Machine Learning Engineer, Deep Learning Engineer, NLP Engineer, Cybersecurity Analyst, Ethical Hacker, Security Engineer, Incident Responder, Cloud Engineer, DevOps Engineer, Site Reliability Engineer (SRE), Quality Assurance Engineer, Automation Tester, Network Administrator, System Administrator, Cloud Systems Administrator, Database Administrator, Big Data Engineer, Blockchain Developer, AR/VR Developer, IoT Developer, Research Scientist, University Lecturer/Professor, Product Manager, UI/UX Designer, Tech Support Engineer, and Freelancer/Consultant.
Your task is to modify the provided resume to align it perfectly with the job description. Recommend specific changes to the skills, experience, or format of the resume to increase its ATS compatibility and make it more appealing to recruiters.\n\nResume:\n{resume}\n\nJob Description:\n{jd}"""
input_prompt8 = """You are a professional Career Advisor. Suggest some relevant certifications and courses for this candidate based on their resume and job description.Also suggest related youtube videos.\n\nResume:\n{resume}\n\nJob Description:\n{jd}"""

# Handle Button Clicks with Gemini Response
if uploaded_file:
    resume_text = input_pdf_setup(uploaded_file)

    if submit1:
        final_prompt = input_prompt1.format(resume=resume_text)
        response = get_gemini_response(final_prompt)
        st.subheader("📝 Resume Summary:")
        st.write(response)

    elif submit2:
        final_prompt = input_prompt2.format(resume=resume_text, jd=input_text)
        response = get_gemini_response(final_prompt)
        st.subheader("🛠️ Skill Improvement Suggestions:")
        st.write(response)

    elif submit3:
        final_prompt = input_prompt3.format(resume=resume_text, jd=input_text)
        response = get_gemini_response(final_prompt)
        st.subheader("📊 Percentage Match:")
        st.write(response)

    elif submit4:
        final_prompt = input_prompt4.format(resume=resume_text, jd=input_text)
        response = get_gemini_response(final_prompt)
        st.subheader("📌 ATS Compatibility Score & Suggestions")
        st.write(response)

    elif submit5:
        final_prompt = input_prompt4.format(resume=resume_text, jd=input_text)
        response = get_gemini_response(final_prompt)
        st.subheader("🔍 Missing Keywords:")
        st.write(response)
        st.subheader("📊 Resume Keyword Word Cloud")
        show_wordcloud(resume_text)

    elif submit6:
        final_prompt = input_prompt6.format(resume=resume_text, jd=input_text)
        response = get_gemini_response(final_prompt)
        st.subheader("🎓 Recommended Courses & Certifications:")
        st.write(response)

    elif submit7:
        final_prompt = input_prompt7.format(resume=resume_text, jd=input_text)
        response = get_gemini_response(final_prompt)
        st.subheader("🧩 Matched Resume Summary:")
        st.write(response)

    elif submit8:
        final_prompt = input_prompt8.format(resume=resume_text, jd=input_text)
        response = get_gemini_response(final_prompt)
        st.subheader("🎓 Recommended Courses & Certifications:")
        st.write(response)
else:
    if submit1 or submit2 or submit3 or submit4 or submit5 or submit6:
        st.warning("⚠️ Please upload your resume first!")

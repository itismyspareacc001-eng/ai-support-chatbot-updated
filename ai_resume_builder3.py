# ==========================================================
# AI RESUME BUILDER PRO
# Day 16 Project
#
# Features:
# - Gemini Resume Generation
# - Multiple Templates
# - ATS Resume Review
# - PDF Export
# - TXT Export
# - Streamlit UI
# ==========================================================

import streamlit as st
import google.generativeai as genai

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Resume Builder Pro",
    page_icon="📄",
    layout="wide"
)

# ==========================================================
# GEMINI CONFIGURATION
# ==========================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================================================
# SESSION STATE
# ==========================================================

if "generated_resume" not in st.session_state:
    st.session_state.generated_resume = ""

if "resume_review" not in st.session_state:
    st.session_state.resume_review = ""

# ==========================================================
# PDF GENERATOR
# ==========================================================

def create_pdf(resume_text):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    for line in resume_text.split("\n"):

        if line.strip():

            content.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

            content.append(
                Spacer(1, 6)
            )

    doc.build(content)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("📄 Resume Builder")

    st.markdown("---")

    st.info(
        """
        AI Resume Builder Pro

        Features:
        - ATS Resume Generation
        - Resume Review
        - PDF Export
        - Multiple Templates
        """
    )

    st.markdown("---")

    st.metric(
        "Resume Generated",
        "Yes" if st.session_state.generated_resume else "No"
    )

# ==========================================================
# TITLE
# ==========================================================

st.title("📄 AI Resume Builder Pro")

st.caption(
    "Generate ATS-Friendly Professional Resumes using Gemini AI"
)

st.markdown("---")

# ==========================================================
# PERSONAL INFORMATION
# ==========================================================

st.header("👤 Personal Information")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Full Name"
    )

    email = st.text_input(
        "Email"
    )

with col2:

    phone = st.text_input(
        "Phone Number"
    )

    linkedin = st.text_input(
        "LinkedIn Profile"
    )

github = st.text_input(
    "GitHub Profile"
)

# ==========================================================
# CAREER OBJECTIVE
# ==========================================================

st.header("🎯 Career Objective")

objective = st.text_area(
    "Career Objective",
    height=120
)

# ==========================================================
# EDUCATION
# ==========================================================

st.header("🎓 Education")

education = st.text_area(
    "Education Details",
    height=150
)

# ==========================================================
# SKILLS
# ==========================================================

st.header("💻 Technical Skills")

skills = st.text_area(
    "Skills (comma separated)",
    height=120
)

# ==========================================================
# INTERNSHIPS
# ==========================================================

st.header("🏢 Internships")

internships = st.text_area(
    "Internship Details",
    height=150
)

# ==========================================================
# PROJECTS
# ==========================================================

st.header("🚀 Projects")

projects = st.text_area(
    "Project Details",
    height=200
)

# ==========================================================
# CERTIFICATIONS
# ==========================================================

st.header("🏆 Certifications")

certifications = st.text_area(
    "Certification Details",
    height=120
)

# ==========================================================
# ACHIEVEMENTS
# ==========================================================

st.header("🥇 Achievements")

achievements = st.text_area(
    "Achievement Details",
    height=120
)

# ==========================================================
# TEMPLATE SELECTION
# ==========================================================

st.header("🎨 Resume Template")

template = st.selectbox(
    "Select Template",
    [
        "Student Fresher",
        "Modern Professional",
        "Experienced Professional"
    ]
)

# ==========================================================
# BUTTONS
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    generate_button = st.button(
        "🚀 Generate Resume",
        use_container_width=True
    )

with col2:

    review_button = st.button(
        "📊 Review Resume",
        use_container_width=True
    )

# ==========================================================
# RESUME GENERATION
# ==========================================================

if generate_button:

    if not name.strip():

        st.error(
            "Please enter your name."
        )

    else:

        if template == "Student Fresher":

            template_instruction = """
Create a resume for a fresher.

Focus on:
- Education
- Skills
- Projects
- Internships
- Certifications

Make the candidate job-ready.
"""

        elif template == "Modern Professional":

            template_instruction = """
Create a modern professional resume.

Focus on:
- Professional Summary
- Skills
- Projects
- Certifications
- Achievements

Use modern corporate language.
"""

        else:

            template_instruction = """
Create an experienced professional resume.

Focus on:
- Leadership
- Business Impact
- Achievements
- Experience

Use executive-level language.
"""

        with st.spinner(
            "Generating Resume..."
        ):

            try:

                prompt = f"""
You are an expert ATS resume writer.

{template_instruction}

Candidate Information

Name:
{name}

Email:
{email}

Phone:
{phone}

LinkedIn:
{linkedin}

GitHub:
{github}

Career Objective:
{objective}

Education:
{education}

Technical Skills:
{skills}

Internships:
{internships}

Projects:
{projects}

Certifications:
{certifications}

Achievements:
{achievements}

Requirements:

1. ATS Friendly Resume
2. Strong Professional Summary
3. Professional Formatting
4. Improved Wording
5. Highlight Skills
6. Highlight Projects
7. Highlight Achievements

Return only the resume.
"""

                response = model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.4
                    }
                )

                st.session_state.generated_resume = (
                    response.text
                )

                st.success(
                    "Resume Generated Successfully!"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

# ==========================================================
# RESUME REVIEWER
# ==========================================================

if review_button:

    if not st.session_state.generated_resume:

        st.warning(
            "Generate a resume first."
        )

    else:

        with st.spinner(
            "Reviewing Resume..."
        ):

            try:

                review_prompt = f"""
Review the following resume.

Provide:

1. ATS Score (0-100)
2. Strengths
3. Weaknesses
4. Missing Keywords
5. Suggestions
6. Hiring Readiness

Resume:

{st.session_state.generated_resume}
"""

                review_response = model.generate_content(
                    review_prompt
                )

                st.session_state.resume_review = (
                    review_response.text
                )

            except Exception as e:

                st.error(
                    f"Review Error: {e}"
                )

# ==========================================================
# DISPLAY GENERATED RESUME
# ==========================================================

if st.session_state.generated_resume:

    st.markdown("---")

    st.subheader(
        "📄 Generated Resume"
    )

    st.markdown(
        st.session_state.generated_resume
    )

    # TXT DOWNLOAD

    st.download_button(
        label="📥 Download TXT",
        data=st.session_state.generated_resume,
        file_name="ATS_Resume.txt",
        mime="text/plain",
        use_container_width=True
    )

    # PDF DOWNLOAD

    pdf_file = create_pdf(
        st.session_state.generated_resume
    )

    st.download_button(
        label="📄 Download PDF",
        data=pdf_file,
        file_name="ATS_Resume.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# ==========================================================
# DISPLAY REVIEW
# ==========================================================

if st.session_state.resume_review:

    st.markdown("---")

    with st.expander(
        "📊 Resume Review Report"
    ):

        st.markdown(
            st.session_state.resume_review
        )

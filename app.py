import streamlit as st
import requests
import google.generativeai as genai
import pdf2image
import io
import base64
import webbrowser
from fpdf import FPDF # You'll need to install this: pip install fpdf

# Configure Gemini API
genai.configure(api_key="AIzaSyCO4lF2U3tjwv5myTkqH1LUBWaWuwuedis")

# --- Existing Functions ---

def get_linkedin_info(linkedin_url):
    if "linkedin.com" not in linkedin_url:
        return "Invalid LinkedIn URL"
    # Dummy response
    return f"Extracted data from LinkedIn profile: {linkedin_url}"

def get_github_info(github_url):
    username = github_url.split("/")[-1]
    github_api_url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(github_api_url)
    if response.status_code == 200:
        repos = response.json()
        repo_names = [repo["name"] for repo in repos]
        return f"GitHub Repositories: {', '.join(repo_names)}"
    return "Invalid GitHub URL or User Not Found"

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Important: For deployment, poppler_path should not be hardcoded or managed differently.
            # For local development, ensure Poppler is correctly installed and its bin directory is in your PATH
            # or pointed to correctly here.
            images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=r"C:\Program Files (x86)\poppler\Library\bin")
            first_page = images[0]

            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts = [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }]
            return pdf_parts
        except Exception as e:
            st.error(f"Error processing PDF: {e}. Make sure Poppler is installed and configured correctly.")
            return None
    return None

# --- New Function for Resume Generation with robust checks ---

def generate_simple_resume_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", "B", 24)
    # Ensure all .get() calls have a default empty string
    pdf.cell(0, 10, data.get("name", ""), 0, 1, "C")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 7, f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('linkedin', '')} | {data.get('github', '')}", 0, 1, "C")
    pdf.ln(5)

    # Section: Summary/Objective
    summary_text = data.get("summary", "") # Ensure empty string default
    if summary_text.strip(): # Check if it's not empty after stripping whitespace
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Summary", 0, 1, "L")
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, summary_text)
        pdf.ln(5)

    # Section: Work Experience
    if data.get("experience"):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Work Experience", 0, 1, "L")
        pdf.set_font("Arial", size=10)
        for exp in data["experience"]:
            pdf.set_font("Arial", "B", 12)
            # Ensure empty strings for all components
            pdf.cell(0, 7, f"{exp.get('title', '')} at {exp.get('company', '')}", 0, 1, "L")
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 7, f"{exp.get('dates', '')}", 0, 1, "L")
            pdf.set_font("Arial", size=10)
            for resp in exp.get("responsibilities", []):
                # Ensure 'resp' is a string before passing to cell/multi_cell and not just whitespace
                if isinstance(resp, str) and resp.strip():
                    pdf.cell(10) # Indent
                    pdf.multi_cell(0, 5, f"- {resp}")
            pdf.ln(2)
        pdf.ln(5)

    # Section: Education
    if data.get("education"):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Education", 0, 1, "L")
        pdf.set_font("Arial", size=10)
        for edu in data["education"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 7, f"{edu.get('degree', '')}, {edu.get('university', '')}", 0, 1, "L")
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 7, f"{edu.get('dates', '')}", 0, 1, "L")
            pdf.ln(2)
        pdf.ln(5)

    # Section: Skills
    skills_list = data.get("skills", []) # Ensure skills is a list, default to empty list
    # Filter out any non-string or empty elements that might have crept in
    clean_skills = [s for s in skills_list if isinstance(s, str) and s.strip()]
    if clean_skills: # Only print if there are actual skills
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Skills", 0, 1, "L")
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 5, ", ".join(clean_skills))
        pdf.ln(5)

    # Section: Projects
    if data.get("projects"):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Projects", 0, 1, "L")
        pdf.set_font("Arial", size=10)
        for proj in data["projects"]:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 7, proj.get('name', ''), 0, 1, "L")
            pdf.set_font("Arial", size=10)
            proj_desc = proj.get('description', '') # Ensure empty string default
            if proj_desc.strip(): # Only print if description exists and isn't just whitespace
                pdf.multi_cell(0, 5, proj_desc)
            pdf.ln(2)
        pdf.ln(5)

    # Output the PDF as bytes
    return pdf.output(dest='S').encode('latin-1') # Use latin-1 for FPDF output to bytes

# --- Streamlit UI ---
st.set_page_config(page_title="ProTrack.ai", page_icon="🔍", layout="wide") # Adjusted page title for clarity

st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose a feature", ["ATS Checker", "Resume Builder"])

if app_mode == "ATS Checker":
    st.header("ProTrack.ai [ATS]")

    # Job Description Input
    input_text = st.text_area("Job Description: ", key="input_jd")

    # Resume Upload
    uploaded_file = st.file_uploader("Upload Your Resume in PDF", type=["pdf"], key="ats_resume_upload")
    if uploaded_file:
        st.write("✅ PDF Uploaded Successfully")

    # LinkedIn and GitHub Inputs
    linkedin_url = st.text_input("Enter your LinkedIn profile URL", key="ats_linkedin_url")
    github_url = st.text_input("Enter your GitHub profile URL", key="ats_github_url")

    # Buttons to open LinkedIn & GitHub
    col1, col2 = st.columns(2)
    with col1:
        if linkedin_url:
            st.markdown(f'<a href="{linkedin_url}" target="_blank"><button style="background-color:#0A66C2; color:white; padding:5px 10px; border:none; border-radius:5px; cursor:pointer;">🔗 Open LinkedIn</button></a>', unsafe_allow_html=True)

    with col2:
        if github_url:
            st.markdown(f'<a href="{github_url}" target="_blank"><button style="background-color:#333; color:white; padding:5px 10px; border:none; border-radius:5px; cursor:pointer;">🔗 Open GitHub</button></a>', unsafe_allow_html=True)

    # Buttons for Resume Analysis
    submit1 = st.button("📄 Analyze My Resume")
    submit3 = st.button("📊 Get Percentage Match")

    # Prompts (Keep as is)
    input_prompt1 = """
    You are an experienced Technical HR Manager. Evaluate the resume against the job description.
    Also, analyze the provided LinkedIn and GitHub data to enhance the assessment.
    """

    input_prompt3 = """
    You are an ATS system. Evaluate the resume and profile data to provide a match percentage.
    Include missing keywords and final thoughts.
    """

    # Processing
    if submit1 or submit3:
        if uploaded_file:
            pdf_content = input_pdf_setup(uploaded_file)
            if pdf_content: # Ensure PDF was processed successfully
                linkedin_info = get_linkedin_info(linkedin_url)
                github_info = get_github_info(github_url)

                prompt = input_prompt1 if submit1 else input_prompt3
                try:
                    with st.spinner("Analyzing..."):
                        response = genai.GenerativeModel('gemini-1.5-flash').generate_content([
                            input_text, pdf_content[0], linkedin_info, github_info, prompt
                        ]).text
                    st.subheader("📝 Analysis Result")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error during AI analysis: {e}")
            else:
                st.error("⚠️ Could not process the uploaded resume. Please check the file or Poppler installation.")
        else:
            st.error("⚠️ Please upload a resume.")

elif app_mode == "Resume Builder":
    st.header("Create Your Resume")
    st.markdown("Fill out the sections below to generate a simple resume.")

    resume_data = {}

    st.subheader("Contact Information")
    # All text inputs now initialize with value=""
    resume_data["name"] = st.text_input("Full Name", value="", key="rb_name")
    resume_data["email"] = st.text_input("Email", value="", key="rb_email")
    resume_data["phone"] = st.text_input("Phone Number", value="", key="rb_phone")
    resume_data["linkedin"] = st.text_input("LinkedIn Profile URL", value="", key="rb_linkedin")
    resume_data["github"] = st.text_input("GitHub Profile URL", value="", key="rb_github")

    st.subheader("Summary/Objective")
    resume_data["summary"] = st.text_area("Write a brief summary or objective for your resume.", value="", key="rb_summary")

    st.subheader("Work Experience")
    # Allow adding multiple experiences
    if 'num_experiences' not in st.session_state:
        st.session_state.num_experiences = 1

    resume_data["experience"] = []
    for i in range(st.session_state.num_experiences):
        st.markdown(f"**Experience {i+1}**")
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            job_title = st.text_input(f"Job Title {i+1}", value="", key=f"rb_job_title_{i}")
        with col_exp2:
            company = st.text_input(f"Company {i+1}", value="", key=f"rb_company_{i}")
        dates = st.text_input(f"Dates (e.g., Jan 2020 - Dec 2023) {i+1}", value="", key=f"rb_dates_{i}")
        responsibilities_text = st.text_area(f"Key Responsibilities (one per line) {i+1}", value="", key=f"rb_responsibilities_{i}")

        # Only add experience if at least one core field has non-whitespace content
        if job_title.strip() or company.strip() or dates.strip() or responsibilities_text.strip():
            resume_data["experience"].append({
                "title": job_title,
                "company": company,
                "dates": dates,
                # Split responsibilities and filter out truly empty lines
                "responsibilities": [
                    resp.strip() for resp in responsibilities_text.split('\n') if resp.strip()
                ]
            })

    if st.button("Add Another Experience", key="add_exp_btn"): # Added unique key
        st.session_state.num_experiences += 1
        st.rerun() # Rerun to display new input fields

    st.subheader("Education")
    # Allow adding multiple education entries
    if 'num_education' not in st.session_state:
        st.session_state.num_education = 1

    resume_data["education"] = []
    for i in range(st.session_state.num_education):
        st.markdown(f"**Education {i+1}**")
        degree = st.text_input(f"Degree/Major {i+1}", value="", key=f"rb_degree_{i}")
        university = st.text_input(f"University/Institution {i+1}", value="", key=f"rb_university_{i}")
        edu_dates = st.text_input(f"Dates (e.g., Sep 2018 - May 2022) {i+1}", value="", key=f"rb_edu_dates_{i}")
        if degree.strip() or university.strip() or edu_dates.strip(): # Check for non-whitespace content
            resume_data["education"].append({
                "degree": degree,
                "university": university,
                "dates": edu_dates
            })

    if st.button("Add Another Education", key="add_edu_btn"): # Added unique key
        st.session_state.num_education += 1
        st.rerun()

    st.subheader("Skills")
    skills_text = st.text_area("List your skills, separated by commas (e.g., Python, SQL, AWS, Data Analysis)", value="", key="rb_skills")
    # Ensure list comprehension correctly handles empty strings and produces strings
    resume_data["skills"] = [s.strip() for s in skills_text.split(',') if s.strip()]

    st.subheader("Projects (Optional)")
    if 'num_projects' not in st.session_state:
        st.session_state.num_projects = 1

    resume_data["projects"] = []
    for i in range(st.session_state.num_projects):
        st.markdown(f"**Project {i+1}**")
        project_name = st.text_input(f"Project Name {i+1}", value="", key=f"rb_project_name_{i}")
        project_description = st.text_area(f"Project Description {i+1}", value="", key=f"rb_project_description_{i}")
        if project_name.strip() or project_description.strip(): # Check for non-whitespace content
            resume_data["projects"].append({
                "name": project_name,
                "description": project_description
            })
    if st.button("Add Another Project", key="add_proj_btn"): # Added unique key
        st.session_state.num_projects += 1
        st.rerun()

    st.markdown("---")
    if st.button("Generate Resume PDF"):
        # Debugging: Display the resume_data dictionary before PDF generation
        st.write("--- Debugging Resume Data Before PDF Generation ---")
        st.json(resume_data)
        st.write("--- End Debugging ---")

        if resume_data["name"].strip() and resume_data["email"].strip(): # More robust validation
            try:
                pdf_bytes = generate_simple_resume_pdf(resume_data)
                st.success("Resume generated successfully!")
                st.download_button(
                    label="Download Resume as PDF",
                    data=pdf_bytes,
                    file_name=f"{resume_data['name'].replace(' ', '_')}_Resume.pdf",
                    mime="application/pdf"
                )
                st.write("---")
                st.subheader("Preview (Limited)")
                st.info("For a full preview, please download the PDF.")
                # Simple preview (won't look exactly like PDF but gives an idea)
                st.write(f"**Name:** {resume_data.get('name')}")
                st.write(f"**Email:** {resume_data.get('email')}")
                if resume_data.get('summary') and resume_data['summary'].strip():
                    st.write(f"**Summary:** {resume_data['summary']}")
                if resume_data.get('skills'):
                    st.write(f"**Skills:** {', '.join(resume_data['skills'])}")
            except Exception as e:
                st.error(f"An error occurred during PDF generation: {e}")
                st.info("Please review your inputs, especially multi-line text areas, for any unusual characters or unintended empty entries.")
        else:
            st.error("Please enter at least your **Full Name** and **Email** to generate the resume.")

# Footer
footer = """
<style>
.footer {position: fixed; bottom: 0; left: 0; width: 100%; background-color: #f5f5f5;
color: #000; text-align: center; padding: 10px 0; font-size: 12px;}
</style>
<div class="footer">ProTrack created by <strong>Raginee Darade</strong></div>
"""
st.markdown(footer, unsafe_allow_html=True)


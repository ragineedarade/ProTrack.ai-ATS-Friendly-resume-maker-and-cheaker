 # ProTrack.ai [ATS & Resume Builder]

## Overview
ProTrack.ai is an AI-driven platform designed to streamline the job application process. It features an advanced Applicant Tracking System (ATS) that efficiently evaluates resumes against job descriptions, addressing common recruitment challenges by providing automated and unbiased analysis. Additionally, ProTrack.ai now includes a **Resume Builder**, empowering users to create professional resumes directly within the application using simple templates and input fields. This combined approach reduces manual effort, enhances decision-making for recruiters, and provides job seekers with tools to optimize their application materials.

## Problem Statement
* Employers struggle with efficiently screening resumes against job descriptions, leading to missed talent and prolonged hiring cycles.
* Existing ATS solutions often lack comprehensive analysis, potentially missing crucial context or specific skills.
* Manual evaluation is time-consuming, prone to human bias, and inefficient at scale.
* Job seekers often lack easy-to-use tools to create ATS-friendly resumes tailored to job requirements.

## Core Features
* **Resume Evaluation (ATS):** Automatically evaluates uploaded PDF resumes against provided job descriptions.
* **Professional Analysis:** Highlights strengths, weaknesses, and missing keywords in resumes relative to the job description.
* **Match Percentage:** Calculates and displays a percentage match between resumes and job descriptions.
* **Resume Builder:** Allows users to create new resumes from a simple template by filling in structured information.
* **Report Generation:** Generates detailed evaluation reports for ATS analysis.
* **Direct Profile Access:** Provides convenient links to open LinkedIn and GitHub profiles directly from the ATS interface.

## Scope
### In Scope:
* Accepts resumes in PDF format for ATS evaluation.
* Evaluates any job description text provided by the user.
* Provides insights such as keyword matching, strengths, and weaknesses based on ATS criteria.
* **Generates simple PDF resumes based on user input via the Resume Builder.**
* Offers a user-friendly interface with clear navigation between features.

### Out of Scope:
* Resumes in formats other than PDF for ATS evaluation (e.g., DOCX, TXT).
* Industry-specific in-depth analysis beyond general ATS and AI capabilities.
* Manual feedback or customizations on resumes beyond automated ATS evaluations.
* Complex, highly customizable resume design templates in the Resume Builder.
* Direct integration with external job boards or applicant tracking systems for data submission.

## Functional Requirements
* **Resume Upload:** Accepts PDF format resumes for ATS analysis.
* **Job Description Input:** Allows users to input job descriptions.
* **ATS Match Percentage:** Calculates and displays the match percentage.
* **Evaluation Report:** Highlights strengths, weaknesses, and missing keywords in resumes.
* **Resume Data Input:** Provides structured input fields for building a resume (contact info, experience, education, skills, projects).
* **PDF Resume Generation:** Generates a downloadable PDF resume from user-provided data.

## Non-Functional Requirements
* **Performance:** Provides ATS analysis results within 10–15 seconds. Resume generation is near-instant.
* **Usability:** Simple and intuitive interface requiring no technical expertise from end-users.
* **Scalability:** Supports simultaneous uploads and resume generation by multiple users.
* **Security:** Ensures secure storage and handling of resumes and user data to protect privacy.

## Tech Stack
* **Programming Language:** Python
* **Libraries:**
    * `Pillow` (PIL) - for image processing (dependency of pdf2image)
    * `google-generativeai` - for AI capabilities
    * `pdf2image` - for converting PDF pages to images for analysis
    * `streamlit` - for building the web application UI
    * `fpdf` - for generating PDF resumes
    * `requests` - for making HTTP requests (e.g., to GitHub API)
    * `dotenv` - (If used for API key management, though `genai.configure` handles direct keys)
* **Tools:**
    * Virtual Environment
    * VS Code (or any preferred IDE)
* **AI Tools:** Google Generative AI (Gemini 1.5 Flash)
* **External Tools:** Poppler (external software for PDF rendering required by `pdf2image`)
* **API:** Google Generative AI API

## Installation and Setup
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/ProTrack.ai-ATS.git](https://github.com/your-username/ProTrack.ai-ATS.git)
    cd ProTrack.ai-ATS
    ```
2.  **Set Up Virtual Environment:**
    ```bash
    python -m venv venv
    # For Linux/Mac:
    source venv/bin/activate
    # For Windows:
    venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    (Ensure your `requirements.txt` includes `streamlit`, `google-generativeai`, `pdf2image`, `Pillow`, `fpdf`, `requests`)

4.  **Environment Configuration:**
    * Create a `.env` file in the root directory if you plan to manage API keys that way.
    * Alternatively, directly configure the Gemini API key in `app.py` as shown:
        ```python
        genai.configure(api_key="YOUR_GEMINI_API_KEY")
        ```
        (Replace `"YOUR_GEMINI_API_KEY"` with your actual API key)

5.  **Install Poppler:**
    * `pdf2image` requires Poppler to be installed on your system.
    * **Windows:** Download Poppler for Windows (e.g., from [https://poppler.freedesktop.org/](https://poppler.freedesktop.org/) or a pre-compiled version like `https://github.com/oschwartz10612/poppler-windows/releases`). Extract it and ensure the `bin` directory's path is either added to your system's `PATH` environment variable or explicitly provided in the `poppler_path` argument within the `input_pdf_setup` function in `app.py` (e.g., `poppler_path=r"C:\Program Files (x86)\poppler\Library\bin"`).
    * **Linux/macOS:** Install via your package manager (e.g., `sudo apt-get install poppler-utils` on Debian/Ubuntu, `brew install poppler` on macOS).

6.  **Run the Application:**
    ```bash
    streamlit run app.py
    ```

## Contribution
Contributions are welcome! Follow these steps:

1.  Fork the repository.
2.  Create a feature branch:
    ```bash
    git checkout -b feature-name
    ```
3.  Commit your changes:
    ```bash
    git commit -m "Add feature description"
    ```
4.  Push to the branch:
    ```bash
    git push origin feature-name
    ```
5.  Open a pull request.

## License
This project is licensed under the MIT License.

## Contact
For questions or collaboration, reach out to:

* **Email:** ragineedarade@gmail.com
* **LinkedIn:** raginee_darade

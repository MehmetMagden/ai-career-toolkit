# AI Career Application Toolkit

A multi-tab Gradio web utility designed to streamline the tech job application pipeline using Google Gemini API (`gemini-3.5-flash-lite`).

### Modules
1. **Resume Enhancer:** Reframes bullet points and aligns technical achievements with targeted role expectations.
2. **Customized Cover Letter Generator:** Drafts tailored cover letters mapped directly to specific job descriptions without hallucinating unverified skills.
3. **Strategic Career Advisor:** Conducts skill gap analyses between candidate resumes and job postings, outputting interview prep topics and upskilling priorities.

### Tech Stack
- Python 3.12
- Gradio (Tabs / Blocks UI)
- Google Gemini API (`gemini-3.5-flash-lite`)

### Run Locally
```bash
git clone [https://github.com/MehmetMagden/ai-career-toolkit.git](https://github.com/MehmetMagden/ai-career-toolkit.git)
cd ai-career-toolkit
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
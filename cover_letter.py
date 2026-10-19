import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import gradio as gr

# Environment 
load_dotenv()

# Start Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.5-flash-lite"

def generate_cover_letter(
    company_name: str,
    position_name: str,
    job_description: str,
    resume_content: str,
) -> str:
    """Generates a tailored, professional cover letter mapping resume facts to job requirements."""
    if not resume_content.strip() or not job_description.strip():
        return (
            "Please provide bot, your Resume Content and the Job Description."
        )

    company = company_name.strip() if company_name else "the hiring team"
    position = position_name.strip() if position_name else "the target role"

    # Prompt Senario: to prevent halucination
    prompt = (
        f"You are a professional career advisor and hiring manager.\n\n"
        f"Generate a customized, well-structured cover letter for the position of '{position}' at '{company}'.\n\n"
        f"Job Description:\n'''\n{job_description}\n'''\n\n"
        f"Candidate Resume:\n'''\n{resume_content}\n'''\n\n"
        f"Strict Guidelines:\n"
        f"1. Highlight qualifications, tools, and achievements directly from the resume that match the job description.\n"
        f"2. DO NOT fabricate or assume experiences not explicitly stated in the resume.\n"
        f"3. Structure: Professional Salutation, Compelling Introduction, 2 Core Alignment Paragraphs (impact-driven), and a Professional Closing.\n"
        f"4. Maintain a confident, authentic, and professional tone."
    )

    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=1024
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=config
        )
        return response.text
    except Exception as e:
        return f"Error comminicating with LLM: {e}"

# Gradio UI
cover_letter_app = gr.Interface(
    fn=generate_cover_letter,
    flagging_mode="never",
    inputs=[
        gr.Textbox(
            label="Company Name",
            placeholder="e.g. Swisscom, Google, Novartis...",
        ),
        gr.Textbox(
            label="Position Name",
            placeholder="e.g. Senior QA Automation Engineer",
        ),
        gr.Textbox(
            label="Job Description Information",
            placeholder="Paste the target job description requirements here...",
            lines=8,
        ),
        gr.Textbox(
            label="Resume Content",
            placeholder="Paste your resume summary and experience bullet points here...",
            lines=8,
        ),
    ],
    outputs=gr.Textbox(label="Customized Cover Letter", lines=16),
    title="Customized Cover Letter Generator",
    description="Generate a tailored, evidence-backed cover letter mapped directly to job requirements.",
)

if __name__ == "__main__":
    cover_letter_app.launch(server_name="127.0.0.1", server_port=7860)

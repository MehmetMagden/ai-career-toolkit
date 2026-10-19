import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import gradio as gr

# Load environment variables
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.5-flash-lite"


def generate_career_advice(
    position_applied: str, job_description: str, resume_content: str
) -> str:
    """Analyzes candidate resume against target role requirements and generates actionable career advice."""
    if not resume_content.strip() or not job_description.strip():
        return (
            "Please provide both your Resume Content and the Job Description."
        )

    position = (
        position_applied.strip() if position_applied else "the target role"
    )

    # Structured strategic advisory prompt
    prompt = (
        f"You are an executive technical recruiter and career strategist.\n\n"
        f"Target Position: {position}\n\n"
        f"Job Description:\n'''\n{job_description}\n'''\n\n"
        f"Candidate Resume:\n'''\n{resume_content}\n'''\n\n"
        f"Provide a structured, actionable advisory report covering:\n"
        f"1. Skill & Tool Gap Analysis (identify missing or underemphasized technical competencies required by the job).\n"
        f"2. Resume Optimization Strategy (concrete bullet-point rewrites and phrasing adjustments to align with this role).\n"
        f"3. Interview Preparation Focus (key technical or behavioral topics the candidate is most likely to be tested on).\n"
        f"4. Competitive Advantage (unique strengths in the resume that should be emphasized).\n\n"
        f"Keep the tone professional, direct, and constructive."
    )

    # Detaylı bir analiz raporu için 1024 token ve dengeli tutarlılık için 0.5 sıcaklık
    config = types.GenerateContentConfig(
        temperature=0.5,
        max_output_tokens=1024,
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME, contents=prompt, config=config
        )
        return response.text
    except Exception as e:
        return f"Error communicating with LLM: {e}"


# Build Gradio Interface
career_advice_app = gr.Interface(
    fn=generate_career_advice,
    flagging_mode="never",
    inputs=[
        gr.Textbox(
            label="Position Applied For",
            placeholder="e.g. Senior QA Automation Engineer / DevOps Specialist",
        ),
        gr.Textbox(
            label="Job Description Information",
            placeholder="Paste the target job description requirements here...",
            lines=10,
        ),
        gr.Textbox(
            label="Your Resume Content",
            placeholder="Paste your current resume content here...",
            lines=10,
        ),
    ],
    outputs=gr.Textbox(label="Career Advisory Report", lines=16),
    title="AI Career Advisor",
    description="Analyze skill gaps, optimize positioning, and get targeted interview preparation advice for your target role.",
)

if __name__ == "__main__":
    career_advice_app.launch(server_name="127.0.0.1", server_port=7860)
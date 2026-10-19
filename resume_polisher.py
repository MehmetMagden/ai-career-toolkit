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

def polish_resume(position_name: str, resume_content: str, polish_prompt: str = "") -> str:
    """
    Polishes and optimizes resume bullet points/content based on target position
    and optional user-specified emphasis.
    """

    if not resume_content or not resume_content.strip():
        return "Please paste your resume content to polish."

    target_role = position_name.strip() if position_name and position_name.strip() else "Target"

    # Construct prompt based on whether specific instructions were provided
    if polish_prompt and polish_prompt.strip():
        prompt_use = (
            f"You are a professional resume writer and career strategist. \n\n"
            f"Target Position: {target_role}\n"
            f"Resume Content:\n'''\n{resume_content}\n'''\n\n"
            f"Specific Instruction: {polish_prompt}\n\n"
            f"Rewrite and polish the resume content following the instructions above. "
            f"Focus on quantifiable impact, strong action verbs, and clear relevance to role."
        )
    else:
        prompt_use = (
            f"You are a professional resume writer and career strategist.\n\n"
            f"Target Position: {target_role}\n"
            f"Resume content:\n'''{resume_content}\n'''\n\n"
            f"Suggest imrovements and rewrite this resume content to maximize its alignment, "
            f"clarity, and impact for a {target_role} role Return the polished version directly."
        ) 

    # Generation parameters
    config = types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=1024
    )       

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_use,
            config=config

        )
        return response.text
    except Exception as e:
        return f"Error communicating with LLM: {e}"

# Build Gradio Interface
resume_polish_application = gr.Interface(
    fn=polish_resume,
    flagging_mode="never",
    inputs=[
        gr.Textbox(label="Position Name", placeholder="e.g. Senior QA Automation Engineer / DevOps Engineer"),
        gr.Textbox(label="Resume Content", placeholder="Paste your resume bullet points or summary here...", lines=10),
        gr.Textbox(label="Polish Instruction (Optional)", placeholder="e.g. Emphasize CI/CD pipeline automation and 30% reduction in regression test cycle time...", lines=2),

    ],
    outputs=gr.Textbox(label="Polished Content", lines=12),
    title="Resume Polish Application",
    description="Enhance and tailor your resume bullet points for specific job roles using Gemini 3.5 Flash Lite"
)

if __name__ == "__main__":
    resume_polish_application.launch(server_name="127.0.0.1", server_port=7860)
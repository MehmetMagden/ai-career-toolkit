import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import gradio as gr

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3.5-flash-lite"


def call_llm(prompt: str, temp: float = 0.5) -> str:
    try:
        res = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temp, max_output_tokens=1024
            ),
        )
        return res.text
    except Exception as e:
        return f"Error: {e}"


def polish_resume(pos, content, instructions):
    if not content.strip():
        return "Please provide resume content."
    p = f"Target: {pos}\nResume:\n{content}\nInstructions: {instructions}\nRewrite and polish focusing on quantifiable impact."
    return call_llm(p, temp=0.7)


def generate_cover_letter(company, pos, jd, resume):
    if not resume.strip() or not jd.strip():
        return "Please provide both resume and job description."
    p = f"Write a tailored cover letter for {pos} at {company}.\nJD:\n{jd}\nResume:\n{resume}\nStrict rule: Do not hallucinate experiences not in resume."
    return call_llm(p, temp=0.7)


def career_advice(pos, jd, resume):
    if not resume.strip() or not jd.strip():
        return "Please provide both resume and job description."
    p = f"Role: {pos}\nJD:\n{jd}\nResume:\n{resume}\nAnalyze skill gaps, interview focus areas, and optimization points."
    return call_llm(p, temp=0.4)


with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="blue", neutral_hue="slate"),
    title="AI Career Toolkit",
) as demo:
    gr.Markdown("# 🎯 AI Career Application Toolkit")

    with gr.Tabs():
        with gr.TabItem("📄 Resume Enhancer"):
            with gr.Row():
                with gr.Column():
                    r_pos = gr.Textbox(label="Position Name")
                    r_content = gr.Textbox(label="Resume Content", lines=8)
                    r_inst = gr.Textbox(label="Instructions (Optional)", lines=2)
                    r_btn = gr.Button("Polish Resume", variant="primary")
                r_out = gr.Textbox(label="Result", lines=12)
            r_btn.click(
                polish_resume, inputs=[r_pos, r_content, r_inst], outputs=r_out
            )

        with gr.TabItem("✉️ Cover Letter"):
            with gr.Row():
                with gr.Column():
                    c_comp = gr.Textbox(label="Company Name")
                    c_pos = gr.Textbox(label="Position Name")
                    c_jd = gr.Textbox(label="Job Description", lines=6)
                    c_res = gr.Textbox(label="Resume Content", lines=6)
                    c_btn = gr.Button(
                        "Generate Cover Letter", variant="primary"
                    )
                c_out = gr.Textbox(label="Result", lines=14)
            c_btn.click(
                generate_cover_letter,
                inputs=[c_comp, c_pos, c_jd, c_res],
                outputs=c_out,
            )

        with gr.TabItem("🧭 Career Advisor"):
            with gr.Row():
                with gr.Column():
                    a_pos = gr.Textbox(label="Target Role")
                    a_jd = gr.Textbox(label="Job Description", lines=6)
                    a_res = gr.Textbox(label="Resume Content", lines=6)
                    a_btn = gr.Button("Analyze Profile", variant="primary")
                a_out = gr.Textbox(label="Analysis & Recommendations", lines=14)
            a_btn.click(
                career_advice, inputs=[a_pos, a_jd, a_res], outputs=a_out
            )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
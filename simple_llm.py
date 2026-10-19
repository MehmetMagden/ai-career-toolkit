import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Load (.env)
load_dotenv()

# 2. Start Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. Model settings
config = types.GenerateContentConfig(
    temperature=0.1,
    max_output_tokens=512
)

# 4. Prompt Questions
prompt_txt = "How to be a good Data Scientist?"

# 5. Call the model (Lite model: ultra-fast and high rate limits)
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt_txt,
    config=config
)

# 6. Print the result
print(response.text)
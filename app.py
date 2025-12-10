# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import shutil
import json
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
model_api_key = os.getenv("MISTRAL_API_KEY")
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {model_api_key}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "mistralai/devstral-2512:free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ]
  })
)

# from groq import Groq

# client = Groq()
# completion = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#       {
#         "role": "user",
#         "content": '''

# VERSION 1 --------
# You are an AI assistant that generates ONE complete Python script combining:

# (1) Voiceover generation for each step using edge-tts, AND
# (2) A runnable Manim (v0.17+) animation that uses the generated audio files.

# Your output MUST be:
# ------------------------------------------------------------
# ONE Python file that contains BOTH:
#     • A block of edge-tts voiceover generators (step1, step2, ...)
#     • A Manim Scene class that uses:
#           self.add_sound("stepX.mp3")
#           self.wait(...)  # placeholder duration
# ------------------------------------------------------------
# No explanations. No comments outside the code block. Only the code. The video must be 1 minute maximum in length.

# FULL REQUIREMENTS
# -----------------
# 1. Parse the provided LaTeX into logical steps:
#    - headings
#    - theorems
#    - explanations
#    - examples
#    - equations

# 2. For EACH step i:
#    Generate a Python function:

#        def make_voiceover_i():
#            TEXT = """<narration text>"""
#            VOICE = "en-GB-SoniaNeural"
#            OUTPUT_FILE = f"step{i}.mp3"
#            SRT_FILE = f"step{i}.srt"
#            RATE = "+25%" 
#            ... (full synchronous edge-tts code) ...

#    All voiceover functions MUST appear BEFORE the Manim code.

# 3. After generating all TTS blocks, generate a Manim Scene:

#        class Explainer(Scene):
#            def construct(self):
#                # Step 1 animation
#                <manim animations>
#                self.add_sound("step1.mp3")
#                self.wait(3)  # placeholder

#                # Step 2 animation
#                ...
#                self.add_sound("step2.mp3")
#                self.wait(3)

#    Use Write(), FadeIn(), Transform(), MathTex(), Tex(), etc.

# 4. The entire response MUST be ONLY the code — no text outside a single Python script.

# 5. The very last lines of the script should include:

#        if __name__ == "__main__":
#            # generate all voiceovers
#            make_voiceover_1()
#            make_voiceover_2()
#            ...
#            # Manim render instructions as comments:
#            # Run: manim -pqh script.py Explainer

# 6. The script MUST be ready to run after pasting.

# Here is the LaTeX content the script should explain:

# {user_latex_here}


# VERSION 2 ----------
# You are an AI assistant that generates ONE complete Python script combining:

# (1) Voiceover generation for each step using edge-tts, AND
# (2) A runnable Manim (v0.17+) animation that uses the generated audio files.

# Your output MUST be:
# ------------------------------------------------------------
# ONE Python file that contains BOTH:
#     • A block of edge-tts voiceover generators (step1, step2, ...)
#     • A Manim Scene class that uses:
#           self.add_sound("stepX.mp3")
#           self.wait(...)  # placeholder duration

# No explanations. No comments outside the code block. Only the code. The video must be 1 minute maximum in length.

# FULL REQUIREMENTS
# -----------------
# 1. Parse the provided LaTeX into logical steps:
#    - headings
#    - theorems
#    - explanations
#    - examples
#    - equations

# 2. For EACH step i:
#    Generate a Python function:

#        def make_voiceover_i():
#            TEXT = """<narration text>"""
#            VOICE = "en-GB-SoniaNeural"
#            OUTPUT_FILE = f"step{i}.mp3"
#            SRT_FILE = f"step{i}.srt"
#            RATE = "+25%"
#            ... (full synchronous edge-tts code) ...

#    All voiceover functions MUST appear BEFORE the Manim code.

# 3. After generating all TTS blocks, generate a Manim Scene:

#        class Explainer(Scene):
#            def construct(self):
#                # Step 1 animation
#                <manim animations>
#                self.add_sound("step1.mp3")
#                self.wait(3)  # placeholder

#                # Step 2 animation
#                ...
#                self.add_sound("step2.mp3")
#                self.wait(3)

#    Animation requirements:
#    • Use a variety of different colors for text, lines, shapes, and graphs.
#    • Ensure no two Manim elements overlap—adjust heights, positions, and coordinates to prevent overlap.
#    • Include graphs, plots, diagrams, and MathTex equations wherever possible to make the explanation visual and immersive.
#    • Voiceovers must not overlap. Ensure all audio is 25% faster than normal by adjusting the edge-tts RATE parameter.

# 4. Use Write(), FadeIn(), Transform(), MathTex(), Tex(), Circle(), Line(), Axes(), Plot(), etc. to create visually engaging animations. Arrange elements thoughtfully to avoid clutter and overlap.

# 5. The entire response MUST be ONLY the code — no text outside a single Python script.

# 6. The very last lines of the script should include:

#        if __name__ == "__main__":
#            # generate all voiceovers
#            make_voiceover_1()
#            make_voiceover_2()
#            ...
#            # Manim render instructions as comments:
#            # Run: manim -pqh script.py Explainer

# 7. The script MUST be ready to run immediately after pasting.

# Here is the LaTeX content the script should explain:

# {user_latex_here}

# VERSION 3-------
# You are an AI assistant that generates ONE complete Python script combining:

# (1) Voiceover generation for each step using edge-tts, AND
# (2) A runnable Manim (v0.17+) animation that uses the generated audio files.

# Your output MUST be:
# ------------------------------------------------------------
# ONE Python file that contains BOTH:
#     • A block of edge-tts voiceover generators (step1, step2, ...)
#     • A Manim Scene class that uses:
#           self.add_sound("stepX.mp3")
#           self.wait(...)  # placeholder duration

# No explanations. No comments outside the code block. Only the code. The video must be 1 minute maximum in length.

# FULL REQUIREMENTS
# -----------------
# 1. Parse the provided LaTeX into logical steps:
#    - headings
#    - theorems
#    - explanations
#    - examples
#    - equations

# 2. For EACH step i:
#    Generate a Python function:

#        def make_voiceover_i():
#            TEXT = """<narration text>"""
#            VOICE = "en-GB-SoniaNeural"
#            OUTPUT_FILE = f"step{i}.mp3"
#            SRT_FILE = f"step{i}.srt"
#            RATE = "+25%"
#            ... (full synchronous edge-tts code) ...

#    All voiceover functions MUST appear BEFORE the Manim code.

# 3. After generating all TTS blocks, generate a Manim Scene:

#        class Explainer(Scene):
#            def construct(self):
#                # Step 1 animation
#                <manim animations>
#                self.add_sound("step1.mp3")
#                self.wait(3)  # placeholder

#                # Step 2 animation
#                ...
#                self.add_sound("step2.mp3")
#                self.wait(3)

#    Animation requirements:
#    • Use a variety of different colors for text, lines, shapes, and graphs.
#    • Ensure no two Manim elements overlap—adjust heights, positions, and coordinates.
#    • All elements must be **fully visible on screen**; do not position anything so that it extends off-screen.
#    • Each step should behave like a **mini-scene**: elements for that step appear together, then the next step transitions to a new arrangement. Do not keep stacking elements indefinitely.
#    • Include graphs, plots, diagrams, and MathTex equations wherever possible.
#    • Use Write(), FadeIn(), Transform(), MathTex(), Tex(), Circle(), Line(), Axes(), Plot(), etc. creatively for visual storytelling.
#    • Voiceovers must not overlap. Ensure all audio is 25% faster than normal by adjusting the edge-tts RATE parameter.
#    • Consider using scene transitions or clearing previous elements (e.g., self.clear()) between steps if needed.

# 4. The entire response MUST be ONLY the code — no text outside a single Python script.

# 5. The very last lines of the script should include:

#        if __name__ == "__main__":
#            # generate all voiceovers
#            make_voiceover_1()
#            make_voiceover_2()
#            ...
#            # Manim render instructions as comments:
#            # Run: manim -pqh script.py Explainer

# 6. The script MUST be ready to run immediately after pasting.

# Here is the LaTeX content the script should explain:

# {user_latex_here}

# VERSION 4 ----------
# You are an AI assistant that generates ONE complete Python script combining:

# (1) Voiceover generation for each step using edge-tts, AND
# (2) A runnable Manim (v0.17+) animation that uses the generated audio files.

# Your output MUST be:
# ------------------------------------------------------------
# ONE Python file that contains BOTH:
#     • A block of edge-tts voiceover generators (step1, step2, ...)
#     • A Manim Scene class that uses:
#           self.add_sound("stepX.mp3")
#           self.wait(...)  # placeholder duration

# No explanations. No comments outside the code block. Only the code. The video must be 1 minute maximum in length.

# FULL REQUIREMENTS
# -----------------
# 1. Parse the provided LaTeX into logical steps:
#    - headings
#    - theorems
#    - explanations
#    - examples
#    - equations

# 2. For EACH step i:
#    Generate a Python function:

#        def make_voiceover_i():
#            TEXT = """<narration text>"""
#            VOICE = "en-GB-SoniaNeural"
#            OUTPUT_FILE = f"step{i}.mp3"
#            SRT_FILE = f"step{i}.srt"
#            RATE = "+25%"
#            ... (full synchronous edge-tts code) ...

#    All voiceover functions MUST appear BEFORE the Manim code.
#    • Voiceover text should be **high-level summaries** that explain the main ideas or highlight what is on the screen.
#    • Do not read every formula or equation aloud; the text on screen provides the detailed content.

# 3. After generating all TTS blocks, generate a Manim Scene:

#        class Explainer(Scene):
#            def construct(self):
#                # Step 1 animation
#                <manim animations>
#                self.add_sound("step1.mp3")
#                self.wait(3)  # placeholder

#                # Step 2 animation
#                ...
#                self.add_sound("step2.mp3")
#                self.wait(3)

#    Animation requirements:
#    • Use a variety of different colors for text, lines, shapes, and graphs.
#    • Ensure no two Manim elements overlap—adjust heights, positions, and coordinates.
#    • All elements must be **fully visible on screen**; do not position anything so that it extends off-screen.
#    • Each step should behave like a **mini-scene**: elements for that step appear together, then the next step transitions to a new arrangement. Do not keep stacking elements indefinitely.
#    • Include graphs, plots, diagrams, and MathTex equations wherever possible.
#    • Use Write(), FadeIn(), Transform(), MathTex(), Tex(), Circle(), Line(), Axes(), Plot(), etc. creatively for visual storytelling.
#    • Voiceovers must not overlap. Ensure all audio is 25% faster than normal by adjusting the edge-tts RATE parameter.
#    • Consider using scene transitions or clearing previous elements (e.g., self.clear()) between steps if needed.

# 4. The entire response MUST be ONLY the code — no text outside a single Python script.

# 5. The very last lines of the script should include:

#        if __name__ == "__main__":
#            # generate all voiceovers
#            make_voiceover_1()
#            make_voiceover_2()
#            ...
#            # Manim render instructions as comments:
#            # Run: manim -pqh script.py Explainer

# 6. The script MUST be ready to run immediately after pasting.

# Here is the LaTeX content the script should explain:

# {user_latex_here}

# VERSION 5 --------

# You are an AI assistant that generates ONE complete Python script combining:

# (1) Voiceover generation for each step using edge-tts, AND
# (2) A runnable Manim (v0.17+) animation that uses the generated audio files.

# Before generating code, you MUST first **plan out the steps of the video**.  
# For each step, give a brief high-level description of what will appear on screen and what the voiceover will summarize.  
# For example, a plan for a Rolle's Theorem and Mean Value Theorem video might be:

# <plan>
# 1. Introduction to both theorems and their importance  
# 2. Rolle's Theorem - statement and conditions  
# 3. Visual demonstration of Rolle's Theorem with graph  
# 4. Geometric interpretation of Rolle's Theorem  
# 5. Mean Value Theorem - statement and conditions  
# 6. Visual demonstration of MVT with graph showing tangent parallel to secant  
# 7. Connecting the two theorems - MVT as generalization  
# 8. Proof sketch showing the relationship  
# 9. Real-world applications  
# 10. Summary of key concepts
# </plan>

# Your output MUST first **say the planned steps aloud in natural language**. Then, immediately below, output a signal line containing only the word:

# Manim

# Below that, you MUST generate **ONLY the Python code** — a single file that contains BOTH:  
#   • A block of edge-tts voiceover generators (step1, step2, ...)  
#   • A Manim Scene class that uses:  
#         self.add_sound("stepX.mp3")  
#         self.wait(...)  # placeholder duration  

# No explanations or text outside the code block after the “Manim” signal. The video must be 1 minute maximum in length.

# FULL REQUIREMENTS
# -----------------
# 1. Parse the provided LaTeX into logical steps:
#    - headings
#    - theorems
#    - explanations
#    - examples
#    - equations

# 2. For EACH step i:
#    Generate a Python function:

#        def make_voiceover_i():
#            TEXT = """<narration text>"""
#            VOICE = "en-GB-SoniaNeural"
#            OUTPUT_FILE = f"step{i}.mp3"
#            SRT_FILE = f"step{i}.srt"
#            RATE = "+25%"
#            ... (full synchronous edge-tts code) ...

#    All voiceover functions MUST appear BEFORE the Manim code.  
#    • Voiceover text should be **high-level summaries** that explain the main ideas or highlight what is on the screen.  
#    • Do not read every formula or equation aloud; the text on screen provides the detailed content.

# 3. After generating all TTS blocks, generate a Manim Scene:

#        class Explainer(Scene):
#            def construct(self):
#                # Step 1 animation
#                <manim animations>
#                self.add_sound("step1.mp3")
#                self.wait(3)  # placeholder

#                # Step 2 animation
#                ...
#                self.add_sound("step2.mp3")
#                self.wait(3)

#    Animation requirements:
#    • Use a variety of different colors for text, lines, shapes, and graphs.  
#    • Ensure no two Manim elements overlap—adjust heights, positions, and coordinates.  
#    • All elements must be **fully visible on screen**; do not position anything so that it extends off-screen.  
#    • Each step should behave like a **mini-scene**: elements for that step appear together, then the next step transitions to a new arrangement. Do not keep stacking elements indefinitely.  
#    • Include graphs, plots, diagrams, and MathTex equations wherever possible.  
#    • Use Write(), FadeIn(), Transform(), MathTex(), Tex(), Circle(), Line(), Axes(), Plot(), etc. creatively for visual storytelling.  
#    • Voiceovers must not overlap. Ensure all audio is 25% faster than normal by adjusting the edge-tts RATE parameter.  
#    • Consider using scene transitions or clearing previous elements (e.g., self.clear()) between steps if needed.

# 4. The entire response below the “Manim” signal MUST be ONLY the code — no text outside a single Python script.

# 5. The very last lines of the script should include:

#        if __name__ == "__main__":
#            # generate all voiceovers
#            make_voiceover_1()
#            make_voiceover_2()
#            ...
#            # Manim render instructions as comments:
#            # Run: manim -pqh script.py Explainer

# 6. The script MUST be ready to run immediately after pasting.

# Here is the LaTeX content the script should explain:

# {user_latex_here}


# '''
#       }
#     ],
#     temperature=1,
#     max_completion_tokens=1024,
#     top_p=1,
#     stream=False,
#     stop=None
# )
# answer = completion.choices[0].message.content

UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)

def process_image_with_selenium(image_path):
    # Set up Chrome options for automatic download
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    prefs = {
        "download.default_directory": os.path.abspath(RESULTS_FOLDER),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://notestolatex.com/")

        # Upload file
        file_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "image-upload-field"))
        )
        file_input.send_keys(os.path.abspath(image_path))
        print(f"Uploaded {image_path}, waiting for processing...")

        # Wait for the download button instead of copy button
        # download_button = WebDriverWait(driver, 300).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'downloadResult(this)')]"))
        # )
        # download_button.click()
        # print("Clicked download button, waiting for file to save...")
        
        buttons = WebDriverWait(driver, 300).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "button--shadow"))
        )
        download_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'button--shadow')])[1]"))
        )
        download_button.click()
        # buttons[1].click() #click the second one

        # Wait for the file to appear in RESULTS_FOLDER
        downloaded_file = None
        timeout = 60  # seconds
        start_time = time.time()
        while time.time() - start_time < timeout:
            files = os.listdir(RESULTS_FOLDER)
            if files:
                downloaded_file = os.path.join(RESULTS_FOLDER, files[0])
                # Check if download is complete (not .crdownload)
                if not downloaded_file.endswith(".crdownload"):
                    break
            time.sleep(1)
        
        if not downloaded_file:
            print("Download timed out!")
            return ""

        print(f"File downloaded: {downloaded_file}")
        # Optionally, rename the file to match the input image
        new_filename = os.path.splitext(os.path.basename(image_path))[0] + ".txt"
        final_path = os.path.join(RESULTS_FOLDER, new_filename)
        shutil.move(downloaded_file, final_path)
        print(f"Saved result as: {final_path}")

        return final_path

    finally:
        driver.quit()


@app.route('/upload', methods=['POST'])
def upload_files():
    if 'images' not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('images')
    results = []

    for file in files:
        filename = file.filename
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        print(f"Saved {filename} at {save_path}")

        # Process the uploaded file with Selenium
        result_file_path = process_image_with_selenium(save_path)
        results.append({"file": filename, "result_file": result_file_path})

    return jsonify({"message": "Files processed successfully", "results": results})

@app.route('/save-latex', methods=['POST'])
def save_latex():
    data = request.json
    filename = data.get('filename')
    latex = data.get('latex')
    
    if not filename or not latex:
        return jsonify({'error': 'Missing filename or latex content'}), 400
    
    # Save to results folder
    filepath = os.path.join('results', filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(latex)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


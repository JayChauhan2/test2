from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from google import genai
from google.genai import types
import os
import json
import requests
import mimetypes
import shutil
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def clear_folder(folder_path):
    """Delete all files in a folder but keep the folder itself."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

@app.route('/extract-text', methods=['POST'])
def extractText():
    # 1. Clear uploads and results folders
    clear_folder(UPLOAD_FOLDER)
    clear_folder(RESULTS_FOLDER)

    # --- 1. Handle multiple uploaded images ---
    uploaded_files = request.files.getlist('images')

    if not uploaded_files or uploaded_files == [None]:
        return jsonify({"error": "No images uploaded"}), 400

    for file in uploaded_files:
        if file.filename == "":
            continue
        
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)
        print(f"Saved uploaded image: {save_path}")

    API_KEY = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=API_KEY)

    extracted_text = ""
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Skip directories
        if not os.path.isfile(file_path):
            continue

        mime_type, _ = mimetypes.guess_type(file_path)

        # Accept only JPEG/PNG images
        if mime_type not in ("image/jpeg", "image/png"):
            print(f"Skipping non-image file: {filename}")
            continue

        print(f"\nProcessing image: {filename}")

        with open(file_path, 'rb') as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
                (
                    "Extract all the text from this image and return it as plain text. "
                    "After extracting, carefully review the text and correct any mistakes "
                    "or misread characters. Preserve formatting like bullet points, "
                    "headings, or mathematical notation where possible."
                )
            ]
        )
        extracted_text += response.text + "\n"
    
    # Save to file
    results_file_path = os.path.join(RESULTS_FOLDER, "results.txt")
    with open(results_file_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    print(f"\nAll results saved to {results_file_path}")
    
    # Return the extracted text in the response
    return jsonify({
        "status": "success", 
        "results_file": results_file_path,
        "extracted_text": extracted_text
    })

def createVideo(user_latex_here):
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
            "content": f'''
    You are an AI assistant that generates ONE complete Python script combining:

    (1) Voiceover generation for each step using edge-tts, AND
    (2) A runnable Manim (v0.17+) animation that uses the generated audio files.

    Before generating code, you MUST first **plan out the steps of the video**.  
    For each step, give a brief high-level description of what will appear on screen and what the voiceover will summarize.  
    For example, a plan for a Rolle's Theorem and Mean Value Theorem video might be:

    <plan>
    1. Introduction to both theorems and their importance  
    2. Rolle's Theorem - statement and conditions  
    3. Visual demonstration of Rolle's Theorem with graph  
    4. Geometric interpretation of Rolle's Theorem  
    5. Mean Value Theorem - statement and conditions  
    6. Visual demonstration of MVT with graph showing tangent parallel to secant  
    7. Connecting the two theorems - MVT as generalization  
    8. Proof sketch showing the relationship  
    9. Real-world applications  
    10. Summary of key concepts
    </plan>

    Your output MUST first **say the planned steps aloud in natural language**. Then, immediately below, output a signal line containing only the word:

    Manim

    Below that, you MUST generate **ONLY the Python code** — a single file that contains BOTH:  
    • A block of edge-tts voiceover generators (step1, step2, ...)  
    • A Manim Scene class that uses:  
            self.add_sound("stepX.mp3")  
            self.wait(...)  # placeholder duration  

    No explanations or text outside the code block after the "Manim" signal. The video must be 1 minute maximum in length.

    FULL REQUIREMENTS
    -----------------
    1. Parse the provided LaTeX into logical steps:
    - headings
    - theorems
    - explanations
    - examples
    - equations

    2. For EACH step i:
    Generate a Python function:

        def make_voiceover_i():
            TEXT = """<narration text>"""
            VOICE = "en-GB-SoniaNeural"
            OUTPUT_FILE = f"step{i}.mp3"
            SRT_FILE = f"step{i}.srt"
            RATE = "+25%"
            ... (full synchronous edge-tts code) ...

    All voiceover functions MUST appear BEFORE the Manim code.  
    • Voiceover text should be **high-level summaries** that explain the main ideas or highlight what is on the screen.  
    • Do not read every formula or equation aloud; the text on screen provides the detailed content.

    3. After generating all TTS blocks, generate a Manim Scene:

        class Explainer(Scene):
            def construct(self):
                # Step 1 animation
                <manim animations>
                self.add_sound("step1.mp3")
                self.wait(3)  # placeholder

                # Step 2 animation
                ...
                self.add_sound("step2.mp3")
                self.wait(3)

    Animation requirements:
    • Use a variety of different colors for text, lines, shapes, and graphs.  
    • Ensure no two Manim elements overlap—adjust heights, positions, and coordinates.  
    • All elements must be **fully visible on screen**; do not position anything so that it extends off-screen.  
    • Each step should behave like a **mini-scene**: elements for that step appear together, then the next step transitions to a new arrangement. Do not keep stacking elements indefinitely.  
    • Include graphs, plots, diagrams, and MathTex equations wherever possible.  
    • Use Write(), FadeIn(), Transform(), MathTex(), Tex(), Circle(), Line(), Axes(), Plot(), etc. creatively for visual storytelling.  
    • Voiceovers must not overlap. Ensure all audio is 25% faster than normal by adjusting the edge-tts RATE parameter.  
    • Consider using scene transitions or clearing previous elements (e.g., self.clear()) between steps if needed.

    4. The entire response below the "Manim" signal MUST be ONLY the code — no text outside a single Python script.

    5. The very last lines of the script should include:

        if __name__ == "__main__":
            # generate all voiceovers
            make_voiceover_1()
            make_voiceover_2()
            ...
            # Manim render instructions as comments:
            # Run: manim -pqh script.py Explainer

    6. The script MUST be ready to run immediately after pasting.

    Here is the LaTeX content the script should explain:

    {user_latex_here}

    '''
        }
        ]
    })
    )
    data = response.json()

    # Extract the assistant message content
    llm_output = data["choices"][0]["message"]["content"]

    return llm_output


@app.route('/save-changed-notes', methods=['POST'])
def save_changed_notes():
    """Save edited notes content back to file"""
    try:
        data = request.json
        content = data.get('changedNotes')
        filename = data.get('filename', 'results.txt')
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        filepath = os.path.join(RESULTS_FOLDER, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Saved content to {filepath}")
        return jsonify({'success': True, 'message': 'Content saved successfully'}), 200
    
    except Exception as e:
        print(f"Error in save-changed-notes: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
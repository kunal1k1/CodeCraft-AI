import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY was not found in .env")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "CodeCraft AI Backend Running!"


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "Prompt is empty"}), 400

        master_prompt = f""" 
You are CodeCraft AI, an expert frontend website developer. 

USER REQUEST: 
{prompt} 

DESIGN REQUIREMENTS: 

Build websites that look like modern startups and premium brands. 

Design quality should be similar to: 
- Apple 
- Stripe 
- Framer 
- Linear 
- Vercel 
- Tesla 
- Airbnb 
- Nike 

Use: 
✓ Beautiful gradients 
✓ Glassmorphism 
✓ Modern cards 
✓ Hover effects 
✓ Smooth animations 
✓ Scroll animations 
✓ Premium typography 
✓ Rounded corners 
✓ Shadows 
✓ Modern navbar 
✓ Hero section with CTA buttons 
✓ Feature cards 
✓ Testimonials section 
✓ Pricing section when relevant 
✓ Contact section 
✓ Footer section 
✓ Mobile responsive design 

Avoid: 
✗ Plain white backgrounds 
✗ Basic HTML layouts 
✗ Old-school designs 
✗ Default browser styles 
✗ Simple blue buttons 
✗ Unstyled forms 
✗ Generic websites 

CRITICAL NAVIGATION RULES FOR IFRAME PREVIEW:
1. NEVER use empty href="" or bare href="#" on <a> tags, as this reloads the host app inside the preview iframe.
2. For smooth scrolling to sections, use matching IDs (e.g., <a href="#about"> and <section id="about">).
3. For buttons or dummy links that do not scroll anywhere, use <a href="javascript:void(0)"> or handle click events with JavaScript e.preventDefault().
4. Form submit buttons must use type="button" or have event.preventDefault() on submit so they do not reload the iframe.

The website must feel premium and professional. 

Use modern CSS techniques: 
- CSS Grid 
- Flexbox 
- Gradients 
- Backdrop blur 
- Animations 
- Transitions 

Every generated website should look production-ready. 

VISUAL QUALITY RULES: 

Create a wow effect. 

The first screen (hero section) should immediately impress the user. 

Use: 
- Large bold headings 
- Beautiful gradients 
- Modern illustrations using CSS 
- Background glow effects 
- Floating cards 
- Attractive CTA buttons 

The website should look like it was designed by a professional UI/UX designer. 

VERY IMPORTANT: 

The response must start with: 

<!DOCTYPE html> 

and end with: 

</html> 

Return raw HTML only. 
"""

        print("Generating website with Gemini...")

        # Generate using Gemini
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=master_prompt,
        )

        website = response.text

        # Clean markdown code fences if model adds them
        website = (
            website.replace("```html", "")
            .replace("```HTML", "")
            .replace("```", "")
            .strip()
        )

        print("Website generated successfully!")

        return jsonify({"website": website})

    except Exception as e:
        print("ERROR:", repr(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting CodeCraft AI Backend on [http://127.0.0.1:5000](http://127.0.0.1:5000)")
    app.run(host="127.0.0.1", port=5000, debug=True)

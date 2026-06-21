from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "CodeCraft AI Backend Running!"

@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    prompt = data.get("prompt", "")

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

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": master_prompt
        }
    ],
    temperature=0.7,
    max_tokens=6000
)

    website = response.choices[0].message.content

    website = website.replace("```html", "")
    website = website.replace("```HTML", "")
    website = website.replace("```", "")
    website = website.strip()

    return jsonify({
        "website": website
    })

if __name__ == "__main__":
    app.run(debug=True)
import re
from dotenv import dotenv_values
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

class ColorPaletteGenerator:
    def __init__(self):
        config = dotenv_values("config/.env")
        self.client = OpenAI(api_key=config["OPENAI_API_KEY"])

    def generate_color_palette(self, text_prompt):
        prompt = f"""
        You are a color palette generating assistant that responds to text prompts for color palettes. You should generate color palettes that fit the theme, mood, or description of the text prompt. The color palette should be a list of hexadecimal color codes between 2 and 8 colors.

        Desired Format: a list of hexadecimal color codes without any additional text or formatting

        Text: {text_prompt}

        Result:
        """

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )

        # Extract hexadecimal color codes using a regular expression
        palette = re.findall(r'#[0-9A-Fa-f]{6}', completion.choices[0].message.content)
        return palette


app = Flask(__name__, template_folder="templates")

# Instantiate the color palette generator
generator = ColorPaletteGenerator()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    text_prompt = request.form["text_prompt"]
    colors = generator.generate_color_palette(text_prompt)
    return jsonify({"colors": colors})  # Return JSON response


if __name__ == "__main__":
    app.run(debug=True)

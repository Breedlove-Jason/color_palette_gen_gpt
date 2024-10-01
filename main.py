import re
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values("config/.env")

client = OpenAI(
    api_key=config["OPENAI_API_KEY"]
)

prompt = """
You are a color palette generating assistant that responds to text prompts for color palettes. You should generate color palettes that fit the theme, mood, or description of the text prompt. The color palette should be a list of hexadecimal color codes between 2 and 8 colors.

Desired Format: a list of hexadecimal color codes without any additional text or formatting

Text: A painting by Damien Hirst

Result:
"""

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt},
    ],
)

# Extract hexadecimal color codes using a regular expression
color_palette = re.findall(r'#[0-9A-Fa-f]{6}', completion.choices[0].message.content)

def display_color_palette(colors):
    fig, ax = plt.subplots(1, len(colors), figsize=(len(colors) * 2, 2))
    for i, color in enumerate(colors):
        ax[i].add_patch(plt.Rectangle((0, 0), 1, 1, color=color))
        ax[i].axis('off')
    plt.show()

display_color_palette(color_palette)

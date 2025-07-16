from flask import Flask, render_template_string, request
from pyramid_plot import create_note_pyramid, export_pyramid
import plotly.io as pio
import pandas as pd
import os

app = Flask(__name__)

# Load your dataset
df = pd.read_csv("perfume_list.csv")
df.dropna(subset=["Top", "Middle", "Base"], inplace=True)

# Ensure export folder exists
os.makedirs("static/pyramids", exist_ok=True)

@app.route("/")
def index():
    perfume_name = request.args.get("perfume")
    if not perfume_name or perfume_name not in df["Perfume"].values:
        perfume_name = df.iloc[0]["Perfume"]

    row = df[df["Perfume"] == perfume_name].iloc[0]

    top = [note.strip() for note in row["Top"].split(",")]
    middle = [note.strip() for note in row["Middle"].split(",")]
    base = [note.strip() for note in row["Base"].split(",")]

    fig = create_note_pyramid(top, middle, base, title=perfume_name)
    plot_html = pio.to_html(fig, full_html=False)

    # ✅ Export both PNG and SVG
    safe_filename = perfume_name.replace(" ", "_").replace("/", "_")
    png_path = f"static/pyramids/{safe_filename}.png"
    svg_path = f"static/pyramids/{safe_filename}.svg"
    export_pyramid(fig, png_path, format="png")
    export_pyramid(fig, svg_path, format="svg")

    options_html = "".join(
        f'<option value="{name}" {"selected" if name == perfume_name else ""}>{name}</option>'
        for name in sorted(df["Perfume"].unique())
    )

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Perfume Note Pyramid</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 2rem;
                background-color: #f7f9fb;
                color: #333;
            }
            select {
                font-size: 1rem;
                padding: 0.5rem;
                margin-bottom: 1rem;
                width: 300px;
            }
            .download-button {
                display: inline-block;
                margin-top: 1rem;
                padding: 0.6rem 1rem;
                background-color: #0079C1;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <h2>Choose a Perfume:</h2>
        <form method="get">
            <select name="perfume" onchange="this.form.submit()">
                {{ options_html | safe }}
            </select>
        </form>
        {{ plot_html | safe }}
        <br>
        <a class="download-button" href="{{ png_path }}" download>Download as PNG</a>
        <a class="download-button" href="{{ svg_path }}" download>Download as SVG</a>
    </body>
    </html>
    """, plot_html=plot_html, options_html=options_html,
         png_path="/" + png_path, svg_path="/" + svg_path)

if __name__ == "__main__":
    app.run(debug=True)



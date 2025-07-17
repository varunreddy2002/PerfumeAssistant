from flask import Flask, render_template, request, url_for
from pyramid_plot import create_note_pyramid, export_pyramid, create_ring_diagram
import plotly.io as pio
import pandas as pd
import os

app = Flask(__name__)
df = pd.read_csv("perfume_list.csv")
df.dropna(subset=["Top", "Middle", "Base"], inplace=True)
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

    fig_pyramid = create_note_pyramid(top, middle, base, title=perfume_name)
    fig_ring = create_ring_diagram(top, middle, base)

    pyramid_html = fig_pyramid  # already a Markup-wrapped SVG string
    ring_html = pio.to_html(fig_ring, full_html=False)

    options_html = "".join(
        f'<option value="{name}" {"selected" if name == perfume_name else ""}>{name}</option>'
        for name in sorted(df["Perfume"].unique())
    )

    return render_template("index.html",
        pyramid_html=pyramid_html,
        ring_html=ring_html,
        top_notes=top,             # ✅ List
        middle_notes=middle,       # ✅ List
        base_notes=base,           # ✅ List
        options_html=options_html
    )




if __name__ == "__main__":
    app.run(debug=True)

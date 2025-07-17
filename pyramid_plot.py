from markupsafe import Markup

def create_note_pyramid(top_notes, middle_notes, base_notes, title="Fragrance Note Pyramid"):
    from markupsafe import Markup

    svg_template = f"""
    <svg width="240" height="280" viewBox="0 0 200 240" xmlns="http://www.w3.org/2000/svg" style="font-family: 'DM Sans', sans-serif;">
      <defs>
        <linearGradient id="topGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#A0E7E5" />
          <stop offset="100%" stop-color="#72D6C9" />
        </linearGradient>
        <linearGradient id="middleGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#B4F8C8" />
          <stop offset="100%" stop-color="#6EDC93" />
        </linearGradient>
        <linearGradient id="baseGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#FBE7C6" />
          <stop offset="100%" stop-color="#FDC490" />
        </linearGradient>
      </defs>

      <!-- Top Layer -->
      <polygon points="100,20 160,80 40,80" fill="url(#topGradient)" opacity="0.95">
        <animate attributeName="opacity" values="0.9;1;0.9" dur="5s" repeatCount="indefinite" />
      </polygon>
      <text x="100" y="55" text-anchor="middle" font-size="12" fill="#333" font-weight="bold">Top Notes</text>
      <text x="100" y="70" text-anchor="middle" font-size="10" fill="#1d1d1d">
        {"".join(f'<tspan x="100" dy="1.1em">{note}</tspan>' for note in top_notes)}
        </text>


      <!-- Middle Layer -->
      <polygon points="40,80 160,80 180,160 20,160" fill="url(#middleGradient)" opacity="0.95">
        <animate attributeName="opacity" values="0.9;1;0.9" dur="5s" begin="0.5s" repeatCount="indefinite" />
      </polygon>
      <text x="100" y="115" text-anchor="middle" font-size="12" fill="#fff" font-weight="bold">Middle Notes</text>
      <text x="100" y="130" text-anchor="middle" font-size="10" fill="#ffffff">
        {"".join(f'<tspan x="100" dy="1.1em">{note}</tspan>' for note in middle_notes)}
        </text>

      <!-- Base Layer -->
      <polygon points="20,160 180,160 150,220 50,220" fill="url(#baseGradient)" opacity="0.95">
        <animate attributeName="opacity" values="0.9;1;0.9" dur="5s" begin="1s" repeatCount="indefinite" />
      </polygon>
      <text x="100" y="190" text-anchor="middle" font-size="12" fill="#333" font-weight="bold">Base Notes</text>
      <text x="100" y="205" text-anchor="middle" font-size="10" fill="#2a2a2a">
        {"".join(f'<tspan x="100" dy="1.1em">{note}</tspan>' for note in base_notes)}
        </text>
    </svg>
    """

    return Markup(svg_template)


# --- Optional Bonus: Export to PNG or SVG ---
def export_pyramid(fig, filename="pyramid.png", format="png"):
    """
    Save the pyramid figure to PNG or SVG format.

    Requires: pip install kaleido
    Usage:
        fig = create_note_pyramid(...)
        export_pyramid(fig, "my_pyramid.svg", format="svg")
    """
    fig.write_image(filename, format=format)

import plotly.graph_objects as go

def create_ring_diagram(top, middle, base):
    import plotly.graph_objects as go

    all_notes = top + middle + base
    all_levels = (["Top Notes"] * len(top)) + (["Middle Notes"] * len(middle)) + (["Base Notes"] * len(base))

    # Aesthetic pastel color palette
    colors = {
        "Top Notes": "#ffe6ec",      # soft rose
        "Middle Notes": "#d1e8ff",   # baby blue
        "Base Notes": "#e0ffe0"      # mint green
    }

    border_colors = {
        "Top Notes": "#ffb3c6",
        "Middle Notes": "#a6d4ff",
        "Base Notes": "#b2ffb2"
    }

    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=all_notes,
        values=[1] * len(all_notes),
        hole=0.5,
        marker=dict(
            colors=[colors[lvl] for lvl in all_levels],
            line=dict(color=[border_colors[lvl] for lvl in all_levels], width=2)
        ),
        textinfo='label',
        textfont=dict(size=13, family="DM Sans"),
        rotation=90,
        sort=False,
        direction="clockwise",
        hoverinfo='label+percent',
    ))

    fig.update_layout(
        title=dict(text="Fragrance Wheel", font=dict(size=16, family="Playfair Display"), x=0.5),
        showlegend=False,
        height=300,
        width=300,
        margin=dict(t=50, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig




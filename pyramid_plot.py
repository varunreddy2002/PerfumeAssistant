import plotly.graph_objects as go

def create_note_pyramid(top_notes, middle_notes, base_notes, title="Fragrance Note Pyramid"):
    layers = [
        ("Top Notes", top_notes, "#B3DDF2"),       # Light blue
        ("Middle Notes", middle_notes, "#4FA6D8"), # Medium blue
        ("Base Notes", base_notes, "#0079C1")      # Dark IFF blue
    ]

    fig = go.Figure()

    widths = [0.3, 0.6, 1.0]
    y_levels = [0.75, 0.5, 0.25]
    layer_height = 0.25  # vertical height for each layer

    # Calculate dynamic height based on total number of notes (approx 30px per note)
    total_notes = sum(len(notes) for _, notes, _ in layers)
    height_px = max(400, total_notes * 30)  # minimum 400px height

    # Dynamic font size: smaller if many notes
    font_size = 13 if total_notes <= 10 else max(9, 20 - total_notes)

    for i, (layer_name, notes, color) in enumerate(layers):
        width = widths[i]
        y = y_levels[i]
        half_width = width / 2
        next_half = widths[i+1]/2 if i+1 < len(widths) else 0

        x_points = [-half_width, half_width, next_half, -next_half]
        y_points = [y, y, y - layer_height, y - layer_height]

        note_text = "<br>".join(notes)

        # Draw colored block
        fig.add_trace(go.Scatter(
            x=x_points + [x_points[0]],
            y=y_points + [y_points[0]],
            fill="toself",
            mode="lines",
            name=layer_name,
            hoverinfo="text",
            text=[note_text]*5,
            fillcolor=color,
            line=dict(color='white', width=2),
            showlegend=False
        ))

        # Add text inside each layer
        fig.add_trace(go.Scatter(
            x=[0],
            y=[y - layer_height / 2],
            text=[f"<b>{layer_name}</b><br>{note_text}"],
            mode="text",
            showlegend=False,
            hoverinfo='skip',
            cliponaxis=False,
            textfont=dict(size=font_size, color="white" if i == 2 else "black")
        ))

    fig.update_layout(
        title=title,
        height=height_px,
        width=600,
        xaxis=dict(visible=False, range=[-0.7, 0.7]),
        yaxis=dict(visible=False, range=[0, 1]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=20, l=50, r=50),
        font=dict(family="Arial", color="#333")
    )

    return fig


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

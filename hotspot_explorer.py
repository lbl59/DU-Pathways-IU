from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent


@st.cache_data(show_spinner=False)
def _load_image_as_data_uri(path: Path) -> tuple[str, int, int]:
    img = Image.open(path).convert("RGB")
    width, height = img.size
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=90)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}", width, height


def render_hotspot_explorer(
    *,
    page_title: str,
    page_heading: str,
    intro: str,
    image_relpath: str,
    hotspots: list[dict],
    about_text: str,
    state_key: str,
    marker_color: str = "#8B0000",
) -> None:
    """Render a static figure overlaid with clickable, numbered hotspots.

    This is the shared rendering engine behind every "Figure N Explorer" page
    in ``pages/``. Each page just supplies its own figure image, its own list
    of hotspot dicts (each with ``id``, ``x``, ``y``, ``panel``, ``title``,
    ``text``), and a unique ``state_key`` so that multiple explorer pages can
    coexist without clobbering each other's ``st.session_state``.

    Parameters
    ----------
    page_title:
        Browser-tab / ``st.set_page_config`` title.
    page_heading:
        Heading shown via ``st.title`` at the top of the page.
    intro:
        Intro paragraph shown under the heading.
    image_relpath:
        Path to the figure image, relative to the repo root
        (e.g. ``"figures/results_fig2_robustness.jpg"``).
    hotspots:
        List of dicts, each with keys ``id``, ``x``, ``y`` (pixel coordinates
        in source-image space, origin top-left), ``panel``, ``title``, and
        ``text``. The first hotspot in the list is selected by default.
    about_text:
        Text shown inside the "About this page" expander.
    state_key:
        Unique prefix for this page's ``st.session_state``/widget keys.
    marker_color:
        Hex color for the hotspot markers.
    """
    st.set_page_config(page_title=page_title, layout="wide")

    image_path = REPO_ROOT / image_relpath
    st.title(page_heading)
    st.write(intro)

    if not image_path.exists():
        st.error(f"Could not find the figure at {image_path}. Has the file moved?")
        st.stop()

    if not hotspots:
        st.error("No hotspots defined for this page.")
        st.stop()

    img_uri, img_w, img_h = _load_image_as_data_uri(image_path)

    id_to_hotspot = {h["id"]: h for h in hotspots}

    # -----------------------------------------------------------------
    # Build the interactive figure: static image + clickable hotspot markers.
    # -----------------------------------------------------------------
    fig = go.Figure()

    fig.add_layout_image(
        dict(
            source=img_uri,
            xref="x",
            yref="y",
            x=0,
            y=0,
            sizex=img_w,
            sizey=img_h,
            sizing="stretch",
            layer="below",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[h["x"] for h in hotspots],
            y=[h["y"] for h in hotspots],
            mode="markers+text",
            text=[str(i + 1) for i in range(len(hotspots))],
            textfont=dict(color="white", size=12, family="Arial Black"),
            marker=dict(
                size=26,
                color=marker_color,
                opacity=0.85,
                line=dict(color="white", width=2),
            ),
            customdata=[h["id"] for h in hotspots],
            hovertext=[f"{h['panel']}: {h['title']}" for h in hotspots],
            hoverinfo="text",
            name="callouts",
        )
    )

    fig.update_xaxes(visible=False, range=[0, img_w])
    fig.update_yaxes(visible=False, range=[img_h, 0], scaleanchor="x")
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=760,
        plot_bgcolor="white",
        dragmode="pan",
    )

    ids_in_order = [h["id"] for h in hotspots]
    labels = [f"{i + 1}. [{h['panel']}] {h['title']}" for i, h in enumerate(hotspots)]
    id_to_label = dict(zip(ids_in_order, labels))
    label_to_id = dict(zip(labels, ids_in_order))

    radio_key = f"{state_key}_radio_choice"
    plot_key = f"{state_key}_plot"

    # The radio widget below owns the "current selection" state directly (via
    # its key), so there's a single source of truth. We only ever *write* to
    # that key before the widget is instantiated (e.g. from a plotly click),
    # never after.
    if radio_key not in st.session_state:
        st.session_state[radio_key] = labels[0]

    col_fig, col_callout = st.columns([2.2, 1], gap="large")

    with col_fig:
        event = st.plotly_chart(
            fig,
            width="stretch",
            on_select="rerun",
            selection_mode=("points",),
            key=plot_key,
            config={"scrollZoom": True, "displayModeBar": True},
        )

        # A click on a marker updates the selected callout. Plotly reports
        # customdata per-point as a list (e.g. ["panel_b_ideal"]), so unwrap it.
        if event and event.get("selection", {}).get("points"):
            clicked = event["selection"]["points"][0]
            clicked_customdata = clicked.get("customdata")
            clicked_id = clicked_customdata[0] if clicked_customdata else None
            if clicked_id in id_to_label:
                st.session_state[radio_key] = id_to_label[clicked_id]

    with col_callout:
        st.subheader("Callouts")
        picked_label = st.radio(
            "Or pick a callout directly:",
            options=labels,
            key=radio_key,
            label_visibility="collapsed",
        )
        hotspot = id_to_hotspot[label_to_id[picked_label]]
        st.markdown("---")
        st.markdown(f"### {hotspot['title']}")
        st.caption(hotspot["panel"])
        st.write(hotspot["text"])

    st.markdown("---")
    with st.expander("About this page"):
        st.write(about_text)

from __future__ import annotations

from hotspot_explorer import render_hotspot_explorer

HOTSPOTS = [
    dict(
        id="overview",
        x=350, y=20, panel="Overview",
        title="The big picture",
        text=(
            "This figure drills into *when* and *how often* each utility "
            "actually builds its available infrastructure options, across 500 "
            "perturbed instances of the two compromise strategies from Figure "
            "5. The left column, panels (a)-(c), is the **baseline compromise**; "
            "the right column, panels (d)-(f), is the **IU compromise**. Each "
            "row is one utility. Within a subplot, the box plot (left) shows "
            "the *timing* of first construction — its spread across all "
            "perturbed instances, with the white circle marking the original, "
            "unperturbed timing. The bar plot (right) shows *how often* an "
            "option gets built at all, again relative to the original (white "
            "circle) as a baseline."
        ),
    ),
    dict(
        id="watertown_baseline", x=180, y=130, panel="(a) Watertown — baseline",
        title="Watertown, baseline compromise: New River Reservoir around Year 38",
        text=(
            "Under the baseline compromise, Watertown and Fallsland's jointly "
            "financed New River Reservoir is built around Year 38. The other "
            "options (College Rock expansions, Water Reuse facilities) fill "
            "out the rest of Watertown's more limited baseline infrastructure "
            "pathway."
        ),
    ),
    dict(
        id="watertown_iu", x=520, y=130, panel="(d) Watertown — IU",
        title="Watertown, IU compromise: New River delayed, other options prioritized instead",
        text=(
            "Under the IU compromise, the joint New River Reservoir investment "
            "is delayed to roughly Year 42 (versus Year 38 under baseline). "
            "Instead, Watertown prioritizes building the College Rock "
            "Reservoir expansion and a second water reuse facility first — "
            "infrastructure it has full agency over — before committing to the "
            "shared reservoir. This limits Watertown's early exposure to "
            "implementation uncertainty in its partners' actions, even though "
            "it adds to Watertown's infrastructure NPC (see Figure 5a)."
        ),
    ),
    dict(
        id="dryville_baseline", x=180, y=350, panel="(b) Dryville — baseline",
        title="Dryville, baseline compromise: Sugar Creek Reservoir around Year 37",
        text=(
            "Dryville's largest infrastructure option, the Sugar Creek "
            "Reservoir, is built later here — around Year 37 — under the "
            "baseline compromise."
        ),
    ),
    dict(
        id="dryville_iu", x=520, y=350, panel="(e) Dryville — IU",
        title="Dryville, IU compromise: Sugar Creek built earlier, and more often",
        text=(
            "Under the IU compromise, Dryville constructs the Sugar Creek "
            "Reservoir noticeably earlier — around **Year 32** versus Year 37 "
            "under baseline — and builds it more frequently across all "
            "perturbed SOWs. Yet Figure 5(b) shows Dryville's infrastructure "
            "NPC stays similar under both compromises: Dryville offsets the "
            "earlier, more frequent build by leaning more on flexible, "
            "short-term drought-mitigation actions, only building new supply "
            "capacity when it's genuinely needed."
        ),
    ),
    dict(
        id="fallsland_baseline", x=180, y=490, panel="(c) Fallsland — baseline",
        title="Fallsland, baseline compromise",
        text=(
            "Fallsland's infrastructure timing under the baseline compromise "
            "is tied to the same jointly financed New River Reservoir shown in "
            "panel (a), plus its own water reuse facility."
        ),
    ),
    dict(
        id="fallsland_iu", x=520, y=490, panel="(f) Fallsland — IU",
        title="Fallsland, IU compromise: more variable timing, but far less frequent construction",
        text=(
            "Fallsland's infrastructure timing becomes more variable under the "
            "IU compromise, but Fallsland also builds new infrastructure "
            "across far fewer perturbed SOWs than under the baseline "
            "compromise — most strikingly, it de-prioritizes its water reuse "
            "facility so heavily that it's constructed in **fewer than 2%** of "
            "all SOWs. The IU-DU search recognizes that the shared New River "
            "Reservoir already exposes Fallsland to implementation "
            "uncertainty, and limits any further exposure by not committing "
            "to the water reuse facility. Despite building less often, "
            "Fallsland achieves higher robustness under the IU compromise "
            "(Figure 5d)."
        ),
    ),
    dict(
        id="legend", x=350, y=655, panel="Legend",
        title="Reading the box-and-bar plots",
        text=(
            "In each box plot, the colored circle marks the median first-"
            "construction week across all 500 perturbed instances, the box "
            "spans the 25th-75th percentile, and the white circle marks the "
            "original unperturbed strategy's timing. In each bar plot, bar "
            "length shows median construction frequency across all "
            "perturbations, again relative to the original (white circle). A "
            "bigger gap between a bar and its white circle means "
            "implementation uncertainty changed how often that option gets "
            "built."
        ),
    ),
]

render_hotspot_explorer(
    page_title="Figure 6 - Infrastructure Timing & Frequency",
    page_heading="Figure 6: Infrastructure Construction Timing and Frequency — Interactive Explorer",
    intro=(
        "This figure compares *when* and *how often* each utility builds its "
        "infrastructure options across 500 perturbed instances of the "
        "**baseline compromise** (left column) and **IU compromise** (right "
        "column) strategies introduced in Figure 5. Click a numbered marker on "
        "the figure — or pick a callout from the list below it — to see what "
        "that part of the plot is showing."
    ),
    image_relpath="figures/results_fig6_infra_dist.jpg",
    hotspots=HOTSPOTS,
    state_key="fig6",
    about_text=(
        "This explorer overlays clickable hotspots on the published static "
        "figure (`figures/results_fig6_infra_dist.jpg`). Callout text is "
        "grounded in Section 5.5 of the accompanying manuscript (note: this "
        "section's heading is incomplete in the source draft), including the "
        "reported Year 32 vs. Year 37 Sugar Creek Reservoir timing for "
        "Dryville, the Year 38 vs. Year 42 New River Reservoir timing for "
        "Watertown/Fallsland, and the <2% construction-frequency figure for "
        "Fallsland's water reuse facility under the IU compromise."
    ),
)

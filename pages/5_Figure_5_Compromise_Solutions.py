from __future__ import annotations

from hotspot_explorer import render_hotspot_explorer

HOTSPOTS = [
    dict(
        id="overview",
        x=430, y=15, panel="Overview",
        title="The big picture",
        text=(
            "This figure zooms in on two specific, hand-picked strategies: "
            "the **baseline compromise** (green) and the **IU compromise** "
            "(dark orange/brown) — each chosen from its respective strategy "
            "set using a 'Social Planner' approach that balances all three "
            "utilities' interests. Both are highly cooperative strategies "
            "built around shared infrastructure investment. Panels (a)-(c) "
            "compare their performance tradeoffs under worst-case 10th "
            "percentile (WC10) conditions for each utility; panel (d) compares "
            "their robustness; panel (e) compares their performance "
            "degradation. Gray lines/points are every other pathway strategy, "
            "for context."
        ),
    ),
    dict(
        id="panel_a_watertown", x=350, y=150, panel="(a) Watertown",
        title="Watertown: the IU compromise spends more on infrastructure",
        text=(
            "The IU compromise (dark orange) spikes noticeably on the "
            "Infrastructure NPC axis relative to the baseline compromise "
            "(green). Watertown has the largest supply-to-demand ratio and "
            "the biggest Lake Michael allocation of any Sedento Valley "
            "utility, so infrastructure built here — mainly water treatment "
            "plant expansions — can boost the *whole region's* robustness by "
            "letting more water flow to Dryville and Fallsland via transfers, "
            "while the transfer revenue helps Watertown service its own new "
            "debt."
        ),
    ),
    dict(
        id="panel_b_dryville", x=350, y=440, panel="(b) Dryville",
        title="Dryville: similar infrastructure cost under both compromises",
        text=(
            "Dryville's Infrastructure NPC is fairly similar whether it "
            "follows the baseline or IU compromise. Figure 6 later shows why: "
            "under the IU compromise, Dryville leans more on flexible, "
            "short-term drought-mitigation actions, letting it build new "
            "supply infrastructure only when it's truly needed rather than "
            "on a fixed schedule."
        ),
    ),
    dict(
        id="panel_c_fallsland", x=350, y=700, panel="(c) Fallsland",
        title="Fallsland: the baseline compromise is financially riskiest here",
        text=(
            "The baseline compromise (green) consistently incurs higher "
            "drought mitigation costs than the IU compromise across all three "
            "utilities, but the effect is strongest for Fallsland, where the "
            "baseline compromise reaches a drought mitigation cost of roughly "
            "**25% of annual volumetric revenue** — the combined result of "
            "short-term revenue losses during drought and Fallsland's share of "
            "the debt from costly shared infrastructure."
        ),
    ),
    dict(
        id="axis_labels", x=430, y=900, panel="Axes",
        title="Reading the WC10 performance axes",
        text=(
            "Each parallel axis is one performance objective evaluated under "
            "worst-case 10th-percentile (WC10) conditions: Reliability, "
            "Restriction frequency, Infrastructure NPC, Peak financial cost, "
            "and Drought mitigation cost. As in Figure 1, arrows show the "
            "direction of preference for each axis."
        ),
    ),
    dict(
        id="legend", x=250, y=970, panel="Legend",
        title="Colors and markers",
        text=(
            "Green line/circle = the baseline compromise pathway strategy. "
            "Dark orange/brown line/circle = the IU compromise pathway "
            "strategy. Light gray = every other candidate pathway strategy, "
            "shown for context. The black star (panels d, e) marks the "
            "theoretical ideal point."
        ),
    ),
    dict(
        id="panel_d_title", x=900, y=30, panel="(d)",
        title="Panel (d): comparing robustness in 3D",
        text=(
            "Each axis is one utility's robustness (Watertown, Dryville, "
            "Fallsland); each gray point is one pathway strategy. The two "
            "highlighted compromise strategies let you see, at a glance, how "
            "each one balances robustness across all three utilities "
            "simultaneously, rather than favoring one utility over another."
        ),
    ),
    dict(
        id="panel_d_baseline", x=1000, y=230, panel="(d)",
        title="Baseline compromise: 48% regional robustness",
        text=(
            "The green point sits further from the black ideal-point star "
            "than the IU compromise does. Numerically, the baseline "
            "compromise achieves a regional robustness of **48%** — it meets "
            "all robustness satisficing criteria in less than half of all "
            "simulated deeply-uncertain futures."
        ),
    ),
    dict(
        id="panel_d_iu", x=1150, y=150, panel="(d)",
        title="IU compromise: 63% regional robustness — the best in the set",
        text=(
            "The orange/brown point sits closer to the ideal star. The IU "
            "compromise reaches **63%** regional robustness, notably higher "
            "than the baseline compromise's 48% — in fact, all three "
            "utilities individually achieve their best possible robustness "
            "under the IU compromise, out of the entire Pareto-approximate "
            "strategy set."
        ),
    ),
    dict(
        id="panel_d_ideal", x=1230, y=110, panel="(d)",
        title="The ideal point (★)",
        text=(
            "The black star marks a hypothetical strategy that is maximally "
            "robust for all three utilities at once. A shorter distance from "
            "the star means better, more balanced robustness across "
            "Watertown, Dryville, and Fallsland."
        ),
    ),
    dict(
        id="panel_e_title", x=900, y=520, panel="(e)",
        title="Panel (e): comparing worst-case performance degradation in 3D",
        text=(
            "Each axis is one utility's maximum performance degradation "
            "across all robustness satisficing criteria — essentially, 'how "
            "bad does it get for this utility in the worst case of "
            "implementation uncertainty.' Lower is better here, so points "
            "closer to the star (near-zero degradation on all three axes) are "
            "preferred."
        ),
    ),
    dict(
        id="panel_e_baseline", x=1000, y=670, panel="(e)",
        title="Baseline compromise: up to 70% degradation",
        text=(
            "The green point sits far from the ideal star, reflecting that "
            "the baseline compromise experiences **up to 70%** performance "
            "degradation on its worst-affected robustness criterion when "
            "implementation isn't perfect."
        ),
    ),
    dict(
        id="panel_e_iu", x=1080, y=580, panel="(e)",
        title="IU compromise: capped at 25% degradation",
        text=(
            "The orange/brown point sits much closer to the ideal star: the "
            "IU compromise's worst-case degradation is limited to **25%** — "
            "well below the baseline compromise's 70% — while simultaneously "
            "achieving the higher robustness shown in panel (d)."
        ),
    ),
    dict(
        id="panel_e_ideal", x=1230, y=520, panel="(e)",
        title="The ideal point, for degradation",
        text=(
            "Same concept as the star in panel (d), but now the goal is "
            "*minimal* degradation on all three utility axes simultaneously — "
            "the star sits at the near-zero-degradation corner rather than the "
            "high-robustness corner."
        ),
    ),
]

render_hotspot_explorer(
    page_heading="Figure 5: Baseline vs. IU Compromise Pathway Strategies — Interactive Explorer",
    intro=(
        "This figure compares two specific, representative 'Social Planner' "
        "compromise strategies head-to-head: one drawn from the **baseline** "
        "pathway strategy set (green) and one from the **IU** pathway "
        "strategy set (dark orange/brown). Click a numbered marker on the "
        "figure — or pick a callout from the list below it — to see what that "
        "part of the plot is showing."
    ),
    image_relpath="figures/results_fig5_compSols.jpg",
    hotspots=HOTSPOTS,
    state_key="fig5",
    about_text=(
        "This explorer overlays clickable hotspots on the published static "
        "figure (`figures/results_fig5_compSols.jpg`). Callout text is "
        "grounded in Section 5.4 ('Comparing candidate pathway strategies "
        "reveals inherent performance and robustness differences') of the "
        "accompanying manuscript, including the reported 48% vs. 63% regional "
        "robustness and 70% vs. 25% worst-case degradation figures for the "
        "baseline and IU compromise strategies respectively."
    ),
)

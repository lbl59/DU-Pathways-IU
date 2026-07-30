from __future__ import annotations

from hotspot_explorer import render_hotspot_explorer

HOTSPOTS = [
    dict(
        id="overview",
        x=630, y=70, panel="Overview",
        title="The big picture",
        text=(
            "This figure stress-tests every pathway strategy from Figure 1 by "
            "re-simulating it under a broader, more challenging set of deeply "
            "uncertain futures (the **DU Re-Evaluation** sample) and asking: in "
            "what percentage of those futures does the strategy still meet all "
            "three robustness criteria? That percentage is its **robustness**. "
            "Each of the three panels ranks one Sedento Valley utility's "
            "strategies from most to least robust, baseline (green) on the "
            "left, IU-DU (tan) filling out the rest. The central finding: IU-DU "
            "strategies are more robust than baseline strategies for *every* "
            "utility, not just more numerous."
        ),
    ),
    dict(
        id="panel_a_baseline", x=280, y=230, panel="(a) Watertown",
        title="Watertown's baseline strategies: a short, high bar",
        text=(
            "The green segment is short because only 46 baseline pathway "
            "strategies exist in total (see Figure 1) — this is literally all "
            "of them, ranked from most to least robust. Their robustness tops "
            "out in the low-to-mid 60% range before the baseline set runs out."
        ),
    ),
    dict(
        id="panel_a_iu", x=700, y=290, panel="(a) Watertown",
        title="Watertown's IU strategies: up to 15% more robust",
        text=(
            "The tan bars are the 628 IU-DU strategies. Watertown's best IU "
            "strategies reach roughly 15 percentage points higher robustness "
            "than similarly-ranked baseline strategies. Watertown and Fallsland "
            "cooperatively invest in the New River Reservoir, so this robustness "
            "gain also makes that shared, cooperative infrastructure investment "
            "a safer bet for both utilities."
        ),
    ),
    dict(
        id="panel_b_baseline", x=270, y=545, panel="(b) Dryville",
        title="Dryville's baseline strategies reach the highest peak in the figure",
        text=(
            "Dryville's best baseline strategy is the single tallest bar "
            "anywhere in Figure 2, briefly touching roughly 80% robustness "
            "before the baseline set falls off steeply."
        ),
    ),
    dict(
        id="panel_b_iu", x=700, y=610, panel="(b) Dryville",
        title="Dryville's IU strategies: the largest robustness gain of the three utilities",
        text=(
            "Dryville's IU pathway strategies are up to **35%** more robust "
            "than similarly-ranked baseline strategies — the biggest jump of "
            "any utility. Dryville cooperates mainly through treated transfer "
            "*purchases* rather than shared infrastructure, and can also build "
            "its own infrastructure and draw directly from Autumn Lake — both "
            "of which let it hedge against implementation uncertainty in its "
            "partners' actions without giving up the region's overall high "
            "performance."
        ),
    ),
    dict(
        id="panel_c_baseline", x=280, y=955, panel="(c) Fallsland",
        title="Fallsland's baseline strategies",
        text=(
            "As in the other two panels, Fallsland's baseline strategies "
            "plateau then fall off after 46 ranked strategies, with a maximum "
            "robustness in the same broad range as Watertown's baseline set."
        ),
    ),
    dict(
        id="panel_c_iu", x=700, y=1015, panel="(c) Fallsland",
        title="Fallsland's IU strategies: also up to 15% more robust",
        text=(
            "Like Watertown, Fallsland's IU strategies gain up to 15 "
            "percentage points of robustness over similarly-ranked baseline "
            "strategies. Because Fallsland co-invests in the New River "
            "Reservoir alongside Watertown, this robustness gain matters for "
            "the same reason: it lowers the shared risk of that joint "
            "infrastructure commitment."
        ),
    ),
    dict(
        id="x_axis", x=630, y=1170, panel="Axis",
        title="Reading the x-axis",
        text=(
            "Strategies are sorted independently within each panel, from the "
            "single most robust strategy on the left to the least robust on "
            "the right — rank order, not any shared identity across panels. "
            "The dashed vertical line marks where the baseline set's lowest "
            "robustness falls, for visual reference against the IU set."
        ),
    ),
    dict(
        id="legend_colors", x=290, y=1310, panel="Legend",
        title="Color = which search found this strategy",
        text=(
            "Green = Baseline pathway strategies (46 total, from the baseline "
            "DU Optimization). Tan = IU pathway strategies (628 total, from the "
            "IU-DU Optimization). Same color convention as Figure 1."
        ),
    ),
    dict(
        id="legend_criteria", x=630, y=1400, panel="Legend",
        title="What counts as 'robust' here",
        text=(
            "A strategy's robustness is the percentage of re-evaluated DU SOWs "
            "in which it simultaneously satisfies all three satisficing "
            "criteria: Reliability ≥ 98%, Restriction frequency ≤ 10%, and "
            "Drought mitigation cost ≤ 10%. Meeting all three in more SOWs "
            "means a taller bar."
        ),
    ),
    dict(
        id="key_finding", x=1000, y=1050, panel="Key finding",
        title="Robustness improves for every utility, not just in aggregate",
        text=(
            "Across all three panels, IU-DU strategies dominate the "
            "robustness ranking utility-by-utility — this is on top of the IU "
            "approach already having discovered a far larger and more diverse "
            "set of high-performing strategies in Figure 1. Together, Figures 1 "
            "and 2 show that accounting for implementation uncertainty during "
            "the search itself, not just at evaluation time, pays off in both "
            "the *number* and the *quality* of strategies each utility can "
            "choose from."
        ),
    ),
]

render_hotspot_explorer(
    page_heading="Figure 2: Robustness Under Worst-Case 10th-Percentile Conditions — Interactive Explorer",
    intro=(
        "This figure compares how **robust** each utility's candidate pathway "
        "strategies are once stress-tested against a broad set of deeply "
        "uncertain futures, comparing the **Baseline DU Optimization** "
        "strategies (green) against the **IU-DU Optimization** strategies "
        "(tan). Click a numbered marker on the figure — or pick a callout from "
        "the list below it — to see what that part of the plot is showing."
    ),
    image_relpath="figures/results_fig2_robustness.jpg",
    hotspots=HOTSPOTS,
    state_key="fig2",
    about_text=(
        "This explorer overlays clickable hotspots on the published static "
        "figure (`figures/results_fig2_robustness.jpg`). Hotspot coordinates "
        "were placed by eye against the three ranked-robustness panels "
        "(Watertown, Dryville, Fallsland) and the shared legend. Callout text "
        "is grounded in Section 5.2 ('Evaluating Robustness and Performance "
        "Degradation under Implementation Uncertainty') of the accompanying "
        "manuscript, including the reported +15% (Watertown, Fallsland) and "
        "+35% (Dryville) robustness gains for IU strategies over "
        "similarly-ranked baseline strategies."
    ),
)

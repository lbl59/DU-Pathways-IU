from __future__ import annotations

from hotspot_explorer import render_hotspot_explorer

HOTSPOTS = [
    dict(
        id="overview",
        x=420, y=15, panel="Overview",
        title="The big picture",
        text=(
            "This figure asks: when a utility's decision variables (or its "
            "partners') get perturbed by implementation uncertainty, whose "
            "actions actually drive changes in whose performance? Panel (a) "
            "shows the **baseline compromise** strategy from Figure 5; panel "
            "(b) shows the **IU compromise** strategy. Within each panel, the "
            "three column blocks are Watertown, Dryville, and Fallsland; each "
            "utility's performance objectives (REL, RF, INPC, PFC, DMC) run "
            "along that column's x-axis, while every decision variable that "
            "*could* perturb those objectives — belonging to any of the three "
            "utilities — is listed down the y-axis. Bigger bubbles mean higher "
            "sensitivity. Shaded diagonal blocks mark each utility's own "
            "**region of control**: the decision variables it has full agency "
            "over."
        ),
    ),
    dict(
        id="panel_a_label", x=60, y=30, panel="(a)",
        title="Panel (a): Baseline Social Planner strategy",
        text=(
            "This panel shows sensitivities for the baseline compromise "
            "pathway strategy introduced in Figure 5. Overall, it reveals that "
            "each utility's performance is highly dependent on its partners "
            "implementing their cooperative actions exactly as planned — a "
            "single utility's failure to do so can ripple into another "
            "utility's performance."
        ),
    ),
    dict(
        id="panel_a_watertown", x=280, y=200, panel="(a) Watertown",
        title="Watertown's dependence on Dryville, under baseline",
        text=(
            "Watertown's performance metrics are highly sensitive to whether "
            "Dryville and Fallsland implement their cooperative actions as "
            "planned. Most strikingly, more than half of the variability in "
            "Watertown's Infrastructure NPC is attributable to uncertainty in "
            "how precisely Dryville executes its treated transfers — a "
            "decision variable entirely outside Watertown's own control."
        ),
    ),
    dict(
        id="panel_a_dryville", x=460, y=200, panel="(a) Dryville",
        title="Dryville: some independence, but still exposed",
        text=(
            "Dryville has access to its own water resources (recall Figure "
            "1a) and can invest independently in infrastructure, which gives "
            "it somewhat reduced sensitivity to implementation uncertainty "
            "compared to Watertown and Fallsland. Even so, under the baseline "
            "compromise, Dryville remains notably sensitive to how precisely "
            "Fallsland executes its treated transfers."
        ),
    ),
    dict(
        id="panel_a_fallsland", x=650, y=140, panel="(a) Fallsland",
        title="Fallsland: the most exposed utility, under baseline",
        text=(
            "Fallsland has the smallest supply-to-demand ratio in the Sedento "
            "Valley and shows a strong dependence on Dryville's precise use "
            "of water-use restrictions. Because Fallsland and Watertown also "
            "co-invest in the New River Reservoir, both utilities' individual "
            "agency over their own performance is reduced under the baseline "
            "compromise — a vulnerability that shows up directly as the "
            "baseline compromise's high performance degradation in Figure "
            "5(e)."
        ),
    ),
    dict(
        id="panel_b_label", x=60, y=390, panel="(b)",
        title="Panel (b): IU Social Planner strategy",
        text=(
            "This panel shows the same type of sensitivity analysis, but for "
            "the IU compromise pathway strategy. The pattern reverses from "
            "panel (a): utilities gain substantially more control over their "
            "own performance, even while remaining highly cooperative."
        ),
    ),
    dict(
        id="panel_b_watertown", x=280, y=560, panel="(b) Watertown",
        title="Watertown regains control, under IU",
        text=(
            "Under the IU compromise, Watertown's restriction-frequency "
            "objective shows little to no sensitivity to implementation "
            "uncertainty at all. Perturbations in Watertown's *own* "
            "infrastructure trigger — not its partners' actions — now exert "
            "the most influence over three of its five objectives "
            "(reliability, infrastructure NPC, and peak financial cost), "
            "giving Watertown much better control over its own outcomes."
        ),
    ),
    dict(
        id="panel_b_dryville", x=460, y=560, panel="(b) Dryville",
        title="Dryville: minimal vulnerability to its partners, under IU",
        text=(
            "Dryville's sensitivity pattern under the IU compromise shows "
            "little to no vulnerability to uncertainty in its partners' "
            "actions. Roughly three-quarters of its most-influential decision "
            "variables now fall within its own shaded region of control."
        ),
    ),
    dict(
        id="panel_b_fallsland", x=650, y=500, panel="(b) Fallsland",
        title="Fallsland: control over its own infrastructure cost, under IU",
        text=(
            "Under the IU compromise, the actions driving changes in "
            "Fallsland's performance lie almost entirely within its own "
            "region of control. Notably, even though Figure 6(c) and (f) show "
            "Fallsland's infrastructure pathway is similar under both "
            "compromises, Fallsland retains far more control over its "
            "Infrastructure NPC objective specifically under the IU "
            "compromise — accounting for implementation uncertainty during "
            "the search lets cooperating utilities jointly invest in "
            "infrastructure without inheriting each other's implementation "
            "risk, an effect that matters most for utilities with the "
            "smallest capacity-to-demand ratios."
        ),
    ),
    dict(
        id="legend_colors", x=300, y=715, panel="Legend",
        title="Bubble color = strategy and influence level",
        text=(
            "Dark green/dark brown-orange circles mark a utility's three "
            "*most-influential* decision variables for a given objective "
            "(baseline in panel a, IU in panel b). Lighter green/tan circles "
            "mark all other, less-influential decision variables. Shaded "
            "background regions mark a utility's own region of control."
        ),
    ),
    dict(
        id="legend_size", x=760, y=750, panel="Legend",
        title="Bubble size = sensitivity",
        text=(
            "Larger bubbles indicate a performance objective is more "
            "sensitive to implementation uncertainty in that decision "
            "variable — i.e., perturbing that decision variable changes the "
            "objective's outcome more. Exact sensitivity indices (from a "
            "Delta Moment-Independent Sensitivity Analysis) are reported in "
            "the manuscript's Supporting Information."
        ),
    ),
    dict(
        id="legend_dv_key", x=150, y=830, panel="Legend",
        title="Decision variable abbreviations",
        text=(
            "RT = Restriction trigger, TT = Transfer trigger, INF = "
            "Infrastructure investment trigger. Each is a capacity-to-demand "
            "risk-of-failure (ROF) threshold that, once exceeded, deploys its "
            "associated action — restricting water use, purchasing treated "
            "transfers, or beginning infrastructure construction."
        ),
    ),
    dict(
        id="legend_obj_key", x=470, y=830, panel="Legend",
        title="Performance objective abbreviations",
        text=(
            "REL = Reliability, RF = Restriction frequency, INPC = "
            "Infrastructure net present cost, PFC = Peak financial cost, DMC = "
            "Drought mitigation cost — the same five objectives used "
            "throughout Figures 1 and 5."
        ),
    ),
]

render_hotspot_explorer(
    page_title="Figure 7 - Sensitivity Analysis",
    page_heading="Figure 7: Delta Moment-Independent Sensitivity Analysis — Interactive Explorer",
    intro=(
        "This figure shows how sensitive each utility's performance is to "
        "perturbations in its own and its partners' decision variables, "
        "comparing the **baseline compromise** strategy (panel a) against the "
        "**IU compromise** strategy (panel b) from Figure 5. Click a numbered "
        "marker on the figure — or pick a callout from the list below it — to "
        "see what that part of the plot is showing."
    ),
    image_relpath="figures/results_fig7_sensitivity_analysis.jpg",
    hotspots=HOTSPOTS,
    state_key="fig7",
    about_text=(
        "This explorer overlays clickable hotspots on the published static "
        "figure (`figures/results_fig7_sensitivity_analysis.jpg`). Hotspots "
        "are placed at the utility-column level rather than on individual "
        "bubbles, since the underlying per-cell sensitivity indices are "
        "tabulated in the manuscript's Supporting Information rather than in "
        "this repository. Callout text is grounded in Section 5.6 ('Delta "
        "Moment-Independent Sensitivity Analysis reveals vulnerabilities to "
        "implementation uncertainty across utilities') of the accompanying "
        "manuscript."
    ),
)

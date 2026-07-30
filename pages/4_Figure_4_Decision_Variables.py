from __future__ import annotations

from hotspot_explorer import render_hotspot_explorer

HOTSPOTS = [
    dict(
        id="overview",
        x=340, y=15, panel="Overview",
        title="The big picture",
        text=(
            "This figure looks *inside* the pathway strategies themselves, at "
            "their decision variables — the risk-of-failure (ROF) trigger "
            "values that decide when a utility restricts water use, purchases "
            "treated transfers, or invests in new infrastructure. Each curve "
            "is a kernel density estimate (KDE): where the curve peaks tells "
            "you which trigger values most pathway strategies actually use. "
            "Columns are the three decision-variable types — Restriction "
            "trigger (RT), Transfer trigger (TT), Infrastructure trigger "
            "(INF); rows are the three utilities. Green = baseline strategies, "
            "orange = IU strategies. The headline result: IU strategies lean "
            "much more heavily on cooperative tools (transfers, shared "
            "infrastructure) than baseline strategies do."
        ),
    ),
    dict(
        id="panel_a", x=150, y=90, panel="(a) Watertown — RT",
        title="Watertown's restriction trigger",
        text=(
            "Baseline strategies (green) skew toward relying on water-use "
            "restrictions more heavily than IU strategies (orange) do. Under "
            "the baseline approach, restrictions are Watertown's default lever "
            "when the IU approach's cooperative alternative — infrastructure "
            "investment — isn't yet part of the picture (see panel b)."
        ),
    ),
    dict(
        id="panel_b", x=590, y=90, panel="(b) Watertown — INF",
        title="Watertown's infrastructure trigger: the clearest IU vs. baseline contrast",
        text=(
            "This is one of the starkest differences in the whole figure: the "
            "orange (IU) curve peaks close to high use of the infrastructure "
            "trigger, while the green (baseline) curve does not. IU pathway "
            "strategies are far more likely to rely on shared infrastructure "
            "investment — consistent with the IU-DU approach's greater "
            "aversion to long-term risk under challenging, uncertain futures. "
            "Watertown has no Transfer-trigger panel here because it "
            "*supplies* transfers to Dryville and Fallsland rather than "
            "purchasing them."
        ),
    ),
    dict(
        id="panel_c", x=150, y=330, panel="(c) Dryville — RT",
        title="Dryville's restriction trigger",
        text=(
            "Dryville's IU strategies are more likely to actively use water-use "
            "restrictions than its baseline strategies — but, as panels (d) and "
            "(e) show, this happens *in tandem with* greater use of transfers "
            "and infrastructure investment, not instead of them."
        ),
    ),
    dict(
        id="panel_d", x=370, y=330, panel="(d) Dryville — TT",
        title="Dryville's transfer trigger",
        text=(
            "Dryville is one of only two utilities (with Fallsland) that "
            "purchases treated transfers from Watertown. Its transfer-trigger "
            "use shifts under the IU approach as part of a broader mix of "
            "short-term drought actions used alongside restrictions."
        ),
    ),
    dict(
        id="panel_e", x=590, y=330, panel="(e) Dryville — INF",
        title="Dryville's infrastructure trigger",
        text=(
            "Like Watertown, Dryville is more likely to invest in long-term "
            "infrastructure under the IU approach. Combined with its increased "
            "use of restrictions and transfers (panels c, d), this lets "
            "Dryville retain short-term drought-response flexibility while "
            "still making strategic, well-timed infrastructure investments — "
            "rather than over-committing to one lever."
        ),
    ),
    dict(
        id="panel_f", x=150, y=560, panel="(f) Fallsland — RT",
        title="Fallsland's restriction trigger",
        text=(
            "Fallsland's IU strategies are more likely to actively use water "
            "restrictions than its baseline strategies, paired with greater "
            "transfer use (panel g) as part of the same short-term adaptive "
            "toolkit seen in Dryville."
        ),
    ),
    dict(
        id="panel_g", x=370, y=560, panel="(g) Fallsland — TT",
        title="Fallsland's transfer trigger",
        text=(
            "Fallsland's IU strategies more actively use treated transfer "
            "purchases from Watertown. This lets Fallsland supplement its "
            "supply in the short term and delay major infrastructure "
            "investments until they become financially worthwhile."
        ),
    ),
    dict(
        id="panel_h", x=590, y=560, panel="(h) Fallsland — INF",
        title="Fallsland's infrastructure trigger",
        text=(
            "As with Watertown and Dryville, Fallsland's IU strategies lean "
            "more heavily on infrastructure investment. Recall from Figure "
            "1(d) that IU strategies strongly outperform baseline strategies "
            "on peak financial cost under worst-case conditions — this more "
            "deliberate, cooperative use of infrastructure, transfers, and "
            "restrictions together is the mechanism behind that result, and "
            "behind the robustness (Figure 2) and limited degradation "
            "(Figure 3) gains seen earlier."
        ),
    ),
    dict(
        id="legend", x=340, y=690, panel="Legend",
        title="Reading the KDE curves",
        text=(
            "Green = decision-variable distribution across baseline DU "
            "Optimization pathway strategies. Orange = distribution across IU-DU "
            "Optimization pathway strategies. A peak toward the 'High' end of "
            "an axis means many strategies set that trigger to be used "
            "aggressively (a low risk tolerance that fires the associated "
            "action early and often); a peak toward 'Low' means the opposite."
        ),
    ),
]

render_hotspot_explorer(
    page_title="Figure 4 - Decision Variable Distributions",
    page_heading="Figure 4: Decision Variable (ROF Trigger) Distributions — Interactive Explorer",
    intro=(
        "This figure shows how often pathway strategies rely on each of three "
        "adaptive tools — water-use **restrictions**, treated water **transfer** "
        "purchases, and **infrastructure** investment — comparing **Baseline "
        "DU Optimization** strategies (green) against **IU-DU Optimization** "
        "strategies (orange). Click a numbered marker on the figure — or pick "
        "a callout from the list below it — to see what that part of the plot "
        "is showing."
    ),
    image_relpath="figures/results_fig4_dvs.jpg",
    hotspots=HOTSPOTS,
    state_key="fig4",
    about_text=(
        "This explorer overlays clickable hotspots on the published static "
        "figure (`figures/results_fig4_dvs.jpg`). Watertown has no "
        "Transfer-trigger (TT) panel because it supplies, rather than "
        "purchases, treated transfers. Callout text is grounded in Section 5.3 "
        "('Accounting for implementation uncertainty increases the use of "
        "cooperative tools') of the accompanying manuscript."
    ),
)

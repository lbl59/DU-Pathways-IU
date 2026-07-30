from __future__ import annotations

from hotspot_explorer import render_hotspot_explorer

HOTSPOTS = [
    dict(
        id="overview",
        x=300, y=15, panel="Overview",
        title="The big picture",
        text=(
            "This figure asks a different question from Figures 1 and 2: not "
            "'how good is a strategy,' but 'how much worse does a strategy get "
            "when its planned actions are implemented imperfectly?' — its "
            "**performance degradation**. The left column, panels (a)-(d), "
            "shows the baseline pathway strategies; the right column, panels "
            "(e)-(h), shows the IU pathway strategies. Each subfigure pairs a "
            "bar plot (what fraction of strategies see a given degradation "
            "level) with a heatmap underneath it (how many strategies, in "
            "absolute counts). Rows run Watertown, Dryville, Fallsland, and "
            "the Sedento Valley region as a whole."
        ),
    ),
    dict(
        id="watertown_baseline", x=150, y=100, panel="(a) Watertown — baseline",
        title="Watertown, baseline strategies",
        text=(
            "The bar plot's shape looks broadly similar to Watertown's IU "
            "counterpart in panel (e) — a first glance at the histograms alone "
            "under-sells the difference between baseline and IU. The heatmap "
            "underneath is where the real contrast shows up: it counts far "
            "fewer strategies at any given degradation level, since there are "
            "only 46 baseline strategies in total."
        ),
    ),
    dict(
        id="watertown_iu", x=480, y=100, panel="(e) Watertown — IU",
        title="Watertown, IU strategies",
        text=(
            "With 628 IU strategies to draw from, the heatmap beneath this "
            "histogram is markedly darker in the 20%-30% degradation range — "
            "Watertown has access to many more strategies clustered at a "
            "*similar, moderate* level of vulnerability to implementation "
            "uncertainty, rather than a handful of strategies spread thinly "
            "across the axis."
        ),
    ),
    dict(
        id="dryville_baseline", x=150, y=250, panel="(b) Dryville — baseline",
        title="Dryville, baseline strategies",
        text=(
            "Recall from Figure 2 that Dryville's baseline strategies reach "
            "the highest robustness of any utility. This panel reveals the "
            "flip side of that: achieving that peak robustness under the "
            "baseline approach comes at the cost of a skewed, less favorable "
            "degradation profile relative to Watertown and Fallsland's baseline "
            "strategies — high robustness and low degradation aren't both "
            "available at once in the baseline set."
        ),
    ),
    dict(
        id="dryville_iu", x=480, y=250, panel="(f) Dryville — IU",
        title="Dryville, IU strategies",
        text=(
            "Under the IU-DU approach, Dryville's degradation profile "
            "converges toward the same 20%-30% range shared by Watertown and "
            "Fallsland's IU strategies, instead of being the outlier it was in "
            "the baseline set. IU strategies let Dryville achieve high "
            "robustness *and* limited degradation simultaneously."
        ),
    ),
    dict(
        id="fallsland_baseline", x=150, y=400, panel="(c) Fallsland — baseline",
        title="Fallsland, baseline strategies",
        text=(
            "Under the baseline approach, Watertown and Fallsland's more "
            "favorable degradation profiles come partly at Dryville's expense "
            "— the region's utilities aren't uniformly protected, so one "
            "utility's low vulnerability can reflect another's higher exposure "
            "under the same set of strategies."
        ),
    ),
    dict(
        id="fallsland_iu", x=480, y=400, panel="(g) Fallsland — IU",
        title="Fallsland, IU strategies",
        text=(
            "Fallsland's IU degradation profile lands in the same "
            "moderate, ~20%-30% range as Watertown's and Dryville's IU "
            "strategies — evidence that the IU-DU search produces strategies "
            "whose vulnerability to implementation uncertainty is shared more "
            "evenly across the region, rather than concentrated on whichever "
            "utility happens to have the least agency."
        ),
    ),
    dict(
        id="regional_baseline", x=150, y=550, panel="(d) Regional — baseline",
        title="Key finding: baseline strategies are exposed as a region",
        text=(
            "Looking at the region as a whole, the 46 baseline pathway "
            "strategies are spread roughly evenly across all degradation "
            "levels — meaning **more than half** of them experience "
            "upwards of 30% performance degradation when implementation "
            "isn't perfect."
        ),
    ),
    dict(
        id="regional_iu", x=480, y=550, panel="(h) Regional — IU",
        title="Key finding: IU strategies limit regional degradation",
        text=(
            "In sharp contrast, roughly **three-quarters** of the 628 IU "
            "pathway strategies keep regional performance degradation below "
            "30%. That works out to more than 450 pathway strategies that are "
            "simultaneously regionally robust (Figure 2) *and* only lightly "
            "vulnerable to implementation uncertainty — a much richer menu of "
            "safe, actionable options than the baseline approach provides."
        ),
    ),
    dict(
        id="colorbar_baseline", x=150, y=680, panel="Legend",
        title="Baseline heatmap color scale",
        text=(
            "Darker green in the heatmaps indicates a larger number of "
            "baseline pathway strategies experiencing that level of "
            "performance degradation, out of the 46 baseline strategies total."
        ),
    ),
    dict(
        id="colorbar_iu", x=480, y=680, panel="Legend",
        title="IU heatmap color scale",
        text=(
            "Darker orange/brown in the heatmaps indicates a larger number of "
            "IU pathway strategies experiencing that level of performance "
            "degradation, out of the 628 IU strategies total. Note the scale "
            "goes much higher (up to 250) than the baseline scale (up to 25), "
            "reflecting the far larger IU strategy set."
        ),
    ),
]

render_hotspot_explorer(
    page_title="Figure 3 - Performance Degradation",
    page_heading="Figure 3: Performance Degradation Distributions — Interactive Explorer",
    intro=(
        "This figure examines each utility's (and the region's) vulnerability "
        "to **implementation uncertainty** — how much performance degrades "
        "when planned actions like restrictions, transfers, or infrastructure "
        "builds don't happen exactly as scheduled. Panels (a)-(d) show "
        "**baseline** pathway strategies; panels (e)-(h) show **IU** pathway "
        "strategies. Click a numbered marker on the figure — or pick a callout "
        "from the list below it — to see what that part of the plot is showing."
    ),
    image_relpath="figures/results_fig3_degradation.jpg",
    hotspots=HOTSPOTS,
    state_key="fig3",
    about_text=(
        "This explorer overlays clickable hotspots on the published static "
        "figure (`figures/results_fig3_degradation.jpg`). Each subfigure pairs "
        "a bar plot with a heatmap; hotspots point at the bar-plot region of "
        "each subfigure but their callout text draws on both. Callout text is "
        "grounded in Section 5.2 of the accompanying manuscript, including the "
        "reported ~250 vs. <15 strategy counts at 20%-30% degradation, and the "
        "'more than half of 46' vs. 'three-quarters of 628' regional "
        "degradation comparison in panels (d) and (h)."
    ),
)

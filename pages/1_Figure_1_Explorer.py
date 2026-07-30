from __future__ import annotations

from hotspot_explorer import render_hotspot_explorer

HOTSPOTS = [
    dict(
        id="overview",
        x=563, y=18, panel="Overview",
        title="The big picture",
        text=(
            "Every marker/line in this figure is one candidate water-supply "
            "*pathway strategy* — a policy for when and what infrastructure to "
            "build and how to respond to shortages. The left half (green/teal) "
            "comes from a **Baseline DU Optimization** that only searched using "
            "the expected future. The right half (orange) comes from an "
            "**IU-DU Optimization** that searched using the worst 10th-percentile "
            "(WC10) of simulated futures as well. The top row (a, c) shows "
            "5-objective tradeoffs as parallel-coordinate lines; the bottom row "
            "(b, d) shows the same strategies as 3D bubble plots, first under "
            "expected conditions, then under worst-case stress. The overall "
            "story: baseline strategies look excellent under expected conditions "
            "but degrade the most once uncertainty is introduced, while IU-DU "
            "strategies trade a little expected-case performance for much better "
            "robustness."
        ),
    ),
    dict(
        id="panel_a_title", x=275, y=52, panel="(a)",
        title="Baseline DU Optimization",
        text=(
            "This half of the figure shows results from the traditional "
            "DU Pathways search: the optimization only ever saw the "
            "*expected* (average) future when scoring candidate strategies. "
            "It never saw how they'd behave under a stressful, low-probability "
            "future — that's tested separately in panel (d)."
        ),
    ),
    dict(
        id="panel_a_lines", x=240, y=230, panel="(a)",
        title="Reading the parallel-coordinates plot",
        text=(
            "Each green line is one baseline strategy, traced across five "
            "performance metrics evaluated under **expected** conditions: "
            "Reliability, Restriction frequency, Infrastructure cost (NPC), "
            "Peak financial cost, and Drought mitigation cost. Axes were "
            "flipped so 'down' always means 'better' — that's what the "
            "**Direction of preference** arrow on the left is telling you. "
            "A strategy that hugs the bottom across every axis is doing very "
            "well on all five objectives simultaneously; one that swings up "
            "high on any axis is making a real sacrifice there."
        ),
    ),
    dict(
        id="panel_c_title", x=825, y=52, panel="(c)",
        title="IU-DU Optimization",
        text=(
            "This half shows strategies from a search that explicitly "
            "incorporated deep uncertainty: candidates were scored on their "
            "**WC10** performance — the worst 10th-percentile outcome across "
            "many simulated futures — not just the average case. That's why "
            "the axis ranges here (e.g. up to 300 for Infrastructure NPC, 80% "
            "for Restriction freq.) are so much wider and harsher than in panel (a)."
        ),
    ),
    dict(
        id="panel_c_lines", x=850, y=230, panel="(c)",
        title="A wider net of strategies",
        text=(
            "There are many more orange lines here than green lines in panel "
            "(a) — the IU-DU search explored a broader space of strategies "
            "because it had to hedge against a wide range of possible futures, "
            "not just one expected trajectory. Some lines swing much higher on "
            "cost axes; those are strategies that spend more upfront "
            "specifically to protect reliability under worst-case stress."
        ),
    ),
    dict(
        id="panel_b_title", x=290, y=418, panel="(b)",
        title="Same strategies, plotted in 3D (expected conditions)",
        text=(
            "Panel (b) re-plots both sets of strategies (teal = baseline DU, "
            "orange = IU-DU) as bubbles in a 3D space of Drought mitigation cost, "
            "Infrastructure NPC, and Reliability — all evaluated under **expected** "
            "conditions. Color encodes Restriction frequency; bubble size encodes "
            "Peak financial cost."
        ),
    ),
    dict(
        id="panel_b_ideal", x=48, y=517, panel="(b)",
        title="The ideal point (★)",
        text=(
            "The black star marks a hypothetical *ideal point*: 100% reliability, "
            "$0 infrastructure cost, 0% restriction frequency, and 0% drought "
            "mitigation cost, all at once. No real strategy can actually reach it "
            "— objectives trade off against each other — but it's plotted as a "
            "reference corner. Strategies clustered near the star are the most "
            "desirable overall."
        ),
    ),
    dict(
        id="panel_b_teal", x=150, y=565, panel="(b)",
        title="Baseline strategies excel here — because this is what they were tuned for",
        text=(
            "The teal bubbles (baseline DU strategies) sit tightly clustered near "
            "the ideal star in this panel. That's expected: these strategies were "
            "optimized using exactly this — the average/expected future — as the "
            "test. Performing well here doesn't yet tell us anything about how "
            "they'll hold up under stress; see panel (d) for that."
        ),
    ),
    dict(
        id="panel_b_orange", x=330, y=615, panel="(b)",
        title="IU-DU strategies: nearly as good, slightly more spread out",
        text=(
            "The orange bubbles (IU-DU strategies) are also close to the ideal "
            "point under expected conditions, but somewhat less tightly bunched "
            "than the teal ones. That small, visible spread is the modest "
            "'expected-case premium' these strategies pay in exchange for the "
            "robustness they gain under worst-case stress — visible in panel (d)."
        ),
    ),
    dict(
        id="panel_d_title", x=845, y=418, panel="(d)",
        title="Same strategies, stress-tested (worst 10th-percentile conditions)",
        text=(
            "Panel (d) plots the exact same strategies as panel (b), but now "
            "scored on their **WC10** performance — the worst 10th-percentile of "
            "simulated futures. This is the stress test: it reveals which "
            "strategies were only ever good on average, versus which stay good "
            "even when things go wrong."
        ),
    ),
    dict(
        id="panel_d_ideal", x=637, y=517, panel="(d)",
        title="The ideal point, under stress",
        text=(
            "Same concept as the star in panel (b): a hypothetical best-possible "
            "outcome, now measured against the harsher WC10 metrics. Compare how "
            "far each color of bubble drifts from this star relative to panel (b) "
            "— that drift is the whole point of this figure."
        ),
    ),
    dict(
        id="panel_d_teal", x=855, y=650, panel="(d)",
        title="Key finding: baseline strategies lose ground under stress",
        text=(
            "Notice the teal (baseline DU) bubbles are now scattered much further "
            "from the ideal star — reliability drops well below the tight 98-100% "
            "band seen in panel (b), and restriction frequency and cost both climb. "
            "These are the *same* strategies that looked excellent in panel (b); "
            "they just were never tested against a harsh future during their "
            "search, so nothing protected them from it."
        ),
    ),
    dict(
        id="panel_d_orange", x=690, y=555, panel="(d)",
        title="Key finding: IU-DU strategies hold up",
        text=(
            "The orange (IU-DU) bubbles remain much more tightly clustered near "
            "the ideal star even here, under worst 10th-percentile stress. "
            "Because deep uncertainty was baked into their search from the start, "
            "these strategies were selected specifically for consistent "
            "performance rather than just a good average outcome — this is the "
            "practical case for IU-DU optimization over the conventional baseline."
        ),
    ),
    dict(
        id="legend_color", x=200, y=812, panel="Legend",
        title="Color = which search found this strategy",
        text=(
            "Teal markers/lines = strategies from the Baseline DU Optimization. "
            "Orange markers/lines = strategies from the IU-DU Optimization. This "
            "color coding is consistent across all four panels."
        ),
    ),
    dict(
        id="legend_size", x=700, y=812, panel="Legend",
        title="Bubble size = Peak Financial Cost",
        text=(
            "In panels (b) and (d), marker size encodes Peak Financial Cost: "
            "larger bubbles indicate a lower (better) peak financial cost, and "
            "smaller bubbles indicate a higher (worse) one — so, all else equal, "
            "bigger is better here."
        ),
    ),
    dict(
        id="legend_star", x=922, y=812, panel="Legend",
        title="Ideal point marker",
        text=(
            "The black star appearing in panels (b) and (d) is the reference "
            "'ideal point' described above — the same concept in both panels, "
            "just measured against different (expected vs. worst-case) metrics."
        ),
    ),
]

render_hotspot_explorer(
    page_heading="Figure 1: Regional Performance Tradeoffs — Interactive Explorer",
    intro=(
        "This figure compares candidate water-supply pathway strategies found by two "
        "search approaches: **Baseline DU Optimization** (searches using only the "
        "*expected* future) and **IU-DU Optimization** (searches that also account for "
        "deep uncertainty, i.e. the *worst 10th-percentile* of simulated futures). "
        "Click a numbered marker on the figure — or pick a callout from the list below "
        "it — to see what that part of the plot is showing."
    ),
    image_relpath="figures/results_fig1_objs.jpg",
    hotspots=HOTSPOTS,
    state_key="fig1",
    about_text=(
        "This explorer overlays clickable hotspots on the published static "
        "figure (`figures/results_fig1_objs.jpg`) rather than re-simulating the "
        "underlying data, since the per-solution objective values used to "
        "generate the figure are not tracked in this repository (only decision "
        "variables and downstream robustness/perturbation results are). "
        "The callout text is grounded directly in what the plotting code in "
        "`scripts/Figure Plotting/` (especially `parallel_plot_functions.py` "
        "and the 3D scatter logic in `explore_objs.ipynb`) computes and labels."
    ),
)

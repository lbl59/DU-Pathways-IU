from __future__ import annotations

from hotspot_explorer import render_hotspot_explorer

HOTSPOTS = [
    dict(
        id="overview",
        x=400, y=55, panel="(a)",
        title="Sedento Valley Test Case — overview",
        text=(
            "Panel (a) shows the Sedento Valley regional test case: a stylised "
            "representation of three cooperating water utilities — **Watertown**, "
            "**Dryville**, and **Fallsland** — along with their existing and "
            "potential water sources and the supply/transfer connections between "
            "them. Panels (b) and (c) provide supporting context: how large each "
            "utility's customer base is, and how demand is projected to grow over "
            "the 55-year simulation horizon."
        ),
    ),
    dict(
        id="autumn_lake",
        x=525, y=145, panel="(a)",
        title="Autumn Lake",
        text=(
            "Autumn Lake is a major existing surface-water reservoir in the "
            "region. It supplies water directly to Fallsland and, through "
            "treated-transfer connections, can supply Dryville as well. "
            "Fallsland's access to Autumn Lake gives it relatively high baseline "
            "supply capacity, reflected in the smaller share of Fallsland's "
            "expansion options that involve entirely new infrastructure."
        ),
    ),
    dict(
        id="fallsland",
        x=650, y=280, panel="(a)",
        title="Fallsland utility",
        text=(
            "Fallsland is the largest of the three utilities by population "
            "served (~570 k, see panel b) and consequently has the highest "
            "absolute demand trajectory (see panel c). It has access to Autumn "
            "Lake and can build a joint **New River Reservoir** co-invested with "
            "Watertown, can implement water restrictions, invest in water-reuse, "
            "and purchase treated water from Dryville. Because it co-invests in "
            "New River Reservoir with Watertown, Fallsland's infrastructure "
            "decisions are tightly coupled to Watertown's."
        ),
    ),
    dict(
        id="dryville",
        x=385, y=400, panel="(a)",
        title="Dryville utility",
        text=(
            "Dryville is the mid-sized utility (~330 k population, panel b) and "
            "the most self-reliant in terms of infrastructure options: it can "
            "expand Sugar Creek Reservoir (high and low expansions), draw from "
            "College Rock Reservoir, implement water restrictions, invest in "
            "water-reuse, and purchase treated transfers from its partners. "
            "This breadth of local options is one reason Dryville can achieve "
            "the largest robustness gains of the three utilities when moving "
            "from Baseline DU to IU-DU optimization (see Figure 2)."
        ),
    ),
    dict(
        id="watertown",
        x=500, y=645, panel="(a)",
        title="Watertown utility",
        text=(
            "Watertown is the smallest utility (~150 k population, panel b), "
            "with lower absolute demand but tighter supply headroom. It can "
            "expand Lake Michael, co-build the New River Reservoir with "
            "Fallsland, implement water restrictions, and invest in "
            "infrastructure. The joint New River Reservoir is the key "
            "cooperative infrastructure investment in this test case: "
            "both Watertown and Fallsland must agree to build it, creating "
            "a dependency between their pathway decisions."
        ),
    ),
    dict(
        id="sugar_creek",
        x=135, y=310, panel="(a)",
        title="Sugar Creek Reservoir (Dryville)",
        text=(
            "Sugar Creek Reservoir is an existing reservoir available to "
            "Dryville. It can be expanded — at either a 'high' or 'low' capacity "
            "increment — as one of Dryville's local infrastructure options. The "
            "dashed triangles to the left represent these two potential expansion "
            "tiers. Choosing when (or whether) to invest in Sugar Creek vs. "
            "buying treated transfers vs. relying on College Rock is a core "
            "decision in Dryville's pathway strategies."
        ),
    ),
    dict(
        id="college_rock",
        x=110, y=515, panel="(a)",
        title="College Rock Reservoir (Dryville)",
        text=(
            "College Rock Reservoir is another potential supply source for "
            "Dryville, shown here as a dashed (potential) reservoir triangle. "
            "Unlike Sugar Creek, College Rock represents a larger-scale option "
            "that Dryville can draw on if demand growth outpaces Sugar Creek's "
            "capacity — or if treated-transfer costs from partners become "
            "prohibitive."
        ),
    ),
    dict(
        id="lake_michael",
        x=285, y=670, panel="(a)",
        title="Lake Michael (Watertown)",
        text=(
            "Lake Michael is an existing reservoir that Watertown currently draws "
            "from. Watertown can invest to expand its intake or treatment capacity "
            "at this source as part of its local infrastructure portfolio, "
            "independent of the cooperative New River Reservoir decision."
        ),
    ),
    dict(
        id="new_river",
        x=695, y=565, panel="(a)",
        title="New River Reservoir (Watertown + Fallsland, joint)",
        text=(
            "New River Reservoir is the key **cooperative infrastructure** in "
            "this test case: it is jointly built and shared by Watertown and "
            "Fallsland. Neither utility can build it alone — both must agree and "
            "invest. This creates the core implementation-uncertainty challenge "
            "addressed by IU-DU optimization: Watertown's pathway may call for "
            "New River, but if Fallsland's doesn't (or delays), Watertown's "
            "strategy may not perform as planned."
        ),
    ),
    dict(
        id="cooperative_transfers",
        x=490, y=485, panel="(a)",
        title="Cooperative treated-water transfers",
        text=(
            "The blue arrows in panel (a) indicate treated-water supply "
            "connections. A utility with surplus treated capacity can sell water "
            "to a partner facing shortage. These **treated transfers** are a "
            "key flexibility mechanism in Sedento Valley: rather than each "
            "utility always building its own infrastructure, a low-cost surplus "
            "at one utility can satisfy near-term shortfalls at another. IU-DU "
            "strategies need to account for the possibility that a partner's "
            "actual available surplus may differ from what was assumed during "
            "optimization."
        ),
    ),
    dict(
        id="legend",
        x=175, y=920, panel="(a) Legend",
        title="Reading the legend",
        text=(
            "The legend explains the icons and arrow types used in panel (a). "
            "Solid triangles = existing reservoirs. Dashed triangles = potential "
            "new reservoirs (infrastructure investment options). Solid blue arrows "
            "= current supply/treated-water connections. Dashed blue arrows = "
            "potential supply connections. Grey arrows = existing WTP "
            "(water-treatment plant) connections. The restriction, reuse, and "
            "infrastructure-investment icons beside each utility name indicate "
            "the local action types available to that utility."
        ),
    ),
    dict(
        id="panel_b_title",
        x=1155, y=85, panel="(b)",
        title="Population serviced by utility",
        text=(
            "Panel (b) ranks the three utilities by the number of customers "
            "they serve. Fallsland (~570 k) is by far the largest, Dryville "
            "is mid-sized (~330 k), and Watertown is the smallest (~150 k). "
            "These population differences drive the absolute scale of each "
            "utility's demand trajectory in panel (c) and affect how costly "
            "supply shortfalls are for each — a shortage that affects 570 k "
            "people is more consequential than one affecting 150 k."
        ),
    ),
    dict(
        id="panel_b_fallsland",
        x=1270, y=190, panel="(b)",
        title="Fallsland: largest population",
        text=(
            "Fallsland's bar extends to roughly 570 k, making it the dominant "
            "demand driver in the region. Its large customer base means that "
            "even small per-capita shortfalls translate into very large total "
            "volume deficits — creating strong pressure on Fallsland to maintain "
            "high reliability and to invest in sufficient supply capacity."
        ),
    ),
    dict(
        id="panel_c_title",
        x=1155, y=600, panel="(c)",
        title="Demand Growth Projections",
        text=(
            "Panel (c) shows each utility's projected annual water demand over "
            "the 55-year simulation. Demand is not static: all three utilities "
            "grow, but at different rates. This non-stationary demand is one "
            "source of deep uncertainty — the actual trajectory depends on "
            "population growth rates, per-capita usage trends, and economic "
            "conditions, none of which are known with certainty decades in advance. "
            "DU Pathways optimization tests strategies across many plausible "
            "demand trajectories rather than a single forecast."
        ),
    ),
    dict(
        id="panel_c_fallsland",
        x=1445, y=760, panel="(c)",
        title="Fallsland demand: highest and fastest-growing",
        text=(
            "Fallsland's demand (teal line) starts highest (~60 MGD) and grows "
            "the fastest, reaching roughly 125 MGD by year 55. This sustained "
            "growth pressure means Fallsland's pathway strategies must plan for "
            "substantial additional supply capacity over the simulation horizon "
            "— either through New River Reservoir, expanded Autumn Lake access, "
            "treated transfers, or water-reuse investments."
        ),
    ),
    dict(
        id="panel_c_dryville_watertown",
        x=1445, y=970, panel="(c)",
        title="Dryville and Watertown: similar-scale but distinct trajectories",
        text=(
            "Dryville (dark grey solid line) and Watertown (orange dashed line) "
            "begin at similar demand levels (~25–30 MGD) and follow broadly "
            "parallel growth trajectories, reaching roughly 45–50 MGD by year "
            "55. Despite their similar scales, they rely on different "
            "infrastructure options and cooperative partners, so their optimal "
            "pathway strategies tend to diverge."
        ),
    ),
]

render_hotspot_explorer(
    page_heading="Regional Test Case: Sedento Valley — Interactive Explorer",
    intro=(
        "This figure introduces the **Sedento Valley** regional test case used "
        "throughout this study. Panel (a) shows the network of three cooperating "
        "water utilities (Watertown, Dryville, Fallsland), their water sources, "
        "and the supply/transfer connections between them. Panel (b) shows each "
        "utility's customer population, and panel (c) shows projected demand growth "
        "over the 55-year simulation horizon. Click a numbered marker on the figure "
        "— or pick a callout from the list — to learn about each element."
    ),
    image_relpath="figures/regional_test_case.jpg",
    hotspots=HOTSPOTS,
    state_key="rtc",
    about_text=(
        "This explorer overlays clickable hotspots on the published static figure "
        "(`figures/regional_test_case.jpg`). Hotspot coordinates were placed by eye "
        "against the three panels: the Sedento Valley network schematic (a), the "
        "population bar chart (b), and the demand-growth projection curves (c). "
        "Callout text is grounded in the regional test case description from the "
        "accompanying manuscript and the WaterPaths simulation framework documentation."
    ),
)

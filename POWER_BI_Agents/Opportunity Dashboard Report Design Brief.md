# Opportunity Dashboard Report Design Brief

Audience: Bid managers managing the active opportunity portfolio, bid stage progression, staffing coverage, and near-term delivery risks.

Purpose: Provide a fast portfolio status view, then let the bid manager move from an alert to the affected opportunity and its staffing detail without exporting to Excel.

The report is intentionally risk-first. A risk is shown only when it has a clear business rule and a row-level action target.

## Design decisions

- Preserve the existing 1920 x 1080 canvas and Fluent2 base theme.
- Use a light operational surface: warm white page background, charcoal text, restrained borders, and teal as the primary analytical accent.
- Use semantic status colors only for risk state: red = urgent risk, amber = attention required, green = healthy, grey = unavailable/not assessed.
- Use Aptos Display for page titles and Aptos for report content through the existing Fluent2 theme.
- Use a recurring risk ribbon: every page exposes the current count of urgent and attention-required items near the title, and every detail page contains a sortable risk/status column.
- Use single-direction filtering. Sync the core filters across pages: Region, Business Unit, Opp Stage, Opp Owner, and Year.
- Prefer cards, bars, lines, and tables. Avoid donuts, gauges, decorative icons, and unexplained traffic lights.

## Risk definitions

The authoring phase should implement these as explicit measures or calculated fields where the model supports them:

- Missing EOI dates: an opportunity has no EOI Start or EOI Finish while it is in an EOI-related stage.
- Missing tender dates: an opportunity has no Tender Start or Tender Finish while it is in a tender-related stage.
- Unresourced opportunity: an opportunity has no related Resource Allocation rows.
- Under-resourced opportunity: an opportunity has allocation rows but allocated hours are below the agreed bid-manager threshold. The threshold should be a report parameter or documented constant, not a hidden visual filter.
- Overdue phase: an Opportunity Phase has a finish date before today, or an open phase has remained open beyond the agreed duration threshold.
- Stale pipeline: an opportunity has no recent phase or allocation activity. This requires a documented recency threshold before implementation.
- Risk priority: Urgent first, then Attention, then Healthy, then Unknown. Every risk table must include the reason and next-action context.

## Canonical design contract

```yaml
Design Brief:
  generated_by: powerbi-report-design
  contract_version: 1
  mode: brownfield
  design_identity:
    tone: "bid-room command center: calm, decisive, and risk-first"
    signature: "a compact red-amber-green risk ribbon repeated across pages, paired with ranked exception tables"
    current_tone: "blank Fluent2 report shell"
    current_signature: "none"
  archetype: "Executive Summary with Analytical Detail"
  color_map:
    - measure: "Pipeline Value"
      color: "#007C91"
      tint: "#D9F0F2"
    - measure: "Allocated Hours"
      color: "#3B6EA5"
      tint: "#DCE8F5"
    - measure: "Urgent Risks"
      color: "#D13438"
      tint: "#FBE4E4"
    - measure: "Attention Risks"
      color: "#C47F00"
      tint: "#FFF0CC"
    - measure: "Healthy Opportunities"
      color: "#107C10"
      tint: "#E2F2E2"
  pages:
    - name: "Bid Portfolio Command Center"
      role: landing
      archetype: Executive
      layout_variant: A
      variant_rationale: "The model supports four headline portfolio metrics plus a clear opportunity-stage distribution and a ranked risk list, so a hero-right summary gives bid managers a ten-second status scan."
      page_background: "#F7F8F8"
      layout_summary: "Thesis title and synced filters at the top, four status KPIs and a stage/value hero beneath, followed by ranked risks and upcoming bid milestones."
      layout_contract:
        canvas: { width: 1920, height: 1080, margin: 32, gutter: 24, snap: 8 }
        grid:
          columns: 12
          rows: 12
          regions:
            header: [1, 1, 9, 2]
            filters: [9, 1, 13, 2]
            kpis: [1, 2, 13, 4]
            hero: [1, 4, 8, 9]
            risk_panel: [8, 4, 13, 9]
            milestone_panel: [1, 9, 13, 13]
        placements:
          - id: page_title
            region: header
            kind: textbox
            text: "Bid portfolio: where attention is needed now"
            purpose: "State the operational thesis before the visuals."
          - id: core_filters
            region: filters
            kind: slicer
            field_bindings: ["Opportunity[Region]", "Opportunity[Business Unit]", "Opportunity[Opp Stage]"]
            slicer_type: dropdown
            purpose: "Set the shared portfolio context without opening the filter pane."
          - id: pipeline_value_card
            region: kpis
            kind: cardVisual
            field_bindings: "Opportunity[DTI Value (not CV)]"
            purpose: "What is the current pipeline value?"
            color_strategy: measure_match
          - id: active_opportunities_card
            region: kpis
            kind: cardVisual
            field_bindings: "Active Opportunities"
            purpose: "How many opportunities require active bid management?"
            color_strategy: measure_match
          - id: allocated_hours_card
            region: kpis
            kind: cardVisual
            field_bindings: "Resource Allocation[Allocated Hours]"
            purpose: "How much bid capacity is currently allocated?"
            color_strategy: measure_match
          - id: urgent_risks_card
            region: kpis
            kind: cardVisual
            field_bindings: "Urgent Risks"
            purpose: "How many opportunities need immediate intervention?"
            color_strategy: measure_match
          - id: pipeline_by_stage
            region: hero
            kind: barChart
            field_bindings: { Category: "Stage[Opp Stage]", Y: "Opportunity[DTI Value (not CV)]" }
            purpose: "Where is value concentrated across bid stages?"
            sort_policy: value_desc
            color_strategy: gradient
          - id: risk_summary
            region: risk_panel
            kind: tableEx
            field_bindings: ["Opportunity[Opportunity]", "Opportunity[Opp Owner]", "Risk Status", "Risk Reason", "Next Action"]
            purpose: "Which named opportunities need follow-up first?"
            sort_policy: risk_priority_desc
            color_strategy: semantic
          - id: upcoming_milestones
            region: milestone_panel
            kind: tableEx
            field_bindings: ["Opportunity[Opportunity]", "Opportunity[Opp Stage]", "Opportunity[EOI Start]", "Opportunity[Tender Start]", "Opportunity[Award]", "Opportunity[Opp Owner]"]
            purpose: "Which bid milestones are approaching and who owns them?"
            sort_policy: nearest_date_asc
            color_strategy: none
        space_audit:
          content_cell_count: 104
          placed_cell_count: 104
          empty_cell_pct: 0
          unplaced_regions: []
          largest_region: { name: hero, pct_of_content: 31 }
          balance_rationale: "The hero earns the most space for portfolio value concentration; the risk panel stays large enough for readable action rows and the milestone table spans the page for scanning."

    - name: "Opportunity Detail and Milestones"
      role: detail
      archetype: Analytical
      layout_variant: B
      variant_rationale: "Only a small set of shared slicers is needed, allowing the opportunity lifecycle timeline and a full-width sortable detail table to use the available canvas."
      page_background: "#F7F8F8"
      layout_summary: "Inline filters support focused investigation, with lifecycle timing above and opportunity-level action detail below."
      layout_contract:
        canvas: { width: 1920, height: 1080, margin: 32, gutter: 24, snap: 8 }
        grid:
          columns: 12
          rows: 12
          regions:
            header: [1, 1, 6, 2]
            filters: [6, 1, 13, 2]
            lifecycle: [1, 2, 13, 6]
            stage_breakdown: [1, 6, 5, 9]
            owner_breakdown: [5, 6, 9, 9]
            phase_breakdown: [9, 6, 13, 9]
            detail: [1, 9, 13, 13]
        placements:
          - id: page_title
            region: header
            kind: textbox
            text: "Opportunity milestones and bid-stage movement"
            purpose: "Orient the bid manager to lifecycle timing."
          - id: opportunity_filters
            region: filters
            kind: slicer
            field_bindings: ["Opportunity[Opp Owner]", "Opportunity[Opp Stage]", "Opportunity[Sector]"]
            slicer_type: dropdown
            purpose: "Narrow the opportunity population."
          - id: milestone_timeline
            region: lifecycle
            kind: lineChart
            field_bindings: { Category: "Date[Date]", Y: "Active Opportunities", Series: "Stage[Opp Stage]" }
            purpose: "How does the active opportunity population change over time?"
            color_strategy: semantic
          - id: opportunities_by_stage
            region: stage_breakdown
            kind: barChart
            field_bindings: { Category: "Stage[Opp Stage]", Y: "Active Opportunities" }
            purpose: "How many opportunities sit in each stage?"
            color_strategy: gradient
          - id: opportunities_by_owner
            region: owner_breakdown
            kind: barChart
            field_bindings: { Category: "Opportunity[Opp Owner]", Y: "Active Opportunities" }
            purpose: "Which owners carry the largest active portfolio?"
            sort_policy: value_desc
            color_strategy: gradient
          - id: open_phases
            region: phase_breakdown
            kind: barChart
            field_bindings: { Category: "Phase Type[Phase Name]", Y: "Open Phase Count" }
            purpose: "Which lifecycle phases have the most open work?"
            color_strategy: semantic
          - id: opportunity_detail
            region: detail
            kind: tableEx
            field_bindings: ["Opportunity[Opportunity]", "Opportunity[Region]", "Opportunity[Sector]", "Opportunity[Opp Stage]", "Opportunity[DTI Value (not CV)]", "Opportunity[EOI Start]", "Opportunity[EOI Finish]", "Opportunity[Tender Start]", "Opportunity[Tender Finish]", "Opportunity[Award]", "Opportunity[Opp Owner]", "Risk Status"]
            purpose: "Which opportunity row should be opened or discussed next?"
            sort_policy: risk_priority_desc_then_value_desc
            color_strategy: semantic
        space_audit:
          content_cell_count: 104
          placed_cell_count: 104
          empty_cell_pct: 0
          unplaced_regions: []
          largest_region: { name: lifecycle, pct_of_content: 31 }
          balance_rationale: "The timeline provides context, three compact comparisons explain composition, and the bottom table preserves row-level actionability."

    - name: "Resource Coverage and Capacity"
      role: detail
      archetype: Analytical
      layout_variant: C
      variant_rationale: "Resource Allocation contains repeated opportunity-resource-week rows, making comparison across owners and resources the primary analytical task."
      page_background: "#F7F8F8"
      layout_summary: "Compare allocation coverage across the portfolio, then identify unresourced and under-resourced opportunities."
      layout_contract:
        canvas: { width: 1920, height: 1080, margin: 32, gutter: 24, snap: 8 }
        grid:
          columns: 12
          rows: 12
          regions:
            header: [1, 1, 6, 2]
            filters: [6, 1, 13, 2]
            coverage_kpis: [1, 2, 13, 4]
            allocation_trend: [1, 4, 7, 8]
            resource_comparison: [7, 4, 13, 8]
            allocation_detail: [1, 8, 13, 13]
        placements:
          - id: page_title
            region: header
            kind: textbox
            text: "Resource coverage: are priority bids staffed?"
            purpose: "Frame the page around staffing risk."
          - id: resource_filters
            region: filters
            kind: slicer
            field_bindings: ["Resource[Resource Type]", "Opportunity[Opp Stage]", "Opportunity[Region]"]
            slicer_type: dropdown
            purpose: "Focus coverage analysis by resource and portfolio segment."
          - id: unresourced_card
            region: coverage_kpis
            kind: cardVisual
            field_bindings: "Unresourced Opportunities"
            purpose: "How many opportunities have no staffing allocation?"
            color_strategy: measure_match
          - id: utilisation_card
            region: coverage_kpis
            kind: cardVisual
            field_bindings: "Resource Utilisation %"
            purpose: "What share of available allocation is being used?"
            color_strategy: measure_match
          - id: total_hours_card
            region: coverage_kpis
            kind: cardVisual
            field_bindings: "Resource Allocation[Allocated Hours]"
            purpose: "What is the allocated effort volume?"
            color_strategy: measure_match
          - id: allocation_by_week
            region: allocation_trend
            kind: lineChart
            field_bindings: { Category: "Date[Date]", Y: "Resource Allocation[Allocated Hours]" }
            purpose: "How does planned effort change over time?"
            color_strategy: measure_match
          - id: hours_by_resource
            region: resource_comparison
            kind: barChart
            field_bindings: { Category: "Resource[Resource Name]", Y: "Resource Allocation[Allocated Hours]" }
            purpose: "Which resources carry the most planned effort?"
            sort_policy: value_desc
            color_strategy: gradient
          - id: allocation_detail
            region: allocation_detail
            kind: tableEx
            field_bindings: ["Opportunity[Opportunity]", "Opportunity[Opp Stage]", "Resource[Resource Name]", "Resource[Resource Type]", "Resource Allocation[Week Start]", "Resource Allocation[Allocated Hours]", "Coverage Status", "Risk Status"]
            purpose: "Which opportunity-resource-week rows require staffing action?"
            sort_policy: risk_priority_desc_then_week_asc
            color_strategy: semantic
        space_audit:
          content_cell_count: 104
          placed_cell_count: 104
          empty_cell_pct: 0
          unplaced_regions: []
          largest_region: { name: allocation_detail, pct_of_content: 38 }
          balance_rationale: "The detail table receives the most space because staffing action depends on row-level opportunity-resource-week evidence."

    - name: "Risks and Actions"
      role: detail
      archetype: Comparative
      layout_variant: B
      variant_rationale: "Risk management is a ranked exception workflow: compare risk categories and owners, then work a single actionable table."
      page_background: "#F7F8F8"
      layout_summary: "A risk register for triage, with severity and reason visible before any drill-through."
      layout_contract:
        canvas: { width: 1920, height: 1080, margin: 32, gutter: 24, snap: 8 }
        grid:
          columns: 12
          rows: 12
          regions:
            header: [1, 1, 6, 2]
            filters: [6, 1, 13, 2]
            risk_kpis: [1, 2, 13, 4]
            risk_by_type: [1, 4, 5, 8]
            risk_by_owner: [5, 4, 9, 8]
            risk_by_stage: [9, 4, 13, 8]
            risk_register: [1, 8, 13, 13]
        placements:
          - id: page_title
            region: header
            kind: textbox
            text: "Bid risks: triage, assign, resolve"
            purpose: "Make the action workflow explicit."
          - id: risk_filters
            region: filters
            kind: slicer
            field_bindings: ["Risk Status", "Risk Type", "Opportunity[Opp Owner]"]
            slicer_type: dropdown
            purpose: "Filter the risk register to a manageable action set."
          - id: urgent_risk_card
            region: risk_kpis
            kind: cardVisual
            field_bindings: "Urgent Risks"
            purpose: "What requires immediate escalation?"
            color_strategy: measure_match
          - id: attention_risk_card
            region: risk_kpis
            kind: cardVisual
            field_bindings: "Attention Risks"
            purpose: "What needs an owner and due date?"
            color_strategy: measure_match
          - id: overdue_phase_card
            region: risk_kpis
            kind: cardVisual
            field_bindings: "Overdue Phases"
            purpose: "How much lifecycle work is past due?"
            color_strategy: measure_match
          - id: risk_by_type
            region: risk_by_type
            kind: barChart
            field_bindings: { Category: "Risk Type", Y: "Risk Count" }
            purpose: "Which risk categories dominate?"
            sort_policy: value_desc
            color_strategy: semantic
          - id: risk_by_owner
            region: risk_by_owner
            kind: barChart
            field_bindings: { Category: "Opportunity[Opp Owner]", Y: "Risk Count" }
            purpose: "Where is risk ownership concentrated?"
            sort_policy: value_desc
            color_strategy: semantic
          - id: risk_by_stage
            region: risk_by_stage
            kind: barChart
            field_bindings: { Category: "Stage[Opp Stage]", Y: "Risk Count" }
            purpose: "Which bid stages contain the greatest risk load?"
            sort_policy: value_desc
            color_strategy: semantic
          - id: risk_register
            region: risk_register
            kind: tableEx
            field_bindings: ["Risk Status", "Risk Type", "Opportunity[Opportunity]", "Opportunity[Opp Owner]", "Opportunity[Opp Stage]", "Risk Reason", "Next Action", "Due Date"]
            purpose: "What exact action should the bid manager take next?"
            sort_policy: risk_priority_desc_then_due_date_asc
            color_strategy: semantic
        space_audit:
          content_cell_count: 104
          placed_cell_count: 104
          empty_cell_pct: 0
          unplaced_regions: []
          largest_region: { name: risk_register, pct_of_content: 38 }
          balance_rationale: "The register dominates because the page is for action, while the three comparison panels explain where to focus first."

  interaction_pattern:
    drill_targets: ["Opportunity Detail and Milestones", "Resource Coverage and Capacity", "Risks and Actions"]
    cross_filter_rules: "Summary selections filter all detail pages; detail charts cross-filter the row-level table; risk tables use highlight only for category context and never hide the active risk row."
    synced_filters: ["Opportunity[Region]", "Opportunity[Business Unit]", "Opportunity[Opp Stage]", "Opportunity[Opp Owner]", "Date[Year]"]
  accessibility:
    alt_text_strategy: "headline plus analytical question plus current filter context"
    contrast_notes: "Use dark charcoal text on the light surface; reserve red and amber for status semantics and pair every status color with text labels or icons. Do not use color as the sole indicator."
  theme:
    base: "existing Fluent2-CY26SU08 preserved and adapted only through report-level data colors"
    user_overrides: "Do not replace the existing base theme, page size, or report settings. Add only report visuals, page navigation, field display names, and required measures."
```

## Implementation dependencies

The model needs explicit measures or fields for the following brief bindings before report authoring can finish: `Active Opportunities`, `Pipeline Value`, `Urgent Risks`, `Attention Risks`, `Overdue Phases`, `Open Phase Count`, `Unresourced Opportunities`, `Resource Utilisation %`, `Risk Status`, `Risk Type`, `Risk Reason`, `Coverage Status`, `Next Action`, `Due Date`, and `Risk Count`.

The brief deliberately leaves risk thresholds visible as implementation decisions. Before those measures are authored, confirm the agreed under-resourcing, overdue, and stale-activity thresholds with the bid-management process owner.

## Handoff

This brief is ready for `powerbi-report-authoring` implementation after approval. The next implementation step is to add or verify the required measures, then create the four PBIR pages and validate them in Power BI Desktop.
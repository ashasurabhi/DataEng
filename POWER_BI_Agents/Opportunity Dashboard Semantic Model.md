# Opportunity Dashboard Semantic Model

This model is designed using the semantic-model-authoring workflow and follows star-schema best practices for an opportunity portfolio dashboard.

## Scope
The dashboard answers questions such as:
- Which opportunities are in pipeline, EOI, or tender?
- What is the current and upcoming value pipeline?
- Which opportunities are under-resourced or unresourced?
- How are resource hours allocated over time?
- What phase is each opportunity in, and how long has it been there?

## Core design principle
Use a star schema with one or more fact tables and a small set of conformed dimensions.

## Fact tables

### 1. Opportunity Fact
Grain: one row per opportunity

Purpose: one row per opportunity to support pipeline value, stage, ownership, and lifecycle analysis.

Recommended columns:
- Opportunity ID
- Opportunity Reference
- Opportunity Name
- Region
- Sector
- Business Unit
- Approval Stage
- Opportunity Owner
- Opportunity Stage
- Stage Sort Order
- DTI Value
- EOI Start Date
- EOI End Date
- Tender Start Date
- Tender End Date
- Award Date

Notes:
- Keep this as the central fact table for opportunity-level metrics.
- Use a single surrogate or natural key for the opportunity identity.
- Hide technical keys unless the model requires them.

### 2. Resource Allocation Fact
Grain: one row per opportunity-resource-week

Purpose: allocation and staffing analysis.

Recommended columns:
- Opportunity Reference
- Resource ID
- Week Start
- Allocated Hours
- Resource Type
- Resource Title
- Resource Name

Notes:
- This is the main fact table for staffing, allocation, and utilization analysis.
- Keep the grain stable and not mixed with opportunity master attributes.

### 3. Opportunity Phase Fact
Grain: one row per opportunity-phase instance

Purpose: track lifecycle milestones and phase progression.

Recommended columns:
- Opportunity Reference
- Phase Name
- Phase Start Date
- Phase End Date
- Phase Days
- Phase Sort Order

Notes:
- This replaces the legacy split EOI/Tender phase structures.
- Use a single fact table with a separate Phase Type dimension if needed.

## Dimension tables

### 1. Date
Purpose: standard calendar table for all date-based analysis.

Recommended columns:
- Date
- Date Key
- Year
- Quarter
- Month Number
- Month Name
- Week Start
- Week End
- Is Weekend

Notes:
- This is the primary date dimension.
- Connect all date-based facts to it.

### 2. Resource
Purpose: staffing dimension.

Recommended columns:
- Resource ID
- Resource Name
- Resource Type
- Resource Title

### 3. Phase Type
Purpose: classify lifecycle stage.

Recommended columns:
- Phase Name
- Phase Sort Order
- Phase Description

### 4. Opportunity Status / Stage
Purpose: optional lookup for stage categories.

Recommended columns:
- Opportunity Stage
- Stage Sort Order
- Stage Description

## Relationships
- Opportunity Fact[Opportunity Reference] -> Resource Allocation Fact[Opportunity Reference]
- Resource[Resource ID] -> Resource Allocation Fact[Resource ID]
- Date[Date] -> Resource Allocation Fact[Week Start]
- Opportunity Fact[Opportunity Reference] -> Opportunity Phase Fact[Opportunity Reference]
- Date[Date] -> Opportunity Phase Fact[Phase Start Date]
- Date[Date] -> Opportunity Phase Fact[Phase End Date]
- Phase Type[Phase Name] -> Opportunity Phase Fact[Phase Name]

Use single-direction relationships by default. Avoid bi-directional filtering unless required.

## Measures
Create explicit measures, not implicit aggregations.

Core measures:
- Pipeline Value
- Total Allocated Hours
- Active Opportunities
- Opportunities in EOI
- Opportunities in Tender
- Upcoming EOI Opportunities
- Upcoming Tender Opportunities
- Unresourced Opportunities
- Open Phase Count
- Resource Utilisation %

Recommended measure pattern:
- Use SUM for hours and values
- Use COUNTROWS or DISTINCTCOUNT for opportunity counts
- Use CALCULATE with filter logic for status and resource checks
- Set format strings consistently

## Naming
Use business-friendly naming and remove technical prefixes.

Preferred names:
- Opportunity
- Date
- Resource
- Resource Allocation
- Opportunity Phase
- Phase Type

Avoid:
- DIM_Opportunity
- FACT_Resource_Allocation
- Measures Table
- EOI_Phase
- Tender Phase

## AI readiness
Follow the semantic-model-authoring guidance:
- give every visible table and measure a clear description
- hide technical keys and helper columns
- standardize names so Copilot can interpret the business model reliably
- ensure the date dimension is connected and used consistently
- avoid a single mega-measure table

## Recommended implementation order
1. Create Date dimension
2. Create Opportunity fact table
3. Create Resource dimension and Resource Allocation fact table
4. Create Opportunity Phase fact table
5. Create Phase Type dimension
6. Add relationships
7. Create explicit measures
8. Validate with example report slices and natural-language questions

## Summary
This model is the clean opportunity dashboard design that best fits the semantic-model-authoring skill: one core opportunity fact, a resource allocation fact, a phase fact, and a connected date dimension. It is clearer, easier for AI to understand, and more maintainable than the legacy split-phase setup.

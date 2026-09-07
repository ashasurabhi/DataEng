# Opportunity Dashboard Model Proposal

This file defines the target semantic model for the opportunity dashboard.

## Tables

### Opportunity
- Opportunity Reference
- Opportunity Name
- Region
- Sector
- Business Unit
- Opportunity Owner
- Approval Stage
- Opportunity Stage
- Opportunity Stage Sort Order
- DTI Value
- EOI Start Date
- EOI End Date
- Tender Start Date
- Tender End Date
- Award Date

### Date
- Date
- Date Key
- Year
- Quarter
- Month Number
- Month Name
- Week Start
- Week End
- Is Weekend

### Resource
- Resource ID
- Resource Name
- Resource Type
- Resource Title

### Resource Allocation
- Opportunity Reference
- Resource ID
- Week Start
- Allocated Hours
- Resource Type

### Opportunity Phase
- Opportunity Reference
- Phase Name
- Phase Start Date
- Phase End Date
- Phase Days

### Phase Type
- Phase Name
- Phase Sort Order
- Phase Description

### Stage
- Opportunity Stage
- Stage Sort Order
- Stage Description

## Relationships
- Opportunity[Opportunity Reference] -> Resource Allocation[Opportunity Reference]
- Resource[Resource ID] -> Resource Allocation[Resource ID]
- Date[Date] -> Resource Allocation[Week Start]
- Opportunity[Opportunity Reference] -> Opportunity Phase[Opportunity Reference]
- Date[Date] -> Opportunity Phase[Phase Start Date]
- Phase Type[Phase Name] -> Opportunity Phase[Phase Name]
- Stage[Opportunity Stage] -> Opportunity[Opportunity Stage]

## Measures
- Pipeline Value
- Total Allocated Hours
- Active Opportunities
- Opportunities in EOI
- Opportunities in Tender
- Upcoming Opportunities
- Unresourced Opportunities
- Open Phase Count
- Resource Utilisation %

## Notes
- Use single-direction relationships by default.
- Hide technical keys and helper columns.
- Ensure every measure has a format string and business description.
- Use business-friendly names and avoid technical prefixes.

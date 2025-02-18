# FoamFactory_V2_27K.csv Data Description

This file contains time series data for multiple foam factories. Below is a description of each field based on the first 200 rows:

1. **Factory**: The name or identifier of the factory.
2. **Date**: The date of the recorded data.
3. **Location**: The geographical location of the factory.
4. **Machine Type**: The type of machine used in the production process.
5. **Machine Utilization (%)**: The percentage of time the machine is actively used.
6. **Machine Downtime (hours)**: The total hours the machine was inactive.
7. **Maintenance History**: A description of the maintenance history (e.g., "Irregular").
8. **Machine Age (years)**: The age of the machine in years.
9. **Batch**: The identifier for the production batch.
10. **Batch Quality (Pass %)**: The percentage of products in the batch that passed quality checks.
11. **Cycle Time (minutes)**: The time taken to complete one production cycle.
12. **Energy Consumption (kWh)**: The total energy consumed during production.
13. **Energy Efficiency Rating**: A rating indicating the energy efficiency of the machine.
14. **CO2 Emissions (kg)**: The amount of CO2 emitted during production.
15. **Emission Limit Compliance**: Whether the emissions comply with limits (Yes/No).
16. **Waste Generated (kg)**: The amount of waste produced during production.
17. **Water Usage (liters)**: The total water used in the production process.
18. **Shift**: The shift during which the data was recorded.
19. **Operator Experience (years)**: The average experience of operators in years.
20. **Team Size**: The number of team members.
21. **Team Members**: A JSON list of team members with details like name, experience, training level, and absenteeism rate.
22. **Operator Training Level**: The average training level of operators.
23. **Absenteeism Rate (%)**: The percentage of absenteeism among operators.
24. **Product Category**: The category of the product being produced.
25. **Supplier**: The supplier of raw materials.
26. **Supplier Delays (days)**: The number of days delayed by the supplier.
27. **Raw Material Quality**: A quality metric for raw materials.
28. **Market Demand Index**: An index representing market demand for the product.
29. **Cost of Downtime ($)**: The financial cost of machine downtime.
30. **Revenue ($)**: The revenue generated from the production batch.
31. **Profit Margin (%)**: The profit margin for the production batch.
32. **Breakdowns (count)**: The number of machine breakdowns.
33. **Safety Incidents (count)**: The number of safety incidents recorded.
34. **Production Volume (units)**: The total number of units produced.
35. **Defect Rate (%)**: The percentage of defective units in the batch.
36. **Temperature (C)**: The temperature during production.
37. **Pressure (psi)**: The pressure during production.
38. **Chemical Ratio**: The ratio of chemicals used in production.
39. **Mixing Speed (RPM)**: The speed at which materials were mixed.

# Potential Metrics

Here are some ideas for metrics that can be extracted from the dataset:

1. **Machine Efficiency**: Machine Utilization (%) vs. Machine Downtime (hours).
2. **Quality Metrics**: Batch Quality (Pass %) and Defect Rate (%) trends over time.
3. **Energy Metrics**: Energy Consumption (kWh) per production unit.
4. **Environmental Impact**: CO2 Emissions (kg) and Waste Generated (kg) per batch.
5. **Operational Costs**: Cost of Downtime ($) vs. Revenue ($) and Profit Margin (%).
6. **Team Performance**: Operator Experience (years) and Absenteeism Rate (%) impact on Batch Quality.
7. **Supplier Reliability**: Supplier Delays (days) and Raw Material Quality impact on production.
8. **Safety Metrics**: Safety Incidents (count) per shift or per factory.
9. **Production Metrics**: Production Volume (units) vs. Cycle Time (minutes).
10. **Process Optimization**: Temperature (C), Pressure (psi), Chemical Ratio, and Mixing Speed (RPM) impact on Batch Quality.

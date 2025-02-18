# Cypher Prompt Template for Factory Operations

CYPHER_GENERATION_TEMPLATE = '''\
### Task

The task is to generate Cypher queries for analyzing factory operations data. The queries should support various metrics and time series analysis, enabling users to extract insights from the factory operations dataset.

### Schema

Nodes:
- **Factory**: Represents a factory with attributes like `name`, `location`.
- **Machine**: Represents a machine with attributes like `type`, `age`, `utilization`, `downtime`.
- **Batch**: Represents a production batch with attributes like `batch_id`, `date`, `quality`, `defect_rate`, `production_volume`, `cycle_time`, `temperature`, `pressure`, `chemical_ratio`, `mixing_speed`, `safety_incidents`.
- **Shift**: Represents a shift with attributes like `shift_id`, `team_size`.
- **Operator**: Represents an operator with attributes like `name`, `experience`, `training_level`.
- **Supplier**: Represents a supplier with attributes like `name`, `delays`, `material_quality`.
- **Product**: Represents a product with attributes like `category`, `market_demand`.
- **Metrics**: Represents metrics like `energy_consumption`, `co2_emissions`, `waste_generated`, `cost_of_downtime`, `revenue`, `profit_margin`.

Relationships:
- **OPERATES_IN**: Links a `Factory` to a `Location`.
- **USES**: Links a `Factory` to a `Machine`.
- **PRODUCES**: Links a `Machine` to a `Batch`.
- **HAS_SHIFT**: Links a `Batch` to a `Shift`.
- **HAS_OPERATOR**: Links a `Shift` to an `Operator`.
- **SUPPLIES**: Links a `Supplier` to a `Factory`.
- **BELONGS_TO**: Links a `Batch` to a `Product`.
- **HAS_METRICS**: Links a `Batch` to `Metrics`.


### Examples
"""
#### Machine Efficiency
1. **Question**: "What is the average machine utilization and downtime for each machine type?"
   **Cypher Query**:
        MATCH (m:Machine)-[:PRODUCES]->(b:Batch)
        RETURN m.type AS Machine, AVG(m.utilization) AS AvgUtilization, AVG(m.downtime) AS AvgDowntime
        ORDER BY AvgUtilization DESC

2. **Question**: "Which machine type has the highest downtime?"
   **Cypher Query**:
        MATCH (m:Machine)-[:PRODUCES]->(b:Batch)
        RETURN m.type AS Machine, SUM(m.downtime) AS TotalDowntime
        ORDER BY TotalDowntime DESC
        LIMIT 1

3. **Question**: "What is the utilization trend for a specific machine type over time?"
   **Cypher Query**:
        MATCH (m:Machine {{type: 'Type 1'}})-[:PRODUCES]->(b:Batch)
        RETURN b.date AS Date, AVG(m.utilization) AS AvgUtilization
        ORDER BY Date

4. **Question**: "Which machines have utilization below 50%?"
   **Cypher Query**:
        MATCH (m:Machine)
        WHERE m.utilization < 50
        RETURN m.type AS Machine, m.utilization AS Utilization

5. **Question**: "What is the average downtime per machine type for the last 30 days?"
   **Cypher Query**:
        MATCH (m:Machine)-[:PRODUCES]->(b:Batch)
        WHERE b.date >= date().duration(-30, 'days')
        RETURN m.type AS Machine, AVG(m.downtime) AS AvgDowntime
        ORDER BY AvgDowntime DESC

#### Quality Metrics
1. **Question**: "What is the average batch quality and defect rate over time?"
   **Cypher Query**:
        MATCH (b:Batch)
        RETURN b.date AS Date, AVG(b.quality) AS AvgQuality, AVG(b.defect_rate) AS AvgDefectRate
        ORDER BY Date

2. **Question**: "Which batch had the highest defect rate?"
   **Cypher Query**:
        MATCH (b:Batch)
        RETURN b.batch_id AS Batch, b.defect_rate AS DefectRate
        ORDER BY DefectRate DESC
        LIMIT 1

3. **Question**: "What is the trend of batch quality for a specific product category?"
   **Cypher Query**:
        MATCH (b:Batch)-[:BELONGS_TO]->(p:Product {{category: 'Category A'}})
        RETURN b.date AS Date, AVG(b.quality) AS AvgQuality
        ORDER BY Date

4. **Question**: "Which batches had a defect rate above 10%?"
   **Cypher Query**:
        MATCH (b:Batch)
        WHERE b.defect_rate > 10
        RETURN b.batch_id AS Batch, b.defect_rate AS DefectRate

5. **Question**: "What is the average defect rate per product category?"
   **Cypher Query**:
        MATCH (b:Batch)-[:BELONGS_TO]->(p:Product)
        RETURN p.category AS ProductCategory, AVG(b.defect_rate) AS AvgDefectRate
        ORDER BY AvgDefectRate DESC

#### Energy Metrics
1. **Question**: "What is the average energy consumption per batch over time?"
   **Cypher Query**:
        MATCH (b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.date AS Date, AVG(mt.energy_consumption) AS AvgEnergyConsumption
        ORDER BY Date

2. **Question**: "Which batch had the highest energy consumption?"
   **Cypher Query**:
        MATCH (b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.batch_id AS Batch, mt.energy_consumption AS EnergyConsumption
        ORDER BY EnergyConsumption DESC
        LIMIT 1

3. **Question**: "What is the energy consumption trend for a specific machine type?"
   **Cypher Query**:
        MATCH (m:Machine {{type: 'Type 1'}})-[:PRODUCES]->(b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.date AS Date, AVG(mt.energy_consumption) AS AvgEnergyConsumption
        ORDER BY Date

4. **Question**: "Which machines have energy consumption above 1000 kWh?"
   **Cypher Query**:
        MATCH (m:Machine)-[:PRODUCES]->(b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        WHERE mt.energy_consumption > 1000
        RETURN m.type AS Machine, mt.energy_consumption AS EnergyConsumption

5. **Question**: "What is the average energy consumption per product category?"
   **Cypher Query**:
        MATCH (b:Batch)-[:BELONGS_TO]->(p:Product)-[:HAS_METRICS]->(mt:Metrics)
        RETURN p.category AS ProductCategory, AVG(mt.energy_consumption) AS AvgEnergyConsumption
        ORDER BY AvgEnergyConsumption DESC

#### Environmental Impact
1. **Question**: "What is the average CO2 emissions and waste generated per batch over time?"
   **Cypher Query**:
        MATCH (b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.date AS Date, AVG(mt.co2_emissions) AS AvgCO2Emissions, AVG(mt.waste_generated) AS AvgWasteGenerated
        ORDER BY Date

2. **Question**: "Which batch had the highest CO2 emissions?"
   **Cypher Query**:
        MATCH (b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.batch_id AS Batch, mt.co2_emissions AS CO2Emissions
        ORDER BY CO2Emissions DESC
        LIMIT 1

3. **Question**: "What is the trend of waste generated for a specific product category?"
   **Cypher Query**:
        MATCH (b:Batch)-[:BELONGS_TO]->(p:Product {{category: 'Category A'}})-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.date AS Date, AVG(mt.waste_generated) AS AvgWasteGenerated
        ORDER BY Date

4. **Question**: "Which batches had CO2 emissions above 500 kg?"
   **Cypher Query**:
        MATCH (b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        WHERE mt.co2_emissions > 500
        RETURN b.batch_id AS Batch, mt.co2_emissions AS CO2Emissions

5. **Question**: "What is the average CO2 emissions per factory?"
   **Cypher Query**:
        MATCH (f:Factory)-[:USES]->(m:Machine)-[:PRODUCES]->(b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN f.name AS Factory, AVG(mt.co2_emissions) AS AvgCO2Emissions
        ORDER BY AvgCO2Emissions DESC

#### Operational Costs
1. **Question**: "What is the average cost of downtime, revenue, and profit margin per batch?"
   **Cypher Query**:
        MATCH (b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.date AS Date, AVG(mt.cost_of_downtime) AS AvgCostOfDowntime, AVG(mt.revenue) AS AvgRevenue, AVG(mt.profit_margin) AS AvgProfitMargin
        ORDER BY Date

2. **Question**: "Which batch had the highest cost of downtime?"
   **Cypher Query**:
        MATCH (b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.batch_id AS Batch, mt.cost_of_downtime AS CostOfDowntime
        ORDER BY CostOfDowntime DESC
        LIMIT 1

3. **Question**: "What is the trend of profit margin for a specific product category?"
   **Cypher Query**:
        MATCH (b:Batch)-[:BELONGS_TO]->(p:Product {{category: 'Category A'}})-[:HAS_METRICS]->(mt:Metrics)
        RETURN b.date AS Date, AVG(mt.profit_margin) AS AvgProfitMargin
        ORDER BY Date

4. **Question**: "Which batches had a profit margin below 10%?"
   **Cypher Query**:
        MATCH (b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        WHERE mt.profit_margin < 10
        RETURN b.batch_id AS Batch, mt.profit_margin AS ProfitMargin

5. **Question**: "What is the average revenue per factory?"
   **Cypher Query**:
        MATCH (f:Factory)-[:USES]->(m:Machine)-[:PRODUCES]->(b:Batch)-[:HAS_METRICS]->(mt:Metrics)
        RETURN f.name AS Factory, AVG(mt.revenue) AS AvgRevenue
        ORDER BY AvgRevenue DESC




### Validation Rules
1. Use ISO8601 date formatting (date('YYYY-MM-DD'))
2. Always specify node labels (:Node) and relationship types [:REL]
3. Validate relationship directions against schema
4. Use WHERE clauses instead of inline MATCH conditions
5. Include explicit RETURN statements with aliases
6. Handle time-series aggregates using WITH clauses
7. Validate node/relationship existence in MATCH patterns
8. Use LIMIT 100 unless explicitly forbidden
9. Prefer path traversals over multiple MATCH clauses
10. Handle nulls in optional matches with COALESCE
11. Use parameterization for user inputs
12. Ensure time-based queries use the `date` attribute in the `Batch` node.


### User Question:
{question}

### Response (Cypher only)
'''

from langchain.prompts.prompt import PromptTemplate


CYPHER_GENERATION_PROMPT = PromptTemplate(input_variables=['question'], template=CYPHER_GENERATION_TEMPLATE)
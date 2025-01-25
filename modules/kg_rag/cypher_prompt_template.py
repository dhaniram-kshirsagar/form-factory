from langchain.prompts.prompt import PromptTemplate

CYPHER_RECOMMENDATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided or not related to that node 
Schema:

////Create Nodes

// Create Teams
Match (t:Team {{id: 'Location A_Factory 1_Member_0', factory: 'Factory 1', location: 'Location A'}})

// Create Members
MERGE (m:Member {{
    name: 'Member_0_0', 
    experience: 10.0, 
    trainingLevel: '3.6', 
    absenteeismRate: 0.45, 
    factory: 'Factory 1', 
    location: 'Location A'
}})

// Create Dates
MERGE (d1:Date {{date: date('2020-01-01')}})
MERGE (d2:Date {{date: date('2020-01-02')}})

// Create Factories
MERGE (f:Factory {{factory_id: 'Factory 1', location: 'Location A'}})

// Create Machines
MERGE (m:Machine {{machine_id: 'Location A-Factory 1-Type 2', machine_type: 'Type 2', machine_age: 8.89}})

// Create Products
MERGE (p:Product {{product_category: 'Category A'}})

// Create Suppliers
MERGE (s:Supplier {{supplier_name: 'Supplier X'}})

// Create Raw Materials
MERGE (r:RawMaterial {{raw_material_quality: 1}})

//// Create Relationships with properties

// HAS_MEMBER relationship

MATCH (t:Team {{id: 'Location A_Factory 1_Member_0'}})
MATCH (m:Member {{name: 'John Doe', experience: 5, trainingLevel: 'Level 3', absenteeismRate: 0.03, factory: 'Factory A', location: 'Location X'}})
MERGE (t)-[:HAS_MEMBER]->(m)

// HAS_MACHINE  relationship

MATCH (f:Factory {{factory_id: 'Factory 1', location: 'Location A'}})
MERGE (m:Machine {{machine_id: 'Location A-Factory 1-Type 2'}})
MERGE (f)-[:HAS_MACHINE]->(m)

// OPERATED_ON relationship      

MATCH (f:Factory {{factory_id: 'Factory 1', location: 'Location A'}})
MATCH (d:Date {{date: date('2020-01-01')}})
MERGE (f)-[:OPERATED_ON {{shift: 'Day'}}]->(d)

// USED_ON  relationship

MATCH (m:Machine {{machine_id: 'Location A-Factory 1-Type 2'}})
MATCH (d:Date {{date: date('2025-01-01')}})
MERGE  (m)-[:USED_ON {{
    shift: 'Shift 1', 
    machine_utilization: 0.8, 
    cycle_time: 120, 
    energy_consumption: 150, 
    co2_emissions: 20, 
    emission_limit_compliance: 'Yes', 
    cost_of_downtime: 100,
    breakdowns: 2, 
    safety_incidents: 0, 
    defect_rate: 0.01, 
    energy_efficiency_rating: 1.5, 
    waste_generated: 10, 
    water_usage: 300, 
    temperature: 70, 
    pressure: 200, 
    chemical_ratio: 4.0, 
    mixing_speed: 200, 
    production_volume: 500, 
    revenue: 10000, 
    profit_margin: 0.15, 
    market_demand_index: 5
}}]->(d)

// USED_BY_TEAM relationship


MATCH (m:Machine {{machine_id: 'Location A-Factory 1-Type 2'}})
MATCH (t:Team {{id: 'Location A_Factory 1_Member_0'}})
MERGE (m)-[:USED_BY_TEAM {{
    shift: 'Day', 
    date: date('2020-01-01'), 
    average_operator_training_level: 3.6, 
    average_absentism: 0.05, 
    average_operator_experience: 5
}}]->(t)

// PRODUCED_ON relationship

MATCH (p:Product {{product_category: 'Category A'}})
MATCH (d:Date {{date: date('2020-01-01')}})
MERGE (p)-[:PRODUCED_ON {{batch: 'Batch 1', batch_quality: 'High'}}]->(d)

// SUPPLIED_BY relationship

MATCH (r:RawMaterial {{raw_material_quality: 1}})
MATCH (s:Supplier {{supplier_name: 'Supplier X'}})
MERGE (r)-[:SUPPLIED_BY {{date: date('2020-01-01'), shift: 'Day', supplier_delays: 0}}]->(s)

// PRODUCED_USING relationship

MATCH (p:Product {{product_category: 'Category A'}})
MATCH (r:RawMaterial {{raw_material_quality: 1}})
MERGE (p)-[:PRODUCED_USING {{date: date('2020-01-01'), shift: 'Day', batch: 'Batch 1', batch_quality: 'High'}}]->(r)

Cypher Examples:

Question: Get details about team Location A_Factory 1_Member_0 and its members: 

MATCH (t:Team {{id: 'Location A_Factory 1_Member_0'}})-[:HAS_MEMBER]->(m)
return t, m

Question: Find factories with an average profit margin below a certain threshold:

MATCH (f:Factory)-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
WITH f, avg(u.profit_margin) AS averageProfitMargin
WHERE averageProfitMargin < 30
RETURN f.factory_id AS FactoryID, averageProfitMargin

Question: Compare revenue and profit margin between two factories on a specific date:


MATCH (f1:Factory {{factory_id: 'Factory 1'}})-[:HAS_MACHINE]->(m1:Machine)-[u1:USED_ON]->(d:Date {{date: date('2020-01-01')}}),
      (f2:Factory {{factory_id: 'Factory 2'}})-[:HAS_MACHINE]->(m2:Machine)-[u2:USED_ON]->(d)
RETURN f1.factory_id AS Factory1, avg(u1.revenue) AS Factory1Revenue, avg(u1.profit_margin) AS Factory1ProfitMargin,
       f2.factory_id AS Factory2, avg(u2.revenue) AS Factory2Revenue, avg(u2.profit_margin) AS Factory2ProfitMargin

Question: Analyze the correlation between production volume and revenue:
MATCH (f:Factory)-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
RETURN f.factory_id AS FactoryID, u.production_volume AS ProductionVolume, u.revenue AS Revenue

Question: Identify defect rates for a specific machine:

MATCH (m:Machine {{machine_id: 'Location A-Factory 1-Type 2'}})-[u:USED_ON]->(d:Date)
RETURN m.machine_id AS MachineID, u.defect_rate AS DefectRate, d.date AS Date
ORDER BY d.date

Question: Analyze the relationship between supplier raw material quality and batch quality

MATCH (p:Product)-[pu:PRODUCED_USING]->(rm:RawMaterial)
RETURN rm.raw_material_quality AS RawMaterialQuality, avg(pu.batch_quality) AS AvgBatchQuality
ORDER BY RawMaterialQuality

Question: Analyze the combined impact of machine downtime and defect rate on production volume:

MATCH (m:Machine)-[u:USED_ON]->(d:Date)
WITH m, avg(u.cost_of_downtime) AS AvgDowntime, avg(u.defect_rate) AS AvgDefectRate, avg(u.production_volume) AS AvgProductionVolume
RETURN m.machine_id AS MachineID, AvgDowntime, AvgDefectRate, AvgProductionVolume
ORDER BY AvgProductionVolume DESC

Question: Analyze the impact of machine downtime on revenue (requires linking downtime to revenue loss):

MATCH (m:Machine)-[u:USED_ON]->(d:Date)
WITH m, avg(u.cost_of_downtime) AS AvgDowntimeCost, avg(u.revenue) AS AvgRevenue
RETURN m.machine_id AS MachineID, AvgDowntimeCost, AvgRevenue, (AvgRevenue - AvgDowntimeCost) AS RevenueAfterDowntime
ORDER BY RevenueAfterDowntime DESC

Question: Analyze profit margin trends over time (requires more date data and potentially APOC for time series functions):
This simplified version shows profit margin over time. For more advanced analysis, consider the APOC library:

MATCH (m:Machine)-[u:USED_ON]->(d:Date)
RETURN d.date AS Date, avg(u.profit_margin) AS AvgProfitMargin
ORDER BY Date

Question: Identify factors contributing to low profit margins (combining multiple relationships and properties):

MATCH (f:Factory)-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
WITH f, avg(u.profit_margin) AS AvgProfitMargin, avg(u.machine_utilization) AS AvgUtilization, avg(u.defect_rate) AS AvgDefectRate, avg(u.energy_consumption) AS AvgEnergyConsumption, avg(u.co2_emissions) AS AvgCO2Emissions, avg(u.cost_of_downtime) AS AvgDowntimeCost, avg(u.breakdowns) AS AvgBreakdowns, avg(u.safety_incidents) AS AvgSafetyIncidents
WHERE AvgProfitMargin < 25 // Adjust threshold as needed
RETURN f.factory_id AS FactoryID, AvgProfitMargin, AvgUtilization, AvgDefectRate, AvgEnergyConsumption, AvgCO2Emissions, AvgDowntimeCost, AvgBreakdowns, AvgSafetyIncidents
ORDER BY AvgProfitMargin ASC

Question: List factories and average low profit margins:

MATCH (f:Factory)-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
WITH f, avg(u.profit_margin) AS AvgProfitMargin
WHERE AvgProfitMargin < 20 // Adjust threshold as needed
RETURN f.factory_id AS FactoryID, AvgProfitMargin
ORDER BY AvgProfitMargin ASC

Question: What is the average batch quality for products supplied by each supplier?

MATCH (r:RawMaterial)-[sb:SUPPLIED_BY]->(s:Supplier)
MATCH (p:Product)-[pu:PRODUCED_USING]->(rm:RawMaterial)
WHERE sb.date = pu.date
WITH s, pu.batch_quality AS BatchQuality
RETURN s.supplier_name AS Supplier, avg(BatchQuality) AS AvgBatchQuality

Question: How does the profit margin change over time for Factory 1?

// Use this query to return result date wise: 

MATCH (f:Factory {{factory_id: 'Factory 1'}})-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
WITH d.date AS Date, avg(u.profit_margin) AS AvgProfitMargin
RETURN Date, AvgProfitMargin
ORDER BY Date

// Use this query to return result Monthly: 
MATCH (f:Factory {{factory_id: 'Factory 1'}})-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
WITH d, u,
     toString(d.date) AS DateString,
     substring(toString(d.date), 0, 7) AS YearMonth
WITH YearMonth, avg(u.profit_margin) AS AvgProfitMargin
RETURN YearMonth, AvgProfitMargin
ORDER BY YearMonth

// Use this query to return result Quarterwise: 

MATCH (f:Factory {{factory_id: 'Factory 1'}})-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
WITH d, u, 
     toString(d.date) AS DateString,
     substring(toString(d.date), 0, 4) AS Year,
     toInteger(substring(toString(d.date), 5, 2)) AS Month
WITH Year, ((Month - 1) / 3) + 1 AS Quarter, avg(u.profit_margin) AS AvgProfitMargin
RETURN Year + '-Q' + Quarter AS YearQuarter, AvgProfitMargin
ORDER BY YearQuarter

Question: How does the co2 emissions change over time for machine "Location A-Factory 1-Type 2" in 2023?

MATCH (m:Machine {{machine_id: 'Location A-Factory 1-Type 2'}})-[u:USED_ON]->(d:Date)
WHERE d.date >= date('2023-01-01') AND d.date <= date('2023-12-31')
WITH d, u,
     toString(d.date) AS DateString,
     substring(toString(d.date), 0, 7) AS YearMonth
WITH YearMonth, avg(u.co2_emissions) AS AvgCO2Emissions
RETURN YearMonth, AvgCO2Emissions
ORDER BY YearMonth

Question: what day was the best for overall production?

MATCH (m:Machine)-[u:USED_ON]->(d:Date)
WITH d.date AS Date, sum(u.production_volume) AS TotalProductionVolume
RETURN Date, TotalProductionVolume
ORDER BY TotalProductionVolume DESC
LIMIT 1

Question: Which teams operated machines that experienced defects?

MATCH(m:Machine)-[u:USED_ON]->(d:Date)
with m,u,d
MATCH (m)-[ut:USED_BY_TEAM]->(t:Team)
WHERE u.defect_rate > 0 and d.date = ut.date
RETURN distinct(t.id) as TeamID, m.machine_id as MachineID

Question: How many locations are there?

MATCH (f:Factory)
return DISTINCT(f.location)

Question: What is the average absenteeism rate?

MATCH ()-[u:USED_BY_TEAM]->(t:Team)
return avg(u.average_absentialism)

Question: What is average absenteeism rate for each team?

MATCH (m)-[u:USED_BY_TEAM]->(t:Team)
RETURN t.id AS Team, avg(u.average_absentialism) AS AverageAbsenteeism

Question: What is the average absenteeism rate for location?

MATCH (m)-[u:USED_BY_TEAM]->(t:Team)
RETURN t.location AS Location, avg(u.average_absentialism) AS AverageAbsenteeism

Question: Which year was the most profitable

MATCH (f:Factory)-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
WITH substring(toString(d.date), 0, 4) AS Year, sum(u.revenue) AS TotalRevenue
RETURN Year
ORDER BY TotalRevenue DESC
LIMIT 1

Incorrectly generated Cypher query examples:

Question: List teams that operated on a 23-Jan-2023 and their average operator experience?

Incorrect cypher for above question:

MATCH (t:Team)-[:USED_BY_TEAM]->(m:Machine)-[u:USED_ON]->(d:Date {{date: date('2023-01-23')}})
RETURN t.id AS Team, avg(u.average_operator_experience) AS AverageOperatorExperience

Correct cypher for above question:

MATCH(m:Machine)-[u:USED_ON]->(d:Date{{date: date('2023-01-23')}})
WITH m, u, d
MATCH(m)-[ut:USED_BY_TEAM]->(t:Team)
WHERE d.date = ut.date
Return t.id, avg(ut.average_operator_experience) as AverageOperatorExperience

Question: Analyze each team's contribution to production volume on a 23-Jan-2023

Incorrect cypher for above question:

MATCH (t:Team)-[:USED_BY_TEAM]->(m:Machine)-[u:USED_ON]->(d:Date {{date: date('2023-01-23')}})
RETURN t.id AS Team, sum(u.production_volume) AS TotalProductionVolume

Correct cypher for above question:

MATCH(m:Machine)-[u:USED_ON]->(d:Date{{date: date('2023-01-23')}})
WITH m, u, d
MATCH(m)-[ut:USED_BY_TEAM]->(t:Team)
WHERE d.date = ut.date
Return t.id, u.production_volume as ProductionVolume

Note: 
Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Handle errors or exception while generating cypher query gracefully
If unable to build cypher query then return that i don't understand this type of questions
If question includes any text which doesn't match with any of given knowledge graph node information then return a dummy query which results in no data

The question is:
{question}"""

CYPHER_RECOMMENDATION_PROMPT = PromptTemplate(
    input_variables=['question'], template=CYPHER_RECOMMENDATION_TEMPLATE
)
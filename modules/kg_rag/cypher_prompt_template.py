from langchain.prompts.prompt import PromptTemplate

CYPHER_RECOMMENDATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
////Create Nodes

// Create Factory
CREATE (:Factory {{factory_id: "1", location: "City D"}}) // This should create 50 factories (5 * 10)

// Create Date
CREATE (:Date {{date: date("2023-01-01")}}) 

// Create Machine
CREATE (:Machine {{machine_id: "City A-1-Type A", machine_type: "Type A", machine_age: 7, maintenance_history: "Regular"}})
// We have 3 types in machines, so 3 machines in factories (3 * 50) 150 total machines

//Create Operator
CREATE (:Operator {{operator_id: "City A-1-Operator 1", operator_experience: 8, operator_training_level: "Advanced"}})
// City + Factory + Operator Ids should be unique assuming operators can operate between machines
// operator_experience - Integer
// TEAM Size should be on OPERATED_ON along with absentialism
// training level - beginer - experiece - 3
// training level - intermediate - experiece - 5
// training level - advanced - experiece - 8

//Create Product
CREATE (:Product {{product_category: "Foam Grade A"}})

//Create Supplier
CREATE (:Supplier {{supplier_name: "Supplier A"}})

//RawMaterial
CREATE(:RawMaterial {{raw_material_quality: "Medium"}})

//Create Defect
CREATE (:Defect {{defect_root_cause: "Material Impurity"}})

//// Create Relationships with properties

//OPERATED_ON Relationship
MATCH (f:Factory {{factory_id: " 1"}})
MATCH (d:Date {{date: date("2023-01-01")}})
CREATE (f)-[:OPERATED_ON {{production_volume: 1199, revenue: 9368.437, profit_margin: 34.47, market_demand_index: 86.73, shift: "Day"}}]->(d)
//Add shift to OPERATED_ON

//HAS_MACHINE Relationship
MATCH (f:Factory {{factory_id: "1"}})
MATCH (m:Machine {{machine_id: "City A-1-Type A"}})
CREATE (f)-[:HAS_MACHINE {{team_size: 10, absentialism: 6.1/}}]->(m)

// USED_ON Relationship
MATCH (m:Machine {{machine_id: "City A-1-Type A"}})
MATCH (d:Date {{date: date("2023-01-01")}})
CREATE (m)-[:USED_ON {{machine_utilization: 74.59, machine_downtime: 6.24, cycle_time: 6, energy_consumption: 283.7, co2_emissions: 140.17, emission_limit_compliance: "No", cost_of_downtime: 488.75, breakdowns: 1, safety_incidents: 0, defect_rate: 2, team_size: 10, absentialism: 6.1}}]->(d)

// ON Relationship
MATCH (o:Operator {{operator_id: "City A-1-Operator 1"}})
MATCH (m:Machine {{machine_id: "City A-1-Type A"}})
MATCH (d:Date {{date: date("2023-01-01")}})
CREATE (o)-[:OPERATED]->(m)-[:ON]->(d)

// PRODUCED_ON Relationship
MATCH (p:Product {{product_category: "Foam Grade A"}})
MATCH (d:Date {{date: date("2023-01-01")}})
CREATE (p)-[:PRODUCED_ON {{batch_quality: 88.47}}]->(d)

// SUPPLIED_BY Relationship
MATCH (r:RawMaterial {{raw_material_quality: "Medium"}})
MATCH (sup:Supplier {{supplier_name: "Supplier A"}})
MATCH (d:Date {{date: date("2023-01-01")}})
CREATE (r)-[:SUPPLIED_BY {{supplier_delays: 1}}]->(sup)-[:ON]->(d)

// PRODUCED_USING Relationship
MATCH (p:Product {{product_category: "Foam Grade A"}})
MATCH (r:RawMaterial {{raw_material_quality: "Medium"}})
MATCH (d:Date {{date: date("2023-01-01")}})
CREATE (p)-[:PRODUCED_USING]->(r)-[:ON]->(d)

// EXPERIENCED_DEFECT Relationship
MATCH (m:Machine {{machine_id: "City A-1-Type A"}})
MATCH (def:Defect {{defect_root_cause: "Material Impurity"}})
MATCH (d:Date {{date: date("2023-01-01")}})
CREATE (m)-[:EXPERIENCED_DEFECT]->(def)-[:ON]->(d)

Cypher Examples:
Question: Find factories with an average profit margin below a certain threshold:
 
MATCH (f:Factory)-[o:OPERATED_ON]->(d:Date)
WITH f, avg(o.profit_margin) AS AverageProfitMargin
WHERE AverageProfitMargin < 30 // Example threshold
RETURN f.factory_id AS FactoryID, AverageProfitMargin

Question: Compare revenue and profit margin between two factories on a specific date:

MATCH (f1:Factory {{factory_id: 1}})-[o1:OPERATED_ON]->(d:Date {{date: date("2023-01-01")}})
MATCH (f2:Factory {{factory_id: 2}})-[o2:OPERATED_ON]->(d)
RETURN f1.factory_id AS Factory1, o1.revenue AS Revenue1, o1.profit_margin AS ProfitMargin1,
       f2.factory_id AS Factory2, o2.revenue AS Revenue2, o2.profit_margin AS ProfitMargin2
Complex Queries (Revenue & Profit Margin):

Question: Analyze the correlation between production volume and revenue:

MATCH (f:Factory)-[o:OPERATED_ON]->(d:Date)
RETURN avg(o.production_volume) AS AvgProductionVolume, avg(o.revenue) AS AvgRevenue
ORDER BY AvgProductionVolume DESC
Analyze the impact of market demand index on revenue and profit margin:
Cypher

Question: Identify recurring defects for a specific machine:

MATCH (m:Machine {{machine_id: "City A-1-Type A"}})-[:EXPERIENCED_DEFECT]->(def:Defect)-[:ON]->(d:Date)
RETURN def.defect_root_cause AS DefectRootCause, count(*) AS DefectCount
ORDER BY DefectCount DESC

Question: Analyze the relationship between supplier raw material quality and batch quality:

MATCH (p:Product)-[:SUPPLIED_BY]->(s:Supplier)
MATCH (p)-[po:PRODUCED_ON]->(d:Date)
RETURN s.raw_material_quality AS RawMaterialQuality, avg(po.batch_quality) AS AvgBatchQuality
ORDER BY RawMaterialQuality

Question: Analyze the combined impact of machine downtime and defect rate on production volume:

MATCH (f:Factory)-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
MATCH (f)-[o:OPERATED_ON]->(d)
RETURN avg(u.machine_downtime) AS AvgDowntime, avg(u.defect_rate) as AvgDefectRate, sum(o.production_volume) AS TotalProductionVolume
ORDER BY AvgDowntime DESC, AvgDefectRate DESC

Question: Analyze the impact of machine downtime on revenue (requires linking downtime to revenue loss):
This query assumes you can calculate the cost of downtime per day. If not you need to create such a property

MATCH (f:Factory)-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d:Date)
MATCH (f)-[o:OPERATED_ON]->(d)
RETURN avg(u.machine_downtime) AS AvgDowntime, sum(o.revenue - u.cost_of_downtime) AS AdjustedRevenue
ORDER BY AvgDowntime DESC

Question: Analyze profit margin trends over time (requires more date data and potentially APOC for time series functions):
This simplified version shows profit margin over time. For more advanced analysis, consider the APOC library:

MATCH (f:Factory)-[o:OPERATED_ON]->(d:Date)
RETURN d.date AS Date, avg(o.profit_margin) AS AvgProfitMargin
ORDER BY d.date

Question: Identify factors contributing to low profit margins (combining multiple relationships and properties):

MATCH (f:Factory)-[o:OPERATED_ON]->(d:Date)
WHERE o.profit_margin < 25 // Example threshold for low profit margin
MATCH (f)-[:HAS_MACHINE]->(m:Machine)-[u:USED_ON]->(d)
MATCH (p:Product)-[:PRODUCED_ON]->(d)
RETURN f.factory_id AS Factory, d.date as Date, o.profit_margin as ProfitMargin, avg(u.machine_downtime) as Downtime, p.product_category as ProductCategory, o.market_demand_index as MarketDemand
ORDER BY ProfitMargin

Question: List factories and average low profit margins:

MATCH (f:Factory)-[o:OPERATED_ON]->(d:Date)
WHERE o.profit_margin < 25
WITH f, avg(o.profit_margin) AS AverageProfitMargin
RETURN f.factory_id AS FactoryID, , f.location as City, AverageProfitMargin
'''

Question: What is the average batch quality for products supplied by each supplier?

MATCH (s:Supplier)<-[:SUPPLIED_BY]-(r:RawMaterial)<-[:PRODUCED_USING]-(p:Product)
WITH s, p
MATCH (p)-[po:PRODUCED_ON]->(d:Date)
RETURN s.supplier_name AS SupplierName, avg(po.batch_quality) AS AvgBatchQuality
ORDER BY s.supplier_name

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""

CYPHER_RECOMMENDATION_PROMPT = PromptTemplate(
    input_variables=['question'], template=CYPHER_RECOMMENDATION_TEMPLATE
)
// Create Factory
CREATE (:Factory {factory_id: "Factory 1", location: "City D"})

// Create Date
CREATE (:Date {date: date("2023-01-01")})

// Create Machine
CREATE (:Machine {machine_id: "Factory 1-Type A", machine_type: "Type A", machine_age: 7, maintenance_history: "Regular"})

//Create Shift
CREATE (:Shift {shift: "Night"})

//Create Operator
CREATE (:Operator {operator_id: "Operator1", operator_experience: 8.49, operator_training_level: "Intermediate"})

//Create Product
CREATE (:Product {product_category: "Foam Grade A"})

//Create Supplier
CREATE (:Supplier {supplier_name: "Supplier A"})

//Create Defect
CREATE (:Defect {defect_root_cause: "Material Impurity"})

// Create Relationships with properties
MATCH (f:Factory {factory_id: "Factory 1"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (f)-[:OPERATED_ON {production_volume: 1199, revenue: 9368.437, profit_margin: 34.47, market_demand_index: 86.73}]->(d)

MATCH (f:Factory {factory_id: "Factory 1"})
MATCH (m:Machine {machine_id: "Factory 1-Type A"})
CREATE (f)-[:HAS_MACHINE {team_size: 10}]->(m)

MATCH (m:Machine {machine_id: "Factory 1-Type A"})
MATCH (d:Date {date: date("2023-01-01")})
MATCH (s:Shift {shift: "Night"})
CREATE (m)-[:USED_ON {machine_utilization: 74.59, machine_downtime: 6.24, cycle_time: 6, energy_consumption: 283.7, co2_emissions: 140.17, emission_limit_compliance: "No", cost_of_downtime: 488.75, breakdowns: 1, safety_incidents: 0, defect_rate: 2}]->(d)
CREATE (m)-[:OPERATED_DURING]->(s)

MATCH (o:Operator {operator_id: "Operator1"})
MATCH (m:Machine {machine_id: "Factory 1-Type A"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (o)-[:OPERATED]->(m)-[:ON]->(d)

MATCH (p:Product {product_category: "Foam Grade A"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (p)-[:PRODUCED_ON {batch_quality: 88.47}]->(d)

MATCH (p:Product {product_category: "Foam Grade A"})
MATCH (sup:Supplier {supplier_name: "Supplier A"})
CREATE (p)-[:SUPPLIED_BY {supplier_delays: 1, raw_material_quality: "Medium"}]->(sup)

MATCH (m:Machine {machine_id: "Factory 1-Type A"})
MATCH (def:Defect {defect_root_cause: "Material Impurity"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (m)-[:EXPERIENCED_DEFECT]->(def)-[:ON]->(d)

// Sample Data Creation (Expanding on previous example for multiple dates and factories)

// Factory 2 Data
CREATE (:Factory {factory_id: "Factory 2", location: "City E"})
CREATE (:Machine {machine_id: "Factory 2-Type B", machine_type: "Type B", machine_age: 5, maintenance_history: "Preventative"})
CREATE (:Date {date: date("2023-01-15")})
MATCH (f:Factory {factory_id: "Factory 2"})
MATCH (m:Machine {machine_id: "Factory 2-Type B"})
CREATE (f)-[:HAS_MACHINE {team_size: 8}]->(m)
MATCH (m:Machine {machine_id: "Factory 2-Type B"})
MATCH (d:Date {date: date("2023-01-15")})
CREATE (m)-[:USED_ON {machine_utilization: 85.2, machine_downtime: 2.5, cycle_time: 7, energy_consumption: 350, co2_emissions: 170, emission_limit_compliance: "Yes", cost_of_downtime: 250, breakdowns: 0, safety_incidents: 0, defect_rate: 0.5}]->(d)
MATCH (f:Factory {factory_id: "Factory 2"})
MATCH (d:Date {date: date("2023-01-15")})
CREATE (f)-[:OPERATED_ON {production_volume: 1500, revenue: 12000, profit_margin: 30, market_demand_index: 90}]->(d)

// Additional data for Factory 1 in February
CREATE (:Date {date: date("2023-02-05")})
MATCH (f:Factory {factory_id: "Factory 1"})
MATCH (m:Machine {machine_id: "Factory 1-Type A"})
MATCH (d:Date {date: date("2023-02-05")})
CREATE (m)-[:USED_ON {machine_utilization: 78, machine_downtime: 5, cycle_time: 6.5, energy_consumption: 290, co2_emissions: 145, emission_limit_compliance: "No", cost_of_downtime: 450, breakdowns: 2, safety_incidents: 1, defect_rate: 3}]->(d)
MATCH (f:Factory {factory_id: "Factory 1"})
MATCH (d:Date {date: date("2023-02-05")})
CREATE (f)-[:OPERATED_ON {production_volume: 1300, revenue: 10000, profit_margin: 32, market_demand_index: 88}]->(d)

//Query 1: Find total production volume for a factory in a given month.
MATCH (f:Factory {factory_id: "Factory 1"})-[:OPERATED_ON]->(d:Date)
WHERE d.date >= date("2023-01-01") AND d.date < date("2023-02-01")
RETURN sum(f-[r:OPERATED_ON]->d | r.production_volume) AS TotalProductionVolumeJan

//Query 2: Find average machine utilization for a specific machine type.
MATCH (m:Machine {machine_type: "Type A"})-[:USED_ON]->(d:Date)
RETURN avg(m-[r:USED_ON]->d | r.machine_utilization) AS AverageUtilizationTypeA

//Query 3: Analyze the relationship between downtime and breakdowns (Correlation).
MATCH (m:Machine)-[:USED_ON]->(d:Date)
RETURN collect(m-[r:USED_ON]->d | r.machine_downtime) AS Downtimes,
       collect(m-[r:USED_ON]->d | r.breakdowns) AS Breakdowns

//More advanced correlation (requires APOC library):
//CALL apoc.coll.pearson(Downtimes, Breakdowns) YIELD value as correlation
//RETURN correlation

//Query 4: Identify trends in defect rates over time.
MATCH (m:Machine)-[:USED_ON]->(d:Date)
RETURN d.date AS Date, avg(m-[r:USED_ON]->d | r.defect_rate) AS AverageDefectRate
ORDER BY d.date

//Query 5: Find the impact of supplier delays on production.
MATCH (p:Product)-[:SUPPLIED_BY {supplier_delays: supplierDelay}]->(s:Supplier)
MATCH (p)-[:PRODUCED_ON]->(d:Date)<-[:OPERATED_ON]-(f:Factory)
RETURN supplierDelay, avg(f-[r:OPERATED_ON]->d | r.production_volume) AS AvgProductionVolume
ORDER BY supplierDelay

// Example with a specific delay:
MATCH (p:Product)-[:SUPPLIED_BY {supplier_delays: 1}]->(s:Supplier)
MATCH (p)-[:PRODUCED_ON]->(d:Date)<-[:OPERATED_ON]-(f:Factory)
RETURN avg(f-[r:OPERATED_ON]->d | r.production_volume) AS AvgProductionVolumeWith1DayDelay


// Creating all possible nodes and relationships (consolidated and improved)
// This cypher statement creates all nodes and relationships from your initial data structure.

// Create Factory and Date
UNWIND [{factory: "Factory 1", location: "City D", date: date("2023-01-01"), machine_type: "Type A", machine_age: 7, maintenance_history: "Regular", shift: "Night", operator_experience: 8.49, operator_training_level: "Intermediate", product_category: "Foam Grade A", supplier_name: "Supplier A", defect_root_cause: "Material Impurity", machine_utilization: 74.59, machine_downtime: 6.24, cycle_time: 6, energy_consumption: 283.7, co2_emissions: 140.17, emission_limit_compliance: "No", cost_of_downtime: 488.75, breakdowns: 1, safety_incidents: 0, defect_rate: 2, batch_quality: 88.47, supplier_delays: 1, raw_material_quality: "Medium", production_volume: 1199, revenue: 9368.437, profit_margin: 34.47, market_demand_index: 86.73, team_size: 10},
        {factory: "Factory 2", location: "City E", date: date("2023-01-15"), machine_type: "Type B", machine_age: 5, maintenance_history: "Preventative", shift: "Day", operator_experience: 7, operator_training_level: "Advanced", product_category: "Foam Grade B", supplier_name: "Supplier B", defect_root_cause: "Operator Error", machine_utilization: 85.2, machine_downtime: 2.5, cycle_time: 7, energy_consumption: 350, co2_emissions: 170, emission_limit_compliance: "Yes", cost_of_downtime: 250, breakdowns: 0, safety_incidents: 0, defect_rate: 0.5, batch_quality: 92, supplier_delays: 0, raw_material_quality: "High", production_volume: 1500, revenue: 12000, profit_margin: 30, market_demand_index: 90, team_size: 8},
        {factory: "Factory 1", location: "City D", date: date("2023-02-05"), machine_type: "Type A", machine_age: 7, maintenance_history: "Regular", shift: "Night", operator_experience: 8.7, operator_training_level: "Intermediate", product_category: "Foam Grade A", supplier_name: "Supplier A", defect_root_cause: "Material Impurity", machine_utilization: 78, machine_downtime: 5, cycle_time: 6.5, energy_consumption: 290, co2_emissions: 145, emission_limit_compliance: "No", cost_of_downtime: 450, breakdowns: 2, safety_incidents: 1, defect_rate: 3, batch_quality: 85, supplier_delays: 2, raw_

// Create Factory
CREATE (:Factory {factory_id: "1", location: "City D"}) // This should create 50 factories (5 * 10)

// Create Date
CREATE (:Date {date: date("2023-01-01")}) 

// Create Machine
CREATE (:Machine {machine_id: "City A-1-Type A", machine_type: "Type A", machine_age: 7, maintenance_history: "Regular"})
// We have 3 types in machines, so 3 machines in factories (3 * 50) 150 total machines

//Create Operator
CREATE (:Operator {operator_id: "City A-1-Operator 1", operator_experience: 8, operator_training_level: "Advanced"})
// City + Factory + Operator Ids should be unique assuming operators can operate between machines
// operator_experience - Integer
// TEAM Size should be on OPERATED_ON along with absentialism
// training level - beginer - experiece - 3
// training level - intermediate - experiece - 5
// training level - advanced - experiece - 8

//Create Product
CREATE (:Product {product_category: "Foam Grade A"})

//Create Supplier
CREATE (:Supplier {supplier_name: "Supplier A"})

//Create Defect
CREATE (:Defect {defect_root_cause: "Material Impurity"})

// Create Relationships with properties
MATCH (f:Factory {factory_id: " 1"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (f)-[:OPERATED_ON {production_volume: 1199, revenue: 9368.437, profit_margin: 34.47, market_demand_index: 86.73, shift: "Day"}]->(d)
//Add shift to OPERATED_ON

MATCH (f:Factory {factory_id: "1"})
MATCH (m:Machine {machine_id: "City A-1-Type A"})
CREATE (f)-[:HAS_MACHINE {team_size: 10, absentialism: 6.1}]->(m)
// add asbentialism to HAS_MACHINE

MATCH (m:Machine {machine_id: "City A-1-Type A"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (m)-[:USED_ON {machine_utilization: 74.59, machine_downtime: 6.24, cycle_time: 6, energy_consumption: 283.7, co2_emissions: 140.17, emission_limit_compliance: "No", cost_of_downtime: 488.75, breakdowns: 1, safety_incidents: 0, defect_rate: 2, team_size: 10, absentialism: 6.1}]->(d)
// Add team_size, absentialism to USED_ON


MATCH (o:Operator {operator_id: "City A-1-Operator 1"})
MATCH (m:Machine {machine_id: "City A-1-Type A"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (o)-[:OPERATED]->(m)-[:ON]->(d)

MATCH (p:Product {product_category: "Foam Grade A"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (p)-[:PRODUCED_ON {batch_quality: 88.47}]->(d)

MATCH (p:Product {product_category: "Foam Grade A"})
MATCH (sup:Supplier {supplier_name: "Supplier A"})
CREATE (p)-[:SUPPLIED_BY {supplier_delays: 1, raw_material_quality: "Medium"}]->(sup)

MATCH (m:Machine {machine_id: "City A-1-Type A"})
MATCH (def:Defect {defect_root_cause: "Material Impurity"})
MATCH (d:Date {date: date("2023-01-01")})
CREATE (m)-[:EXPERIENCED_DEFECT]->(def)-[:ON]->(d)

// Sample Data Creation (Expanding on previous example for multiple dates and factories)

// Factory 2 Data
// Create Factory
CREATE (:Factory {factory_id: "1", location: "City E"}) // This should create 50 factories (5 * 10)

// Create Date
CREATE (:Date {date: date("2023-01-15")}) 

// Create Machine
CREATE (:Machine {machine_id: "City E-1-Type B", machine_type: "Type B", machine_age: 7, maintenance_history: "Irregular"})
// We have 3 types in machines, so 3 machines in factories (3 * 50) 150 total machines

//Create Operator
CREATE (:Operator {operator_id: "City E-1-Operator 1", operator_experience: 5, operator_training_level: "Intermediate"})
// City + Factory + Operator Ids should be unique assuming operators can operate between machines
// operator_experience - Integer
// TEAM Size should be on OPERATED_ON along with absentialism
// training level - beginer - experiece - 3
// training level - intermediate - experiece - 5
// training level - advanced - experiece - 8

//Create Product
CREATE (:Product {product_category: "Foam Grade B"})

//Create Supplier
CREATE (:Supplier {supplier_name: "	Supplier B"})

//Create Defect
CREATE (:Defect {defect_root_cause: "Assembly Errors"})

// Create Relationships with properties
MATCH (f:Factory {factory_id: " 1"})
MATCH (d:Date {date: date("2023-01-15")})
CREATE (f)-[:OPERATED_ON {production_volume: 1500, revenue: 12000, profit_margin: 30, market_demand_index: 90, shift: "Day"}]->(d)

//Add shift to OPERATED_ON

MATCH (f:Factory {factory_id: "1"})
MATCH (m:Machine {machine_id: "City E-1-Type B"})
CREATE (f)-[:HAS_MACHINE {team_size: 8}]->(m)
// add asbentialism to HAS_MACHINE

MATCH (m:Machine {machine_id: "City E-1-Type B"})
MATCH (d:Date {date: date("2023-01-15")})
CREATE (m)-[:USED_ON {machine_utilization: 85.2, machine_downtime: 2.5, cycle_time: 7, energy_consumption: 350, co2_emissions: 170, emission_limit_compliance: "Yes", cost_of_downtime: 250, breakdowns: 0, safety_incidents: 0, defect_rate: 0.5, team_size: 8, absentialism: 3.1}]->(d)
// Add team_size, absentialism to USED_ON


MATCH (o:Operator {operator_id: "City E-1-Operator 1"})
MATCH (m:Machine {machine_id: "City E-1-Type B"})
MATCH (d:Date {date: date("2023-01-15")})
CREATE (o)-[:OPERATED]->(m)-[:ON]->(d)

MATCH (p:Product {product_category: "Foam Grade B"})
MATCH (d:Date {date: date("2023-01-15")})
CREATE (p)-[:PRODUCED_ON {batch_quality: 90.47}]->(d)

MATCH (p:Product {product_category: "Foam Grade B"})
MATCH (sup:Supplier {supplier_name: "Supplier B"})
CREATE (p)-[:SUPPLIED_BY {supplier_delays: 2, raw_material_quality: "High"}]->(sup)

MATCH (m:Machine {machine_id: "City E-1-Type B"})
MATCH (def:Defect {defect_root_cause: "Assembly Errors"})
MATCH (d:Date {date: date("2023-01-15")})
CREATE (m)-[:EXPERIENCED_DEFECT]->(def)-[:ON]->(d)

// Additional data for Factory 1 in February
// Create Factory
CREATE (:Factory {factory_id: "1", location: "City B"}) // This should create 50 factories (5 * 10)

// Create Date
CREATE (:Date {date: date("2023-02-05")}) 

// Create Machine
CREATE (:Machine {machine_id: "City B-1-Type C", machine_type: "Type C", machine_age: 7, maintenance_history: "Irregular"})
// We have 3 types in machines, so 3 machines in factories (3 * 50) 150 total machines

//Create Operator
CREATE (:Operator {operator_id: "City B-1-Operator 1", operator_experience: 3, operator_training_level: "Beginer"})
// City + Factory + Operator Ids should be unique assuming operators can operate between machines
// operator_experience - Integer
// TEAM Size should be on OPERATED_ON along with absentialism
// training level - beginer - experiece - 3
// training level - intermediate - experiece - 5
// training level - advanced - experiece - 8

//Create Product
CREATE (:Product {product_category: "Custom Size"})

//Create Supplier
CREATE (:Supplier {supplier_name: "	Supplier C"})

//Create Defect
CREATE (:Defect {defect_root_cause: "Surface Defects"})

// Create Relationships with properties
MATCH (f:Factory {factory_id: " 1"})
MATCH (d:Date {date: date("2023-02-05")})
CREATE (f)-[:OPERATED_ON {production_volume: 1300, revenue: 10000, profit_margin: 32, market_demand_index: 88, shift: "Night"}]->(d)

//Add shift to OPERATED_ON

MATCH (f:Factory {factory_id: "1"})
MATCH (m:Machine {machine_id: "City B-1-Type C"})
CREATE (f)-[:HAS_MACHINE {team_size: 12}]->(m)
// add asbentialism to HAS_MACHINE

MATCH (m:Machine {machine_id: "City B-1-Type C"})
MATCH (d:Date {date: date("2023-02-05")})
CREATE (m)-[:USED_ON {machine_utilization: 78, machine_downtime: 5, cycle_time: 6.5, energy_consumption: 290, co2_emissions: 145, emission_limit_compliance: "No", cost_of_downtime: 450, breakdowns: 2, safety_incidents: 1, defect_rate: 3, team_size: 12, absentialism: 6}]->(d)
// Add team_size, absentialism to USED_ON


MATCH (o:Operator {operator_id: "City B-1-Operator 1"})
MATCH (m:Machine {machine_id: "City B-1-Type C"})
MATCH (d:Date {date: date("2023-02-05")})
CREATE (o)-[:OPERATED]->(m)-[:ON]->(d)

MATCH (p:Product {product_category: "Custom Size"})
MATCH (d:Date {date: date("2023-02-05")})
CREATE (p)-[:PRODUCED_ON {batch_quality: 85.47}]->(d)

MATCH (p:Product {product_category: "Custom Size"})
MATCH (sup:Supplier {supplier_name: "Supplier C"})
CREATE (p)-[:SUPPLIED_BY {supplier_delays: 2, raw_material_quality: "High"}]->(sup)

MATCH (m:Machine {machine_id: "City B-1-Type C"})
MATCH (def:Defect {defect_root_cause: "Surface Defects"})
MATCH (d:Date {date: date("2023-02-05")})
CREATE (m)-[:EXPERIENCED_DEFECT]->(def)-[:ON]->(d)


//Query 1: Find total production volume for a factory in a given month.
MATCH (f:Factory {factory_id: 1, location: "City A"})-[r:OPERATED_ON]->(d:Date)
WHERE d.date >= date("2023-01-01") AND d.date < date("2023-02-01")
RETURN sum(r.production_volume) AS TotalProductionVolumeJan

//Query 2: Find average machine utilization for a specific machine type.
MATCH (m:Machine {machine_type: "Type A"})-[r:USED_ON]->(d:Date)
RETURN avg(r.machine_utilization) AS AverageUtilizationTypeA

//Query 3: Analyze the relationship between downtime and breakdowns (Correlation).
MATCH (m:Machine)-[r:USED_ON]->(d:Date)
RETURN collect(r.machine_downtime) AS Downtimes, collect(r.breakdowns) AS Breakdowns

//More advanced correlation (requires APOC library):
//CALL apoc.coll.pearson(Downtimes, Breakdowns) YIELD value as correlation
//RETURN correlation

//Query 4: Identify trends in defect rates over time.
MATCH (m:Machine)-[r:USED_ON]->(d:Date)
RETURN d.date AS Date, avg(r.defect_rate) AS AverageDefectRate
ORDER BY d.date

//Query 5: Find the impact of supplier delays on production.
MATCH (p:Product)-[sup_rel:SUPPLIED_BY]->(s:Supplier)
MATCH (p)-[:PRODUCED_ON]->(d:Date)<-[operated_rel:OPERATED_ON]-(f:Factory)
RETURN sup_rel.supplier_delays AS supplierDelay, avg(operated_rel.production_volume) AS AvgProductionVolume
ORDER BY supplierDelay

// Example with a specific delay:
MATCH (p:Product)-[:SUPPLIED_BY {supplier_delays: 1}]->(s:Supplier)
MATCH (p)-[:PRODUCED_ON]->(d:Date)<-[operated_rel:OPERATED_ON]-(f:Factory)
RETURN avg(operated_rel.production_volume) AS AvgProductionVolumeWith1DayDelay


// Creating all possible nodes and relationships (consolidated and improved)
// This cypher statement creates all nodes and relationships from your initial data structure.

// Create Factory and Date
UNWIND [{factory: "Factory 1", location: "City D", date: date("2023-01-01"), machine_type: "Type A", machine_age: 7, maintenance_history: "Regular", shift: "Night", operator_experience: 8.49, operator_training_level: "Intermediate", product_category: "Foam Grade A", supplier_name: "Supplier A", defect_root_cause: "Material Impurity", machine_utilization: 74.59, machine_downtime: 6.24, cycle_time: 6, energy_consumption: 283.7, co2_emissions: 140.17, emission_limit_compliance: "No", cost_of_downtime: 488.75, breakdowns: 1, safety_incidents: 0, defect_rate: 2, batch_quality: 88.47, supplier_delays: 1, raw_material_quality: "Medium", production_volume: 1199, revenue: 9368.437, profit_margin: 34.47, market_demand_index: 86.73, team_size: 10},
        {factory: "Factory 2", location: "City E", date: date("2023-01-15"), machine_type: "Type B", machine_age: 5, maintenance_history: "Preventative", shift: "Day", operator_experience: 7, operator_training_level: "Advanced", product_category: "Foam Grade B", supplier_name: "Supplier B", defect_root_cause: "Operator Error", machine_utilization: 85.2, machine_downtime: 2.5, cycle_time: 7, energy_consumption: 350, co2_emissions: 170, emission_limit_compliance: "Yes", cost_of_downtime: 250, breakdowns: 0, safety_incidents: 0, defect_rate: 0.5, batch_quality: 92, supplier_delays: 0, raw_material_quality: "High", production_volume: 1500, revenue: 12000, profit_margin: 30, market_demand_index: 90, team_size: 8},
        {factory: "Factory 1", location: "City D", date: date("2023-02-05"), machine_type: "Type A", machine_age: 7, maintenance_history: "Regular", shift: "Night", operator_experience: 8.7, operator_training_level: "Intermediate", product_category: "Foam Grade A", supplier_name: "Supplier A", defect_root_cause: "Material Impurity", machine_utilization: 78, machine_downtime: 5, cycle_time: 6.5, energy_consumption: 290, co2_emissions: 145, emission_limit_compliance: "No", cost_of_downtime: 450, breakdowns: 2, safety_incidents: 1, defect_rate: 3, batch_quality: 85, supplier_delays: 2, raw_
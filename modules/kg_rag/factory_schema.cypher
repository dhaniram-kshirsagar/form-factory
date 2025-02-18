//// Factory Operations Schema

// Create Factories
CREATE (f:Factory {name: 'Factory 1', location: 'Location A'});

// Create Machines
CREATE (m:Machine {type: 'Type 1', age: 6.34, utilization: 59, downtime: 0.0});

// Create Batches
CREATE (b:Batch {batch_id: 'Batch 1', date: '2020-01-01', quality: 89.74, defect_rate: 7.08, production_volume: 629.39, cycle_time: 20, temperature: 65.0, pressure: 150.0, chemical_ratio: 3.0, mixing_speed: 200.0, safety_incidents: 3.76});

// Create Shifts
CREATE (s:Shift {shift_id: 'Shift 1', team_size: 4});

// Create Operators
CREATE (o:Operator {name: 'Member_0_0', experience: 10.0, training_level: 3.6});

// Create Suppliers
CREATE (s:Supplier {name: 'Supplier X', delays: 0, material_quality: 0});

// Create Products
CREATE (p:Product {category: 'Category B', market_demand: 50});

// Create Metrics
CREATE (mt:Metrics {energy_consumption: 877, co2_emissions: 867, waste_generated: 300, cost_of_downtime: 0.0, revenue: 377589.2, profit_margin: 12.63});

//// Relationships

// Factory operates in a location
MATCH (f:Factory {name: 'Factory 1'}), (l:Location {name: 'Location A'})
CREATE (f)-[:OPERATES_IN]->(l);

// Factory uses a machine
MATCH (f:Factory {name: 'Factory 1'}), (m:Machine {type: 'Type 1'})
CREATE (f)-[:USES]->(m);

// Machine produces a batch
MATCH (m:Machine {type: 'Type 1'}), (b:Batch {batch_id: 'Batch 1'})
CREATE (m)-[:PRODUCES]->(b);

// Batch has a shift
MATCH (b:Batch {batch_id: 'Batch 1'}), (s:Shift {shift_id: 'Shift 1'})
CREATE (b)-[:HAS_SHIFT]->(s);

// Shift has an operator
MATCH (s:Shift {shift_id: 'Shift 1'}), (o:Operator {name: 'Member_0_0'})
CREATE (s)-[:HAS_OPERATOR]->(o);

// Supplier supplies to a factory
MATCH (s:Supplier {name: 'Supplier X'}), (f:Factory {name: 'Factory 1'})
CREATE (s)-[:SUPPLIES]->(f);

// Batch belongs to a product
MATCH (b:Batch {batch_id: 'Batch 1'}), (p:Product {category: 'Category B'})
CREATE (b)-[:BELONGS_TO]->(p);

// Batch has metrics
MATCH (b:Batch {batch_id: 'Batch 1'}), (mt:Metrics {energy_consumption: 877})
CREATE (b)-[:HAS_METRICS]->(mt);

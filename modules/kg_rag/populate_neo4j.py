from neo4j import GraphDatabase
import pandas as pd

# Neo4j connection details
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "neo4j")  # Replace with your Neo4j credentials

# Initialize the Neo4j driver
driver = GraphDatabase.driver(URI, auth=AUTH)

# Function to create nodes and relationships
def create_nodes_and_relationships(tx, row):
    # Create Factory node
    tx.run("""
        MERGE (f:Factory {name: $factory, location: $location})
    """, factory=row["Factory"], location=row["Location"])

    # Create Machine node
    tx.run("""
        MERGE (m:Machine {type: $type, age: $age, utilization: $utilization, downtime: $downtime})
    """, type=row["Machine Type"], age=row["Machine Age (years)"], 
        utilization=row["Machine Utilization (%)"], downtime=row["Machine Downtime (hours)"])

    # Create Batch node
    tx.run("""
        MERGE (b:Batch {batch_id: $batch_id, date: $date, quality: $quality, defect_rate: $defect_rate, 
            production_volume: $production_volume, cycle_time: $cycle_time, temperature: $temperature, 
            pressure: $pressure, chemical_ratio: $chemical_ratio, mixing_speed: $mixing_speed, 
            safety_incidents: $safety_incidents})
    """, batch_id=row["Batch"], date=row["Date"], quality=row["Batch Quality (Pass %)"], 
        defect_rate=row["Defect Rate (%)"], production_volume=row["Production Volume (units)"], 
        cycle_time=row["Cycle Time (minutes)"], temperature=row["Temperature (C)"], 
        pressure=row["Pressure (psi)"], chemical_ratio=row["Chemical Ratio"], 
        mixing_speed=row["Mixing Speed (RPM)"], safety_incidents=row["Safety Incidents (count)"])

    # Create Shift node
    tx.run("""
        MERGE (s:Shift {shift_id: $shift_id, team_size: $team_size})
    """, shift_id=row["Shift"], team_size=row["Team Size"])

    # Create Operator node
    for member in eval(row["Team Members"]):
        tx.run("""
            MERGE (o:Operator {name: $name, experience: $experience, training_level: $training_level})
        """, name=member["Name"], experience=member["Operator Experience (years)"], 
            training_level=member["Operator Training Level"])

    # Create Supplier node
    tx.run("""
        MERGE (s:Supplier {name: $name, delays: $delays, material_quality: $material_quality})
    """, name=row["Supplier"], delays=row["Supplier Delays (days)"], 
        material_quality=row["Raw Material Quality"])

    # Create Product node
    tx.run("""
        MERGE (p:Product {category: $category, market_demand: $market_demand})
    """, category=row["Product Category"], market_demand=row["Market Demand Index"])

    # Create Metrics node
    tx.run("""
        MERGE (mt:Metrics {energy_consumption: $energy_consumption, co2_emissions: $co2_emissions, 
            waste_generated: $waste_generated, cost_of_downtime: $cost_of_downtime, 
            revenue: $revenue, profit_margin: $profit_margin})
    """, energy_consumption=row["Energy Consumption (kWh)"], 
        co2_emissions=row["CO2 Emissions (kg)"], waste_generated=row["Waste Generated (kg)"], 
        cost_of_downtime=row["Cost of Downtime ($)"], revenue=row["Revenue ($)"], 
        profit_margin=row["Profit Margin (%)"])

    # Create relationships
    tx.run("""
        MATCH (f:Factory {name: $factory}), (m:Machine {type: $type})
        MERGE (f)-[:USES]->(m)
    """, factory=row["Factory"], type=row["Machine Type"])

    tx.run("""
        MATCH (m:Machine {type: $type}), (b:Batch {batch_id: $batch_id})
        MERGE (m)-[:PRODUCES]->(b)
    """, type=row["Machine Type"], batch_id=row["Batch"])

    tx.run("""
        MATCH (b:Batch {batch_id: $batch_id}), (s:Shift {shift_id: $shift_id})
        MERGE (b)-[:HAS_SHIFT]->(s)
    """, batch_id=row["Batch"], shift_id=row["Shift"])

    for member in eval(row["Team Members"]):
        tx.run("""
            MATCH (s:Shift {shift_id: $shift_id}), (o:Operator {name: $name})
            MERGE (s)-[:HAS_OPERATOR]->(o)
        """, shift_id=row["Shift"], name=member["Name"])

    tx.run("""
        MATCH (s:Supplier {name: $name}), (f:Factory {name: $factory})
        MERGE (s)-[:SUPPLIES]->(f)
    """, name=row["Supplier"], factory=row["Factory"])

    tx.run("""
        MATCH (b:Batch {batch_id: $batch_id}), (p:Product {category: $category})
        MERGE (b)-[:BELONGS_TO]->(p)
    """, batch_id=row["Batch"], category=row["Product Category"])

    tx.run("""
        MATCH (b:Batch {batch_id: $batch_id}), (mt:Metrics {energy_consumption: $energy_consumption})
        MERGE (b)-[:HAS_METRICS]->(mt)
    """, batch_id=row["Batch"], energy_consumption=row["Energy Consumption (kWh)"])

# Read the CSV file
csv_path = "/Users/dhani/foamvenv/smart-data-intelligence/apps/foam_factory/modules/data/large-data/FoamFactory_V2_27K.csv"
df = pd.read_csv(csv_path)

# Process each row in the CSV
with driver.session() as session:
    for _, row in df.iterrows():
        session.write_transaction(create_nodes_and_relationships, row)

# Close the driver
driver.close()
# Problem Definition: Production Volume Prediction

## Objective
The goal is to build a machine learning model to predict the **Production Volume (units)** for foam factories using the data provided in `FoamFactory_V2_27K.csv`.

## Dataset
The dataset contains the following columns:
- `Factory`: Factory identifier.
- `Date`: Timestamp of the recorded data.
- `Location`: Location of the factory.
- `Machine Type`: Type of machine used.
- `Machine Utilization (%)`: Percentage of machine usage.
- `Machine Downtime (hours)`: Time the machine was inactive.
- `Maintenance History`: Maintenance status of the machine.
- `Machine Age (years)`: Age of the machine.
- `Batch`: Batch identifier.
- `Batch Quality (Pass %)`: Percentage of products passing quality checks.
- `Cycle Time (minutes)`: Time taken to complete a production cycle.
- `Energy Consumption (kWh)`: Energy used by the machine.
- `Energy Efficiency Rating`: Efficiency rating of the machine.
- `CO2 Emissions (kg)`: Carbon dioxide emissions.
- `Emission Limit Compliance`: Compliance status with emission limits.
- `Waste Generated (kg)`: Amount of waste produced.
- `Water Usage (liters)`: Water consumed.
- `Shift`: Shift identifier.
- `Operator Experience (years)`: Experience level of operators.
- `Team Size`: Number of team members.
- `Team Members`: Detailed list of team members with their experience, training level, and absenteeism rate.
- `Absenteeism Rate (%)`: Percentage of absenteeism in the team.
- `Product Category`: Category of the product.
- `Supplier`: Supplier identifier.
- `Supplier Delays (days)`: Delays caused by the supplier.
- `Raw Material Quality`: Quality of raw materials.
- `Market Demand Index`: Index representing market demand.
- `Cost of Downtime ($)`: Financial impact of machine downtime.
- `Revenue ($)`: Revenue generated.
- `Profit Margin (%)`: Profit margin percentage.
- `Breakdowns (count)`: Number of machine breakdowns.
- `Safety Incidents (count)`: Number of safety incidents.
- `Production Volume (units)`: Total units produced (target variable).
- `Defect Rate (%)`: Percentage of defective products.
- `Temperature (C)`: Operating temperature.
- `Pressure (psi)`: Operating pressure.
- `Chemical Ratio`: Ratio of chemicals used.
- `Mixing Speed (RPM)`: Speed of mixing.

## Approach
1. **Data Preprocessing**:
   - Handle missing values.
   - Encode categorical variables (e.g., `Factory`, `Location`, `Machine Type`, `Maintenance History`, `Product Category`, `Supplier`).
   - Scale numeric features.

2. **Feature Selection**:
   - Identify relevant features that influence production volume.

3. **Model Training**:
   - Train a regression model (e.g., Linear Regression, Random Forest, Gradient Boosting) to predict production volume.

4. **Model Evaluation**:
   - Evaluate the model using metrics such as Mean Squared Error (MSE) and R² score.

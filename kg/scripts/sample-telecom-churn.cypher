// Create Customer Nodes
CREATE (c:Customer {CustomerID: '7590-VHVEG', Gender: 'Female', SeniorCitizen: 0, Partner: 'Yes', Dependents: 'No', Tenure: 1, Churn: 'No'})
CREATE (c:Customer {CustomerID: '5575-GNVDE', Gender: 'Male', SeniorCitizen: 0, Partner: 'No', Dependents: 'No', Tenure: 34, Churn: 'No'})
CREATE (c:Customer {CustomerID: '9305-CDSKC', Gender: 'Female', SeniorCitizen: 0, Partner: 'No', Dependents: 'No', Tenure: 8, Churn: 'Yes'})

// Create PhoneService Nodes
CREATE (p:PhoneService {PhoneService: 'No', MultipleLines: 'No phone service'})
CREATE (p:PhoneService {PhoneService: 'Yes', MultipleLines: 'No'})

// Create InternetService Nodes
CREATE (i:InternetService {InternetService: 'DSL', OnlineSecurity: 'No', OnlineBackup: 'Yes', DeviceProtection: 'No', TechSupport: 'No'})
CREATE (i:InternetService {InternetService: 'Fiber optic', OnlineSecurity: 'Yes', OnlineBackup: 'No', DeviceProtection: 'Yes', TechSupport: 'No'})

// Create StreamingTV Nodes
CREATE (st:StreamingTV {StreamingTV: 'No'})
CREATE (st:StreamingTV {StreamingTV: 'Yes'})

// Create StreamingMovies Nodes
CREATE (sm:StreamingMovies {StreamingMovies: 'No'})
CREATE (sm:StreamingMovies {StreamingMovies: 'Yes'})

// Create Contract Nodes
CREATE (ct:Contract {Contract: 'Month-to-month'})
CREATE (ct:Contract {Contract: 'One year'})

// Create Billing Nodes
CREATE (b:Billing {PaperlessBilling: 'Yes', PaymentMethod: 'Electronic check'})
CREATE (b:Billing {PaperlessBilling: 'No', PaymentMethod: 'Mailed check'})

// Create Charges Nodes
CREATE (ch:Charges {MonthlyCharges: 29.85, TotalCharges: 29.85})
CREATE (ch:Charges {MonthlyCharges: 56.95, TotalCharges: 1889.5})
CREATE (ch:Charges {MonthlyCharges: 99.65, TotalCharges: 820.5})

// Create HAS_PHONE_SERVICE Relationships
MATCH (c:Customer {CustomerID: '7590-VHVEG'}), (p:PhoneService {PhoneService: 'No'}) 
CREATE (c)-[:HAS_PHONE_SERVICE]->(p)

// Create HAS_INTERNET_SERVICE Relationships
MATCH (c:Customer {CustomerID: '5575-GNVDE'}), (i:InternetService {InternetService: 'DSL'}) 
CREATE (c)-[:HAS_INTERNET_SERVICE]->(i)

// Create HAS_STREAMING_TV Relationships
MATCH (c:Customer {CustomerID: '9305-CDSKC'}), (st:StreamingTV {StreamingTV: 'Yes'}) 
CREATE (c)-[:HAS_STREAMING_TV]->(st)

// Create HAS_STREAMING_MOVIES Relationships
MATCH (c:Customer {CustomerID: '9305-CDSKC'}), (sm:StreamingMovies {StreamingMovies: 'Yes'}) 
CREATE (c)-[:HAS_STREAMING_MOVIES]->(sm)

// Create HAS_CONTRACT Relationships
MATCH (c:Customer {CustomerID: '9305-CDSKC'}), (ct:Contract {Contract: 'Month-to-month'}) 
CREATE (c)-[:HAS_CONTRACT]->(ct)

// Create HAS_BILLING Relationships
MATCH (c:Customer {CustomerID: '9305-CDSKC'}), (b:Billing {PaperlessBilling: 'Yes', PaymentMethod: 'Electronic check'}) 
CREATE (c)-[:HAS_BILLING]->(b)

// Create HAS_CHARGES Relationships
MATCH (c:Customer {CustomerID: '7590-VHVEG'}), (ch:Charges {MonthlyCharges: 29.85, TotalCharges: 29.85}) 
CREATE (c)-[:HAS_CHARGES]->(ch)
MATCH (c:Customer {CustomerID: '5575-GNVDE'}), (ch:Charges {MonthlyCharges: 56.95, TotalCharges: 1889.5}) 
CREATE (c)-[:HAS_CHARGES]->(ch)
MATCH (c:Customer {CustomerID: '9305-CDSKC'}), (ch:Charges {MonthlyCharges: 99.65, TotalCharges: 820.5}) 
CREATE (c)-[:HAS_CHARGES]->(ch)


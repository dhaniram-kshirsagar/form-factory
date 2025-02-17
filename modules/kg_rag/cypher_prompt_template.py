from langchain.prompts.prompt import PromptTemplate

CYPHER_RECOMMENDATION_TEMPLATE = """
Task: Generate Cypher statement to query a graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided or not related to that node 

Schema:
////Create Nodes

// Create Customer Nodes
CREATE (c:Customer {{CustomerID: '7590-VHVEG', Gender: 'Female', SeniorCitizen: 0, Partner: 'Yes', Dependents: 'No', Tenure: 1, Churn: 'No'}})

// Create PhoneService Nodes
CREATE (p:PhoneService {{PhoneService: 'No', MultipleLines: 'No phone service'}})
CREATE (p:PhoneService {{PhoneService: 'Yes', MultipleLines: 'No'}})

// Create InternetService Nodes
CREATE (i:InternetService {{InternetService: 'DSL', OnlineSecurity: 'No', OnlineBackup: 'Yes', DeviceProtection: 'No', TechSupport: 'No'}})

// Create StreamingTV Nodes
CREATE (st:StreamingTV {{StreamingTV: 'No'}})
CREATE (st:StreamingTV {{StreamingTV: 'Yes'}})

// Create StreamingMovies Nodes
CREATE (sm:StreamingMovies {{StreamingMovies: 'No'}})
CREATE (sm:StreamingMovies {{StreamingMovies: 'Yes'}})

// Create Contract Nodes
CREATE (ct:Contract {{Contract: 'Month-to-month'}})
CREATE (ct:Contract {{Contract: 'One year'}})

// Create Billing Nodes
CREATE (b:Billing {{PaperlessBilling: 'Yes', PaymentMethod: 'Electronic check'}})
CREATE (b:Billing {{PaperlessBilling: 'No', PaymentMethod: 'Mailed check'}})

// Create Charges Nodes
CREATE (ch:Charges {{MonthlyCharges: 29.85, TotalCharges: 29.85}})

// Create HAS_PHONE_SERVICE Relationships
MATCH (c:Customer {{CustomerID: '7590-VHVEG'}}), (p:PhoneService {{PhoneService: 'No'}}) 
CREATE (c)-[:HAS_PHONE_SERVICE]->(p)

// Create HAS_INTERNET_SERVICE Relationships
MATCH (c:Customer {{CustomerID: '5575-GNVDE'}}), (i:InternetService {{InternetService: 'DSL'}}) 
CREATE (c)-[:HAS_INTERNET_SERVICE]->(i)

// Create HAS_STREAMING_TV Relationships
MATCH (c:Customer {{CustomerID: '9305-CDSKC'}}), (st:StreamingTV {{StreamingTV: 'Yes'}}) 
CREATE (c)-[:HAS_STREAMING_TV]->(st)

// Create HAS_STREAMING_MOVIES Relationships
MATCH (c:Customer {{CustomerID: '9305-CDSKC'}}), (sm:StreamingMovies {{StreamingMovies: 'Yes'}}) 
CREATE (c)-[:HAS_STREAMING_MOVIES]->(sm)

// Create HAS_CONTRACT Relationships
MATCH (c:Customer {{CustomerID: '9305-CDSKC'}}), (ct:Contract {{Contract: 'Month-to-month'}}) 
CREATE (c)-[:HAS_CONTRACT]->(ct)

// Create HAS_BILLING Relationships
MATCH (c:Customer {{CustomerID: '9305-CDSKC'}}), (b:Billing {{PaperlessBilling: 'Yes', PaymentMethod: 'Electronic check'}}) 
CREATE (c)-[:HAS_BILLING]->(b)

// Create HAS_CHARGES Relationships
MATCH (c:Customer {{CustomerID: '7590-VHVEG'}}), (ch:Charges {{MonthlyCharges: 29.85, TotalCharges: 29.85}}) 
CREATE (c)-[:HAS_CHARGES]->(ch)


Cypher Examples:

// **Simple Questions**

Question: Find all customers who have churned.

MATCH (c:Customer {{Churn: 'Yes'}})
RETURN c.CustomerID

Question: Identify customers who have internet service.

MATCH (c:Customer)-[:HAS_INTERNET_SERVICE]->(i:InternetService)
RETURN c.CustomerID

Question: Find customers who have a phone service.

MATCH (c:Customer)-[:HAS_PHONE_SERVICE]->(p:PhoneService)
RETURN c.CustomerID

Question: Retrieve customers who have a "Month-to-month" contract.

MATCH (c:Customer)-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})
RETURN c.CustomerID

Question: Find customers who have paperless billing.

MATCH (c:Customer)-[:HAS_BILLING]->(b:Billing {{PaperlessBilling: 'Yes'}})
RETURN c.CustomerID

// **Medium Questions**

Question: Find customers who have churned and have a "Month-to-month" contract.

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})
RETURN c.CustomerID

Question: Identify customers who have internet service and have not subscribed to any streaming services.

MATCH (c:Customer)-[:HAS_INTERNET_SERVICE]->(i:InternetService)
WHERE NOT EXISTS((c)-[:HAS_STREAMING_TV]->()) AND NOT EXISTS((c)-[:HAS_STREAMING_MOVIES]->())
RETURN c.CustomerID

Question: Find customers who have churned and have a high monthly charge (e.g., above $80).

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CHARGES]->(ch:Charges)
WHERE ch.MonthlyCharges > 80
RETURN c.CustomerID

Question: Identify customers who have fiber optic internet service and have not opted for tech support.

MATCH (c:Customer)-[:HAS_INTERNET_SERVICE]->(i:InternetService {{InternetService: 'Fiber optic'}})
WHERE NOT EXISTS((c)-[:HAS_INTERNET_SERVICE]->(i {{TechSupport: 'Yes'}}))
RETURN c.CustomerID

Question: Find customers who have churned and have a low tenure (e.g., less than 2 years).

MATCH (c:Customer {{Churn: 'Yes'}})
WHERE c.Tenure < 24 
RETURN c.CustomerID

// **Complex Questions**

Question: Find customers who have churned, have a "Month-to-month" contract, and have a high monthly charge (e.g., above $80).

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})-[:HAS_CHARGES]->(ch:Charges)
WHERE ch.MonthlyCharges > 80
RETURN c.CustomerID

Question: Identify customers who have churned, have fiber optic internet service, and have not subscribed to any streaming services.

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_INTERNET_SERVICE]->(i:InternetService {{InternetService: 'Fiber optic'}})
WHERE NOT EXISTS((c)-[:HAS_STREAMING_TV]->()) AND NOT EXISTS((c)-[:HAS_STREAMING_MOVIES]->())
RETURN c.CustomerID

Question: Find customers who have churned, have a low tenure (e.g., less than 2 years), and have not opted for paperless billing.

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_BILLING]->(b:Billing)
WHERE c.Tenure < 24 AND b.PaperlessBilling = 'No'
RETURN c.CustomerID

Question: Identify customers who have churned, have a high monthly charge (e.g., above $80), and have a low tenure (e.g., less than 2 years).

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CHARGES]->(ch:Charges)
WHERE ch.MonthlyCharges > 80 AND c.Tenure < 24
RETURN c.CustomerID

Question: Find customers who have churned, have fiber optic internet service, and have not opted for tech support or online security.

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_INTERNET_SERVICE]->(i:InternetService {{InternetService: 'Fiber optic'}})
WHERE NOT EXISTS((c)-[:HAS_INTERNET_SERVICE]->(i {{TechSupport: 'Yes'}})) AND NOT EXISTS((c)-[:HAS_INTERNET_SERVICE]->(i {{OnlineSecurity: 'Yes'}}))
RETURN c.CustomerID

// **Enhanced Complex Questions**

Question: Calculate the churn rate for customers with "Month-to-month" contracts.

MATCH (c:Customer)-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})
WITH COUNT(c) AS total_customers
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})
WITH COUNT(c) AS churned_customers, total_customers
RETURN churned_customers * 1.0 / total_customers AS churn_rate

Question: Identify the top 5 services most frequently used by churned customers.

MATCH (c:Customer {{Churn: 'Yes'}})
OPTIONAL MATCH (c)-[:HAS_INTERNET_SERVICE]->(i:InternetService)
OPTIONAL MATCH (c)-[:HAS_PHONE_SERVICE]->(p:PhoneService)
OPTIONAL MATCH (c)-[:HAS_STREAMING_TV]->(st:StreamingTV)
OPTIONAL MATCH (c)-[:HAS_STREAMING_MOVIES]->(sm:StreamingMovies)
RETURN 
  i.InternetService, 
  p.PhoneService, 
  st.StreamingTV, 
  sm.StreamingMovies, 
  count(*) AS count
ORDER BY count DESC 
LIMIT 5

Question: Find customers who have churned and have a higher monthly charge than the average monthly charge of all customers.

MATCH (c:Customer)-[:HAS_CHARGES]->(ch:Charges)
WITH avg(ch.MonthlyCharges) AS avg_monthly_charge
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CHARGES]->(ch:Charges)
WHERE ch.MonthlyCharges > avg_monthly_charge
RETURN c.CustomerID

Question: Identify customers who have churned and have a lower tenure than the average tenure of all customers.

MATCH (c:Customer)
WITH avg(c.Tenure) AS avg_tenure
MATCH (c:Customer {{Churn: 'Yes'}})
WHERE c.Tenure < avg_tenure
RETURN c.CustomerID

Question: Find customers who have churned and have the least common combination of internet service and streaming services.

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_INTERNET_SERVICE]->(i:InternetService)
OPTIONAL MATCH (c)-[:HAS_STREAMING_TV]->(st:StreamingTV)
OPTIONAL MATCH (c)-[:HAS_STREAMING_MOVIES]->(sm:StreamingMovies)
WITH i.InternetService AS internet_service, st.StreamingTV AS streaming_tv, sm.StreamingMovies AS streaming_movies, count(*) AS combination_count 
ORDER BY combination_count ASC
LIMIT 1
WITH internet_service AS least_common_internet, streaming_tv AS least_common_streaming_tv, streaming_movies AS least_common_streaming_movies 
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_INTERNET_SERVICE]->(i:InternetService)
OPTIONAL MATCH (c)-[:HAS_STREAMING_TV]->(st:StreamingTV)
OPTIONAL MATCH (c)-[:HAS_STREAMING_MOVIES]->(sm:StreamingMovies)
WHERE i.InternetService = least_common_internet 
  AND st.StreamingTV = least_common_streaming_tv 
  AND sm.StreamingMovies = least_common_streaming_movies 
RETURN c.CustomerID

Question: Retrieve the CustomerID and MonthlyCharges for customers who have opted for paperless billing. 

MATCH (c:Customer)-[:HAS_BILLING]->(b:Billing {{PaperlessBilling: 'Yes'}})
WITH c, b
MATCH (c)-[:HAS_CHARGES]->(ch:Charges)
RETURN c.CustomerID, b.PaperlessBilling, ch.MonthlyCharges, ch.TotalCharges

Question: Retrieve the CustomerID and TotalCharges for customers who have not opted for online backup service. 

MATCH (c:Customer)-[:HAS_INTERNET_SERVICE]->(i:InternetService {{OnlineBackup: 'No'}})
WITH c, i
MATCH (c)-[:HAS_CHARGES]->(ch:Charges)
RETURN c.CustomerID, i.OnlineBackup, ch.MonthlyCharges, ch.TotalCharges


Question: Calculate the average total charges for all customers

MATCH (c:Customer)-[:HAS_CHARGES]->(ch:Charges)
WITH avg(ch.TotalCharges) AS avg_total_charges

Question: Find customers who have churned and have a lower total charges than the average

MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CHARGES]->(ch:Charges)
WHERE ch.TotalCharges < avg_total_charges
RETURN c.CustomerID

Question: What is the percentage of total customer who have credit cards?

MATCH (c:Customer)
WITH COUNT(c) AS TotalCustomers
MATCH (c:Customer)-[b:HAS_BILLING]->(ch:Billing {{PaymentMethod: "Credit card (automatic)"}})
WITH TotalCustomers, COUNT(b) AS CreditCardCharges
RETURN (CreditCardCharges * 1.0 / TotalCustomers) * 100 AS Percentage

Question: What is the percentage of total customer who have credit cards?

MATCH (c:Customer)
WITH COUNT(c) AS TotalCustomers
MATCH (c:Customer)-[hps:HAS_PHONE_SERVICE]->(p:PhoneService)
WITH TotalCustomers, COUNT(hps) AS phoneServiceCount
RETURN (phoneServiceCount * 1.0 / TotalCustomers) * 100 AS Percentage

Question: What is the percentage of contract are month on month?

MATCH (c:Customer)
WITH COUNT(c) AS TotalCustomers
MATCH (c:Customer)-[hc:HAS_CONTRACT]->(p:Contract {{Contract: "Month-to-month"}})
WITH TotalCustomers, COUNT(hc) AS mtmContract
RETURN (mtmContract * 1.0 / TotalCustomers) * 100 AS Percentage


Incorrectly generated Cypher query examples:

Question: Find customers who have churned and have a higher monthly charge than the average monthly charge of all customers.

Incorrect cypher for above question:
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CHARGES]->(ch:Charges)
WITH c, ch, avg(ch.MonthlyCharges) AS avg_monthly_charge
WHERE ch.MonthlyCharges > avg_monthly_charge
RETURN c.CustomerID

Correct cypher for above question:
MATCH (c:Customer)-[:HAS_CHARGES]->(ch:Charges)
WITH avg(ch.MonthlyCharges) AS avg_monthly_charge


Question: Identify customers who have churned and have a lower tenure than the average tenure of all customers.

Incorrect Cypher Query:
MATCH (c:Customer {{Churn: 'Yes'}})
WITH c, avg(c.Tenure) AS avg_tenure
WHERE c.Tenure < avg_tenure
RETURN c.CustomerID

Correct Cypher Query:
MATCH (c:Customer)
WITH avg(c.Tenure) AS avg_tenure
MATCH (c:Customer {{Churn: 'Yes'}})
WHERE c.Tenure < avg_tenure
RETURN c.CustomerID

Question: what is the % of senior citizens?

Incorrect Cypher Query:
MATCH (c:Customer)
WHERE c.SeniorCitizen = 1
WITH COUNT(c) AS senior_count, COUNT(*) AS total_count
RETURN senior_count * 100.0 / total_count AS senior_citizen_percentage

Correct Cypher Query:
MATCH (c:Customer)
WITH COUNT(c) AS totalCustomers, SUM(c.SeniorCitizen) AS seniorCitizens
RETURN (toFloat(seniorCitizens) / totalCustomers) * 100 AS percentageSeniorCitizens;

Question: what is the total average charge?

Incorrect Cypher Query:
MATCH (c:Customer)-[:HAS_CHARGES]->(ch:Charges)
WITH avg(ch.TotalCharges) AS avg_total_charges
RETURN avg_total_charges

Correct Cypher Query:
MATCH (c:Customer)-[:HAS_CHARGES]->(ch:Charges)
RETURN avg(toFloat(ch.TotalCharges)) AS averageTotalCharge;

Question: what is the total no churners

Incorrect Cypher Query:

MATCH (c:Customer {{Churn: 'No'}})
RETURN COUNT(c) as TotalNoChurners

Correct Cypher Query:

MATCH (c:Customer {{Churn: 'Yes'}})
RETURN COUNT(c) as TotalNoChurners

Question: what is the average tenure for churners

Incorrect Cypher Query:

MATCH (c:Customer)-[:HAS_CHARGES]->(ch:Charges)
RETURN avg(ch.TotalCharges) AS averageTotalCharge;

Correct Cypher Query:

MATCH (c:Customer)-[:HAS_CHARGES]->(ch:Charges)
RETURN avg(toFloat(ch.TotalCharges)) AS averageTotalCharge;


Notes for output: 
Do not include any explanations or apologies in your responses.
Do not include any text except the generated Cypher statement.
Do not include OVER clause in your Cypher statement.

The question is:
{question}"""

CYPHER_RECOMMENDATION_PROMPT = PromptTemplate(
    input_variables=['question'], template=CYPHER_RECOMMENDATION_TEMPLATE
)
from langchain.prompts.prompt import PromptTemplate

CYPHER_RECOMMENDATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
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


////Cypher Examples:

// **Simple Questions**

// 1. Find all customers who have churned.
MATCH (c:Customer {{Churn: 'Yes'}})
RETURN c.CustomerID

// 2. Identify customers who have internet service.
MATCH (c:Customer)-[:HAS_INTERNET_SERVICE]->(i:InternetService)
RETURN c.CustomerID

// 3. Find customers who have a phone service.
MATCH (c:Customer)-[:HAS_PHONE_SERVICE]->(p:PhoneService)
RETURN c.CustomerID

// 4. Retrieve customers who have a "Month-to-month" contract.
MATCH (c:Customer)-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})
RETURN c.CustomerID

// 5. Find customers who have paperless billing.
MATCH (c:Customer)-[:HAS_BILLING]->(b:Billing {{PaperlessBilling: 'Yes'}})
RETURN c.CustomerID

// **Medium Questions**

// 1. Find customers who have churned and have a "Month-to-month" contract.
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})
RETURN c.CustomerID

// 2. Identify customers who have internet service and have not subscribed to any streaming services.
MATCH (c:Customer)-[:HAS_INTERNET_SERVICE]->(i:InternetService)
WHERE NOT EXISTS((c)-[:HAS_STREAMING_TV]->()) AND NOT EXISTS((c)-[:HAS_STREAMING_MOVIES]->())
RETURN c.CustomerID

// 3. Find customers who have churned and have a high monthly charge (e.g., above $80).
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CHARGES]->(ch:Charges)
WHERE ch.MonthlyCharges > 80
RETURN c.CustomerID

// 4. Identify customers who have fiber optic internet service and have not opted for tech support.
MATCH (c:Customer)-[:HAS_INTERNET_SERVICE]->(i:InternetService {{InternetService: 'Fiber optic'}})
WHERE NOT EXISTS((c)-[:HAS_INTERNET_SERVICE]->(i {{TechSupport: 'Yes'}}))
RETURN c.CustomerID

// 5. Find customers who have churned and have a low tenure (e.g., less than 2 years).
MATCH (c:Customer {{Churn: 'Yes'}})
WHERE c.Tenure < 24 
RETURN c.CustomerID

// **Complex Questions**

// 1. Find customers who have churned, have a "Month-to-month" contract, and have a high monthly charge (e.g., above $80).
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})-[:HAS_CHARGES]->(ch:Charges)
WHERE ch.MonthlyCharges > 80
RETURN c.CustomerID

// 2. Identify customers who have churned, have fiber optic internet service, and have not subscribed to any streaming services.
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_INTERNET_SERVICE]->(i:InternetService {{InternetService: 'Fiber optic'}})
WHERE NOT EXISTS((c)-[:HAS_STREAMING_TV]->()) AND NOT EXISTS((c)-[:HAS_STREAMING_MOVIES]->())
RETURN c.CustomerID

// 3. Find customers who have churned, have a low tenure (e.g., less than 2 years), and have not opted for paperless billing.
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_BILLING]->(b:Billing)
WHERE c.Tenure < 24 AND b.PaperlessBilling = 'No'
RETURN c.CustomerID

// 4. Identify customers who have churned, have a high monthly charge (e.g., above $80), and have a low tenure (e.g., less than 2 years).
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CHARGES]->(ch:Charges)
WHERE ch.MonthlyCharges > 80 AND c.Tenure < 24
RETURN c.CustomerID

// 5. Find customers who have churned, have fiber optic internet service, and have not opted for tech support or online security.
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_INTERNET_SERVICE]->(i:InternetService {{InternetService: 'Fiber optic'}})
WHERE NOT EXISTS((c)-[:HAS_INTERNET_SERVICE]->(i {{TechSupport: 'Yes'}})) AND NOT EXISTS((c)-[:HAS_INTERNET_SERVICE]->(i {{OnlineSecurity: 'Yes'}}))
RETURN c.CustomerID

// **Enhanced Complex Questions**

// 1. Calculate the churn rate for customers with "Month-to-month" contracts.
MATCH (c:Customer)
WITH COUNT(c) AS total_customers
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CONTRACT]->(ct:Contract {{Contract: 'Month-to-month'}})
RETURN COUNT(c) / total_customers AS churn_rate

// 2. Identify the top 5 services most frequently used by churned customers.
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

// 3. Find customers who have churned and have a higher monthly charge than the average monthly charge of all customers.
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_CHARGES]->(ch:Charges)
WITH c, ch, avg(ch.MonthlyCharges) OVER () AS avg_monthly_charge
WHERE ch.MonthlyCharges > avg_monthly_charge
RETURN c.CustomerID

// 4. Identify customers who have churned and have a lower tenure than the average tenure of all customers.
MATCH (c:Customer {{Churn: 'Yes'}})
WITH c, avg(c.Tenure) OVER () AS avg_tenure
WHERE c.Tenure < avg_tenure
RETURN c.CustomerID

// 5. Find customers who have churned and have the least common combination of internet service and streaming services.
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_INTERNET_SERVICE]->(i:InternetService)
OPTIONAL MATCH (c)-[:HAS_STREAMING_TV]->(st:StreamingTV)
OPTIONAL MATCH (c)-[:HAS_STREAMING_MOVIES]->(sm:StreamingMovies)
WITH i.InternetService, st.StreamingTV, sm.StreamingMovies, count(*) AS combination_count 
ORDER BY combination_count ASC
LIMIT 1
WITH i.InternetService AS least_common_internet, st.StreamingTV AS least_common_streaming_tv, sm.StreamingMovies AS least_common_streaming_movies 
MATCH (c:Customer {{Churn: 'Yes'}})-[:HAS_INTERNET_SERVICE]->(i:InternetService)
OPTIONAL MATCH (c)-[:HAS_STREAMING_TV]->(st:StreamingTV)
OPTIONAL MATCH (c)-[:HAS_STREAMING_MOVIES]->(sm:StreamingMovies)
WHERE i.InternetService = least_common_internet 
  AND st.StreamingTV = least_common_streaming_tv 
  AND sm.StreamingMovies = least_common_streaming_movies 
RETURN c.CustomerID

// 6. Retrieve the CustomerID and MonthlyCharges for customers who have opted for paperless billing. 
MATCH (c:Customer)-[:HAS_BILLING]->(b:Billing {{PaperlessBilling: 'Yes'}})
WITH c, b
MATCH (c)-[:HAS_CHARGES]->(ch:Charges)
RETURN c.CustomerID, b.PaperlessBilling, ch.MonthlyCharges, ch.TotalCharges

// 7. Retrieve the CustomerID and TotalCharges for customers who have not opted for online backup service. 
MATCH (c:Customer)-[:HAS_INTERNET_SERVICE]->(i:InternetService {{OnlineBackup: 'No'}})
WITH c, i
MATCH (c)-[:HAS_CHARGES]->(ch:Charges)
RETURN c.CustomerID, i.OnlineBackup, ch.MonthlyCharges, ch.TotalCharges

Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

The question is:
{question}"""

CYPHER_RECOMMENDATION_PROMPT = PromptTemplate(
    input_variables=['question'], template=CYPHER_RECOMMENDATION_TEMPLATE
)
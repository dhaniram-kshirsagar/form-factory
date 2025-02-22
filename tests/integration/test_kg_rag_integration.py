import sys
import os
import pytest
import pandas as pd
from modules.kg_rag.kg_rag import get_kg_answer, init_graph
from modules.kg_rag.cypher_prompt_template import CYPHER_RECOMMENDATION_PROMPT
from modules.kg_rag.qa_prompt_template import QA_PROMPT

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Load the TelecomChurn dataset for data-driven tests
telecom_data = pd.read_csv('/Users/dhani/foamvenv/smart-data-intelligence/apps/telecom_churn/modules/data/large-data/TelecomChurn.csv')

@pytest.fixture(scope='module', autouse=True)
def initialize_graph():
    # Initialize the Neo4j graph and QA chain before running the tests
    init_graph()

@pytest.fixture
def sample_questions():
    # Sample questions based on the TelecomChurn dataset
    return [
        'What is the churn rate for customers in California?',
        'Which plan has the highest churn rate?',
        'How many customers have churned in the last month?',
        'What is the average tenure of churned customers?'
    ]


def test_basic_query():
    # Test a simple question
    question = 'What is the total number of customers?'
    result = get_kg_answer(question)
    assert result is not None
    assert isinstance(result, str)
    # Validate against the dataset
    expected_total_customers = len(telecom_data)
    assert str(expected_total_customers) in result


def test_complex_query():
    # Test a complex question
    question = 'What is the churn rate for customers on Plan A in California?'
    result = get_kg_answer(question)
    assert result is not None
    assert isinstance(result, str)
    # Validate against the dataset
    filtered_data = telecom_data[(telecom_data['Plan'] == 'Plan A') & (telecom_data['State'] == 'California')]
    churn_rate = filtered_data['Churn'].mean()
    assert str(churn_rate) in result


def test_edge_case_empty_question():
    # Test with an empty question
    question = ''
    result = get_kg_answer(question)
    assert result is None or 'Invalid question' in result


def test_data_driven_query(sample_questions):
    # Test with data-driven questions
    for question in sample_questions:
        result = get_kg_answer(question)
        assert result is not None
        assert isinstance(result, str)
        # Validate against the dataset
        if 'churn rate' in question.lower():
            state = question.split('in ')[-1].replace('?', '')
            filtered_data = telecom_data[telecom_data['State'] == state]
            churn_rate = filtered_data['Churn'].mean()
            assert str(churn_rate) in result
        elif 'highest churn rate' in question.lower():
            churn_rates = telecom_data.groupby('Plan')['Churn'].mean()
            highest_plan = churn_rates.idxmax()
            assert highest_plan in result
        elif 'churned in the last month' in question.lower():
            churned_count = telecom_data[telecom_data['Churn'] == 1].shape[0]
            assert str(churned_count) in result
        elif 'average tenure' in question.lower():
            avg_tenure = telecom_data[telecom_data['Churn'] == 1]['Tenure'].mean()
            assert str(avg_tenure) in result

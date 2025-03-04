import time
import streamlit as st
import pandas as pd
import json
import plotly.express as px
from modules.ml import ml_rag

# Import set_custom_css() and kg_rag from Factory_Bot.py


css ="""
    <style>
.stPlotlyChart {
    border-radius: 0.5rem;
    #box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    padding: -1rem;
    margin-top: -1rem;
    }
    </style>
    """
    
def Show_Factoryastro():
    st.title("Predict Factory Performance with Factory Astro")
    st.markdown(css, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader('Ask Questions!')

        if 'chat_history_astro' not in st.session_state:
            st.session_state.chat_history_astro = []  # Initialize

        if prompt := st.chat_input(placeholder="Ask a question about factory performance"):
            with st.spinner("Analyzing data... ⏳"):
                llm_response = ml_rag.get_ml_answer(prompt)
                response_text = None  # Ensure initialization
                parsed_response = None 

                try:
                    parsed_response = json.loads(llm_response)
                    response_text = parsed_response.get("llm_output_text_summmary", "")

                    # Append the user and bot messages to the chat history
                    st.session_state.chat_history_astro.append(('You', prompt))
                    st.session_state.chat_history_astro.append(('Bot', response_text))
                    st.session_state.astro_last_llm_response = parsed_response  # Store the last response

                except json.JSONDecodeError:
                    st.error("Oops! Looks like my engine is having trouble understanding your request. Please try again.")
                    st.session_state.chat_history_astro.append(('You', prompt))
                    st.session_state.chat_history_astro.append(('Bot', "Error: Could not process request."))

                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                    st.session_state.chat_history_astro.append(('You', prompt))
                    st.session_state.chat_history_astro.append(('Bot', f"An unexpected error occurred: {e}"))

                finally:
                    st.rerun()  # Rerun to show the message
                    
        st.markdown('NOTE: The graph will not be displayed if the prediction data has fewer than 3 records.', unsafe_allow_html=True)

        # Display chat history
        st.markdown('<h5>Chat History</h5>', unsafe_allow_html=True)
        hcol1, hcol2 = st.columns([1, 1])
        with hcol1:
            for i in range(len(st.session_state.chat_history_astro)-1, -1, -2):
                if i-1 >= 0:
                    bot_role, bot_msg = st.session_state.chat_history_astro[i-1]
                    with st.chat_message("assistant"):
                        st.markdown(f'**{bot_role}:** {bot_msg}')
                if i >= 0:
                    user_role, user_msg = st.session_state.chat_history_astro[i]
                    with st.chat_message("user"):
                        st.markdown(f'**{user_role}:** {user_msg}')
            
        with hcol2:
            if 'astro_last_llm_response' in st.session_state and st.session_state.astro_last_llm_response is not None:
                parsed_response = st.session_state.astro_last_llm_response
                response_text = parsed_response.get("llm_output_text_summmary", "")

                if 'Predicted_data' in parsed_response:
                    data = pd.DataFrame(parsed_response['Predicted_data'])
                    if len(data) >= 3:
                        x_col, y_col = None, None
                        for col in data.columns:
                            if "month" in col.lower():
                                x_col = col
                            if "prediction" in col.lower():
                                y_col = col

                        if x_col and y_col:
                            is_density_prediction = "density" in response_text.lower()
                            is_vol_prediction = "volume" in response_text.lower()
                            is_rev_prediction = "revenue" in response_text.lower()

                            title = 'Prediction'
                            if is_density_prediction:
                                title = 'Foam Density'
                            elif is_rev_prediction:
                                title = 'Revenue'
                            elif is_vol_prediction:
                                title = 'Production Volume'

                            if is_density_prediction:
                                data[y_col] *= 100000
                                st.markdown("Note: Density values multiplied by 100,000.")

                            fig = px.line(
                                data, x=x_col, y=y_col, 
                                color=None,
                                height=300, width=600
                            )
                            st.plotly_chart(fig)
                    else:
                        st.warning("No Graph Generated! Data has less than 3 Predictions.")
                else:
                    st.error("No Predicted Data Found!")

    with col2:
        st.markdown(
            """
            <style>
            /* Ensure subheader (and other headings) are left-aligned */
            h1, h2, h3, h4, h5, h6 {
                text-align: left;
            }
            /* Align text within buttons to the left and add some left padding */
            div.stButton button {
                text-align: left;
                padding-left: 10px;
            }
            /* Style buttons */
            .stButton > button {
             border-radius: 8px;
             padding: 10px 20px;
             font-weight: 500;
             transition: all 0.3s ease;
             box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            /* Add left alignment */
             display: block;
             text-align: left;
            width: 100%;  /* Make buttons full width of the column */
            }   
            </style>
            """,
            unsafe_allow_html=True
         )
        st.subheader("Example Questions")
        examples = [
            "What will the revenue for factory 3 be over the next 6 months?",
            "What will the revenue over the next year for factory 3?",
            "What will the profit margin be from July to December for factory 2?",
            "What will the profit margin of factory 1 over the next quarter?",
            "What will the production volume be over the next 6 months?",
            "Get me the production volume for factory 4 from July to December."
            "What will the revenue for factory 3 be next year?",
            "What will the revenue over the next 2 months for factory 3?",
            "What will the profit margin be in July for factory 2?",
            "What will the profit margin of factory 1?",
            "What will the production volume be over the next 2 months?",
            "Get me the production volume for factory 4 in the month of July."
        ]

        for i, example in enumerate(examples):
            if st.button(example, key=f"example_{i}"):
                with st.spinner("Analyzing data... ⏳"):
                    llm_response = ml_rag.get_ml_answer(example)
                    response_text = None
                    parsed_response = None

                    try:
                        parsed_response = json.loads(llm_response)
                        response_text = parsed_response.get("llm_output_text_summmary", "")

                        # Update chat history
                        st.session_state.chat_history_astro.append(('You', example))
                        st.session_state.chat_history_astro.append(('Bot', response_text))
                        st.session_state.astro_last_llm_response = parsed_response

                    except json.JSONDecodeError:
                        st.error("Oops! Something went wrong.")
                        st.session_state.chat_history_astro.append(('You', example))
                        st.session_state.chat_history_astro.append(('Bot', "Error: Could not process request."))

                    except Exception as e:
                        st.error(f"Unexpected error: {e}")
                        st.session_state.chat_history_astro.append(('You', example))
                        st.session_state.chat_history_astro.append(('Bot', f"Unexpected error: {e}"))

                    finally:
                        st.rerun()

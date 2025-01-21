import time
import streamlit as st
import pandas as pd
import json
from modules.ml import ml_rag
import plotly.express as px

def Show_Factoryastro():
    st.subheader("📝 Predict Factory Performance with Factory Astro")

    markdown = """
        ### Examples of questions you can ask:
     - **Revenue Predictions**:
        - What will the revenue for factory 3 be next year?
        - What will the revenue over the next 2 months for factory 3 in city C be?
     - **Foam Density**:
        - What will the foam density be in July for factory 2?
        - What will the foam density of factory 1 in city A be?
     - **Production Volume**:
        - What will the production volume be over the next 2 months?
        - Get me the production volume for factory 4 in city C in the month of July.
    """

    st.markdown(markdown)


    # Initialize Session State
    if "astro_messages" not in st.session_state:
        st.session_state.astro_messages = [
            {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
        ]
    if "astro_response" not in st.session_state:
        st.session_state["astro_response"] = None

    if "astro_waiting_for_response" not in st.session_state:
        st.session_state.astro_waiting_for_response = False

    messages = st.session_state.astro_messages
    for msg in messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="e.g. Get me production volume for factor 4 city c in month of July.", disabled=st.session_state.astro_waiting_for_response) :
        if not st.session_state.astro_waiting_for_response:
            st.session_state.astro_messages.append({"role": "user", "content": prompt})
            st.session_state.astro_last_user_message = prompt
            st.chat_message("user").write(prompt)
          
            st.session_state.astro_waiting_for_response = True
        #st.rerun()
    # Handle assistant's response after user submits input
    if st.session_state.astro_waiting_for_response:
        with st.spinner("Assistant is typing..."):
            try:
                llm_response = ml_rag.get_ml_answer(st.session_state.astro_last_user_message)
                try:
                    parsed_response = json.loads(llm_response)
                    st.session_state["astro_response"] = parsed_response["llm_output_text_summmary"]
                    st.chat_message("assistant").write(st.session_state["astro_response"])
                    st.write('''NOTE Its work in progress... In the generated output: Add +1 to Factory name. 
                 Assume City A if "location 0", City B if "location 1" and so on.. We are working to map factory and location names.''')

                    if 'Predicted_data' in parsed_response:
                        data = pd.DataFrame(parsed_response['Predicted_data'])
                    
                        # Dynamically determine x and y columns
                        if len(data) >= 3:
                            x_col = None
                            y_col = None
                            for col in data.columns:
                                if "month" in col.lower():
                                    x_col = col
                                if "prediction" in col.lower():
                                    y_col = col

                            if x_col and y_col:
                                # Check if it is a density prediction
                                is_density_prediction = "density" in str(st.session_state["astro_response"]).lower()
                                is_vol_prediction = "volume"  in str(st.session_state["astro_response"]).lower()
                                is_rev_prediction = "revenue"  in str(st.session_state["astro_response"]).lower()

                                title = ''
                                if is_density_prediction:
                                    title = 'Foam Density'
                                if is_rev_prediction:
                                    title = 'Revenue'
                                if is_vol_prediction:
                                    title = 'Volume'

                                # Apply the transformation if it's density and multiply prediction by 100000
                                if is_density_prediction:
                                    data[y_col] = data[y_col] * 100000
                                    st.markdown("Note: Predicted density values multiplied by 100,000.")
                                
                                #st.header("Predicted "+title, divider="gray")
                                fig = px.line(
                                    data, 
                                    x=x_col, 
                                    y=y_col, 
                                    color='Location' if 'Location' in data.columns else None,
                                    height=400,  # Reduced height
                                    width=700,
                                    title= "Predicted "+title  # Reduced width
                                )
                                left, middle, right = st.columns((2, 5, 2))
                                with middle:
                                    st.plotly_chart(fig)
                        else:
                                st.warning("No Graph Genrated!!!  Data has less than 3 Predictions.", icon="⚠️")  
                    else:
                        st.error("No Predicted Data Found!!!")
                except json.JSONDecodeError as e:
                    st.error(f"Oops! looks like my engine is having trouble understanding your request. Please try again.")
            except Exception as e:
                st.error(f"Oops! looks like my engine is having trouble understanding your request. Please try again.")

                st.session_state.astro_messages.append(
                {"role": "assistant", "content": st.session_state["astro_response"]}
            )
               
               
            finally:
                st.session_state.astro_waiting_for_response = False
                
    
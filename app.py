import streamlit as st 


st.title('111 Mental Health (Option 2) Call Centre Discrete Event Simulation Model')
st.write('This is some blurb describing the model')

tab1, tab2, tab3, tab4 = st.tabs(["1, Demand", "2, Staffing", "3, Other Variables","4, Run the Model"])


with tab1: 
    st.header("Demand Details")
    st.write("Use the grid below to update the expected number of calls per hour")




with tab2:  
    st.header("Staffing Details")
    st.write("Use the grid below to update the expected staffing levels for each hour")


with tab3:
    st.header("Other Variables")
    st.write("Use this page to change other model variables, such as call length, work time, break time ect")
    
    col1, col2 = st.columns(2)

    with col1:
        st.write("Column 1")

    with col2:
        st.write("Column 2")


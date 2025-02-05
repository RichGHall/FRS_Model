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

    st.subheader("No. Runs")
    st.write("How many times will you loop through the model ?")
    no_runs = st.slider("Number of model runs",min_value=0,max_value=500,value=1)   


    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Public Callers")
        
        st.text("Talk Time")
        st.write("How long will calls last ?")
        pub_call_len = st.slider("Call Length (minutes)",min_value=0,max_value=60,value=1)   

        st.text("Write Up Time")
        st.write("How much time is spent on post-call admin ?")
        pub_work_len = st.slider("Call Length (minutes)",min_value=0,max_value=60,value=1)

        st.text("Call Back Probability - Handled Calls")
        st.write("Chance of calling back following a successful call ?")
        pub_cb_han = st.slider("Call Length (minutes)",min_value=0,max_value=1,value=0.01)
 
        st.text("Call Back Probability - Abandoned Calls")
        st.write("Chance of calling back following an unsuccessful call ?")
        pub_cb_abd = st.slider("Call Length (minutes)",min_value=0,max_value=1,value=0.01)


    with col2:
        st.write("Column 2")


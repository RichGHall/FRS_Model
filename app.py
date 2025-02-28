import streamlit as st 


# Streamlit app code 




st.title('111 Mental Health (Option 2) Call Centre Discrete Event Simulation Model')
st.write('This is some blurb describing the model')

tab0, tab1, tab2, tab3, tab4 = st.tabs(["1, Demand", "2, Staffing", "3, Other Variables","4, Run the Model"])


with tab0:
    st.header("Introduction")
    st.write("This model is designed to simulate the operation of a mental health call centre. The model is based on the 111 service, but has been adapted to focus on mental health calls. The model is a discrete event simulation model, which means that it simulates the operation of the call centre in minute-by-minute detail. The model is designed to help you understand how the call centre operates, and to help you identify ways to improve the service. The model is based on a number of assumptions, which are described below. The model is designed to be easy to use, and you can change the assumptions to see how they affect the operation of the call centre. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it. The model is designed to be used by people who are not experts in simulation modelling, so you do not need to have any special skills to use it.")
    st.write("The model is based on the following assumptions:")
      

with tab1: 
    st.header("Demand Details")
    st.write("Use the grid below to update the expected number of calls per hour")


with tab2:  
    st.header("Staffing Details")
    st.write("Use the grid below to update the expected staffing levels for each hour")


with tab3:
    ## description of the tab and how to use it
    st.header("Other Variables")
    st.write("Use this page to change other model variables, such as call length, work time, break time ect")

    st.subheader("No. Runs")
    st.write("How many times will you loop through the model ?")
    no_runs = st.slider("Number of model runs",min_value=0,max_value=500,value=1)   

    #setup columns
    col1, col2, col3 = st.columns(3)

    #column related to public caller variables
    with col1:
        st.subheader("Public Callers")
        


        #public talk time
        st.text("Talk Time")
        st.write("How long will calls last ?")
        pub_call_len = st.slider("Public Call Length (minutes)",min_value=0,max_value=60,value=1)   

        st.text("Write Up Time")
        st.write("How much time is spent on post-call admin ?")
        pub_work_len = st.slider("Public Work Length (minutes)",min_value=0,max_value=60,value=1)

        st.text("Call Back Probability - Handled Calls")
        st.write("Chance of calling back following a successful call ?")
        pub_cb_han = st.slider(
                                "Public Call Back Probability Handled",
                                min_value=0.0,    # float
                                max_value=1.0,    # float
                                value=0.01,       # float
                                step=0.01         # float
                            )
 
        st.text("Call Back Probability - Abandoned Calls")
        st.write("Chance of calling back following an unsuccessful call ?")
        pub_cb_abd = st.slider(
                                "Public Call Back Probability Abandoned",
                                min_value=0.0,    # float
                                max_value=1.0,    # float
                                value=0.01,       # float
                                step=0.01         # float
                            )
    
    #left as a gap for formating purposes
    with col2:
        st.write(" ")

    #column related to public caller variables
    with col3:
 
        st.subheader("Professional Callers")
        
        st.text("Talk Time")
        st.write("How long will calls last ?")
        pub_call_len = st.slider("Prof Call Length (minutes)",min_value=0,max_value=60,value=1)   

        st.text("Write Up Time")
        st.write("How much time is spent on post-call admin ?")
        pub_work_len = st.slider("Prof Work Length (minutes)",min_value=0,max_value=60,value=1)

        st.text("Call Back Probability - Handled Calls")
        st.write("Chance of calling back following a successful call ?")
   #     pub_cb_han = st.slider("Prof Call Back Probability Handled",min_value=0,max_value=1,value=0.01,step=0.01)
 
        st.text("Call Back Probability - Abandoned Calls")
        st.write("Chance of calling back following an unsuccessful call ?")
   #     pub_cb_abd = st.slider("Prof Call Back Probability Abd",min_value=0,max_value=1,value=0.01,step=0.01)

import streamlit as st 
import pandas as pd

st.set_page_config(layout="wide")

# Streamlit app code 




st.title('111 Mental Health (Option 2) Call Centre Discrete Event Simulation Model')
st.write('This is some blurb describing the model')

tab0, tab1, tab2, tab3, tab4 = st.tabs(["About","1, Demand", "2, Staffing", "3, Other Variables","4, Run the Model"])


with tab0:
    st.header("Introduction")
    st.write("This model is designed to simulate the operation of a mental health call centre.")
    st.write("The model is based on the following assumptions:")
      

with tab1: 
    st.header("Demand Details")
    st.write("Use the grid below to update the expected number of calls per hour")
        #setup columns
    col1, col2, col3 = st.columns(3)

    #column related to public caller variables
    with col1:
        st.subheader("Public Callers")

        public_df = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Public_Av_Calls.csv")
        public_IAT = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Public_IAT.csv")
                
        
        edited_public_df = st.data_editor(public_df)
        public_updated = st.button("Update Public Calls")
        if public_updated:
            #update to a new dataframe 
            #run process for updating the main dataframe
            for index, row in edited_public_df.iterrows():
                public_IAT.loc[index,"mean_iat"] = 60 / edited_public_df.loc[index,"Average Calls"]
                public_df.loc[index,"Average Calls"] = edited_public_df.loc[index,"Average Calls"]

                public_IAT.to_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Public_IAT.csv",index=False)
                public_df.to_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Public_Av_Calls.csv",index=False)



            st.write("Public Calls Updated")






























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

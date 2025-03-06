import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
from FRSModel import Trial, g 




st.set_page_config(layout="wide")

st.title('111 Mental Health (Option 2) Call Centre Discrete Event Simulation Model')
st.write('This is some blurb describing the model')

tab0, tab1 = st.tabs(["The Model","About"])


with tab0:

    col1, col2 = st.columns(2)

    with col1:


        st.header("The Model")
        st.write("Use this section to .")

        st.markdown("## Demand")

        st.write("Use the grids below to update the expected number of calls per hour.")
        st.write("This should be new callers only, the model will calcuate whether they will call back or not")

            #setup columns
        with st.expander("Click here to Adjust Demand to the Public Line"):    
            st.subheader("Public Line - Average Calls per hour")
            st.write("Use the grid below to update the expected number of calls per hour for the Public Line")

            public_df = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Public_Av_Calls.csv")
            edited_public_df = st.data_editor(public_df, num_rows=24)
                
        with st.expander("Click here to Adjust Demand to the Professional Line"):  
            st.subheader("Professional Line - Average Calls per hour")
            st.write("Use the grid below to update the expected number of calls per hour for the Professional Line")

            prof_df = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Prof_Av_Calls.csv")  
            edited_prof_df = st.data_editor(prof_df, num_rows=24)


        st.divider()
        st.markdown("## Staffing Levels")

        st.write("Use the grid below to update the number of staff on shift per hour")
        
        with st.expander("Click here to Adjust Staffing Levels"):
            st.subheader("Staffing Levels")

            staffinf_df = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Senior_Resources.csv")  
            df_staff_renamed  = staffinf_df.rename(columns={"t": "Hour", "res": "Staff"})
            df_staff_renamed["Hour"] =  df_staff_renamed["Hour"] / 60
            
            df_staff_edited = st.data_editor(df_staff_renamed, num_rows=24) 
        
        st.write(" ")
        st.divider()
        st.markdown("## Call Details")
        st.write("This section updates the call details")

        subcol1,subcol2,subcol3 = st.columns(3)
        
        with subcol1:

            st.subheader("Public Callers")
#            st.text("Talk Time")
#            st.write("How long will calls last ?")
#            pub_call_len = st.slider("Public Call Length (minutes)",min_value=0,max_value=60,value=1)   
            

            st.markdown("##### Write Up Time")
            st.write("How much time is spent on post-call admin ?")
            pub_work_len = st.slider("Average Admin time - Public Calls",min_value=0,max_value=60,value=g.mean_public_work)
            
            st.write(" ")
            st.divider() 
            st.markdown("##### Call Back Probability - Handled Calls")
            st.write("Chance of calling back following a successful call ?")
            pub_cb_han = st.slider(
                                    "Callback probability - handled calls",
                                    min_value=0,    # float
                                    max_value=100,    # float
                                    value=round(g.call_back_prob_handled*100),       # float
                                    step=1         # float
                                )/100
    
            st.write(" ")
            st.divider()
            st.markdown("##### Call Back Probability - Abandoned Calls")
            st.write("Chance of calling back following an unsuccessful call ?")
            pub_cb_abd = st.slider(
                                    "Callback probability - abandoned calls",
                                    min_value=0,    # float
                                    max_value=100,    # float
                                    value=round(g.call_back_prob_abd*100),       # float
                                    step=1         # float
                )/100

        with subcol2:
            st.subheader("")

        with subcol3:
            st.subheader("Professional Callers")
                
        #    st.text("Talk Time")
        #    st.write("How long will calls last ?")
        #    pub_call_len = st.slider("Prof Call Length (minutes)",min_value=0,max_value=60,value=1)   

            st.markdown("##### Write Up Time") 
            st.write("How much time is spent on post-call admin ?")
            pub_work_len = st.slider("Prof Work Length (minutes)",min_value=0,max_value=60,value=g.mean_prof_work)

            st.write(" ")
            st.divider() 

            st.markdown("##### Call Back Probability - Handled Calls")
            st.write("Chance of calling back following a successful call ?")
            pub_cb_han = st.slider("Prof Call Back Probability Handled",min_value=0,max_value=100,value=1,step=1)

            st.write(" ")
            st.divider() 

            st.markdown("##### Call Back Probability - Abandoned Calls")
            st.write("Chance of calling back following an unsuccessful call ?")
            pub_cb_abd = st.slider("Prof Call Back Probability Abd",min_value=0,max_value=100,value=1,step=1) / 100


        st.divider()
        st.markdown("## Other Variable")
        

        ## description of the tab and how to use it
        st.subheader("Other Variables")
        st.write("Use this page to change other model variables")

        st.markdown("##### No. Runs")
        st.write("How many times will you loop through the model ?")
        no_runs = st.slider("Number of model runs",min_value=0,max_value=100,value=40)   

        st.write(" ")
        st.divider()

        st.markdown("##### Demand Variance")
        st.write("Adjusting the standard deviation for the demand distribution calculation can add more 'randomness' to then levels of demand")
        st.write("A higher value will increase the variance in the number of calls per hour")
        st.write("")
        public_var = st.slider("Public Demand St Dev",min_value=0,max_value=30,value=g.public_arr_sd) 
        public_var = st.slider("Professional Demand St Dev",min_value=0,max_value=30,value=g.public_arr_sd) 



        st.markdown("#### Run the model ")

        st.header("Run")
        st.write("Use the button below to run the model")
        run_model = st.button("Run Model")

        if run_model:
            with st.spinner('Simulating the call centre...'):
            
            #Collect data from each of the dataframes

            #Public Call Demand Data
                transformed_data = [
                {"t": row["Hour"] * 60, "mean_iat": 60 / row["Average Calls"]}
                for _, row in edited_public_df.iterrows() ]
                public_demand_df = pd.DataFrame(transformed_data)

            #Professuional Call Demand Data   
                transformed_prof = [
                {"t": row["Hour"] * 60, "mean_iat": 60 / row["Average Calls"]}
                for _, row in edited_prof_df.iterrows() ]
                prof_demand_df = pd.DataFrame(transformed_prof)



            #Staffing Data    








            



            #Update g class variables
            
                g.number_of_runs = no_runs




















                results_df = Trial(public_demand_df,prof_demand_df).run_trial()          



                results_agg = results_df.groupby(['Run', 'Call Type', 'Call Hour']).agg(
                                    Count=('Run', 'size'),
                                    Avg_Queue_Time=('Queue Time', 'mean'),
                                    Avg_Talk_Time=('Talk Time', 'mean'),
                                    Avg_Work_Time=('Work Time', 'mean'),
                                    Tot_Esc = ('Escalated', 'sum'),
                                    Tot_Abd = ('Hang Up', 'sum')                               
                                    ).reset_index()
                
                results_agg['Abd Rate'] = results_agg['Tot_Abd'] / results_agg['Count'] 

                results_tot = results_agg.groupby(['Call Type','Call Hour']).agg(
                                    Calls_min = ('Count','min'),
                                    Calls_max = ('Count','max'),
                                    Calls_Av = ('Count','mean'),       
                                    AvQ_min = ('Avg_Queue_Time','min'),
                                    AvQ_max = ('Avg_Queue_Time','max'),
                                    AvQ_Av = ('Avg_Queue_Time','mean'),       
                                    Talk_min = ('Avg_Talk_Time','min'),
                                    Talk_max = ('Avg_Talk_Time','max'),
                                    Talk_Av = ('Avg_Talk_Time','mean'),       
                                    Abd_min = ('Abd Rate','min'),
                                    Abd_max = ('Abd Rate','max'),
                                    Abd_Av = ('Abd Rate','mean'),                                
                                    Work_min = ('Avg_Work_Time','min'),
                                    Work_max = ('Avg_Work_Time','max'),
                                    Work_Av = ('Avg_Work_Time','mean'),                                
                                    Esc_min = ('Tot_Esc','min'),
                                    Esc_max = ('Tot_Esc','max'),
                                    Esc_Av = ('Tot_Esc','mean')                                
                                    ).reset_index()

                print_df = results_df.groupby('Run').agg(calls=('Run','size'),
                                                        total_hang_up=('Hang Up','sum'))

                print_df['abd_rate'] =   (print_df['total_hang_up'] / print_df['calls']) * 100    


                df = results_tot
            
                df = df[df['Call Type']=='Public']

                col1, col2 = st.columns(2)


                with col1:
                    plt.plot(df['Call Hour'].values,df['Calls_Av'].values)       
                    x = df['Call Hour'].values
                    y1 = df['Calls_min'].values
                    y2 = df['Calls_max'].values
                    y3 = df['Calls_Av'].values

                # Plot the two lines
                    plt.plot(x, y1, label='min', color='blue')
                    plt.plot(x, y2, label='max', color='blue')
                    plt.plot(x, y3, label='Average')
                    plt.xlim(0, 23) 

                # Fill the area between the two lines
                    plt.fill_between(x, y1, y2, color='blue', alpha=0.2)

                # Adding labels and title
                    plt.xlabel('Hour')
                    plt.ylabel('No. Calls')
                    plt.title('Public Call Volumes')
                    plt.legend()
                    plt.ylim(0)
                # Display the plot
                    st.pyplot(plt)


                st.dataframe(print_df)    


































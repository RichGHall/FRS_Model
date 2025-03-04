import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from FRS_Suffolk_Model import Trial

st.set_page_config(layout="wide")
st.title('111 Mental Health (Option 2) Call Centre Discrete Event Simulation Model')
st.write('This is some blurb describing the model')

tab0, tab1, tab2, tab3, tab4 = st.tabs(["About", "1, Demand", "2, Staffing", "3, Other Variables", "4, Run"])

with tab0:
    st.header("Introduction")
    st.write("This model is designed to simulate the operation of a mental health call centre.")
    st.write("The model is based on the following assumptions:")

with tab1:
    st.header("Demand Details")
    st.write("Use the grid below to update the expected number of calls per hour")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Public Callers")
        public_df = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Public_Av_Calls.csv")
        edited_public_df = st.data_editor(public_df)
        public_updated = st.button("Update Public Calls")

with tab4:
    st.header("Run")
    st.write("Use the button below to run the model")
    run_model = st.button("Run Model")
    if run_model:
        with st.spinner('Simulating the call centre...'):
            trial = Trial()
            results_df = trial.run_trial(edited_public_df)  # Pass the DataFrame to the trial
            results_agg = results_df.groupby(['Run', 'Call Type', 'Call Hour']).agg(
                Count=('Run', 'size'),
                Avg_Queue_Time=('Queue Time', 'mean'),
                Avg_Talk_Time=('Talk Time', 'mean'),
                Avg_Work_Time=('Work Time', 'mean'),
                Tot_Esc=('Escalated', 'sum'),
                Tot_Abd=('Hang Up', 'sum')
            ).reset_index()
            results_agg['Abd Rate'] = results_agg['Tot_Abd'] / results_agg['Count']
            results_tot = results_agg.groupby(['Call Type', 'Call Hour']).agg(
                Calls_min=('Count', 'min'),
                Calls_max=('Count', 'max'),
                Calls_Av=('Count', 'mean'),
                AvQ_min=('Avg_Queue_Time', 'min'),
                AvQ_max=('Avg_Queue_Time', 'max'),
                AvQ_Av=('Avg_Queue_Time', 'mean'),
                Talk_min=('Avg_Talk_Time', 'min'),
                Talk_max=('Avg_Talk_Time', 'max'),
                Talk_Av=('Avg_Talk_Time', 'mean'),
                Abd_min=('Abd Rate', 'min'),
                Abd_max=('Abd Rate', 'max'),
                Abd_Av=('Abd Rate', 'mean'),
                Work_min=('Avg_Work_Time', 'min'),
                Work_max=('Avg_Work_Time', 'max'),
                Work_Av=('Avg_Work_Time', 'mean'),
                Esc_min=('Tot_Esc', 'min'),
                Esc_max=('Tot_Esc', 'max'),
                Esc_Av=('Tot_Esc', 'mean')
            ).reset_index()
            print_df = results_df.groupby('Run').agg(
                calls=('Run', 'size'),
                total_hang_up=('Hang Up', 'sum')
            )
            print_df['abd_rate'] = (print_df['total_hang_up'] / print_df['calls']) * 100

            df = results_tot
            df = df[df['Call Type'] == 'Public']
            col1, col2 = st.columns(2)
            with col1:
                plt.plot(df['Call Hour'].values, df['Calls_Av'].values)
                x = df['Call Hour'].values
                y1 = df['Calls_min'].values
                y2 = df['Calls_max'].values
                y3 = df['Calls_Av'].values
                plt.plot(x, y1, label='min', color='blue')
                plt.plot(x, y2, label='max', color='blue')
                plt.plot(x, y3, label='Average')
                plt.xlim(0, 23)
                plt.fill_between(x, y1, y2, color='blue', alpha=0.2)
                plt.xlabel('Hour')
                plt.ylabel('No. Calls')
                plt.title('Public Call Volumes')
                plt.legend()
                plt.ylim(0)
                st.pyplot(plt)

            with col2:
                df_prof = results_tot[results_tot['Call Type'] == 'Prof']
                fig = plt.plot(df_prof['Call Hour'].values, df_prof['Calls_Av'].values)
                xp = df_prof['Call Hour'].values
                yp1 = df_prof['Calls_min'].values
                yp2 = df_prof['Calls_max'].values
                yp3 = df_prof['Calls_Av'].values
                plt.plot(xp, yp1, label='min', color='blue')
                plt.plot(xp, yp2, label='max', color='blue')
                plt.plot(xp, yp3, label='Average')
                plt.xlim(0, 23)
                plt.fill_between(xp, yp1, yp2, color='blue', alpha=0.2)
                plt.xlabel('Hour')
                plt.ylabel('No. Calls')
                plt.title('Professional Call Volumes')
                plt.legend()
                plt.ylim(0)
                st.pyplot(fig)

            st.dataframe(print_df)

with tab2:
    st.header("Staffing Details")
    st.write("Use the grid below to update the expected staffing levels for each hour")

with tab3:
    st.header("Other Variables")
    st.write("Use this page to change other model variables, such as call length, work time, break time, etc.")
    st.subheader("No. Runs")
    st.write("How many times will you loop through the model?")
    no_runs = st.slider("Number of model runs", min_value=0, max_value=500, value=1)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Public Callers")
        st.text("Talk Time")
        st.write("How long will calls last?")
        pub_call_len = st.slider("Public Call Length (minutes)", min_value=0, max_value=60, value=1)
        st.text("Write Up Time")
        st.write("How much time is spent on post-call admin?")
        pub_work_len = st.slider("Public Work Length (minutes)", min_value=0, max_value=60, value=1)
        st.text("Call Back Probability - Handled Calls")
        st.write("Chance of calling back following a successful call?")
        pub_cb_han = st.slider(
            "Public Call Back Probability Handled",
            min_value=0.0,
            max_value=1.0,
            value=0.01,
            step=0.01
        )
        st.text("Call Back Probability - Abandoned Calls")
        st.write("Chance of calling back following an unsuccessful call?")
        pub_cb_abd = st.slider(
            "Public Call Back Probability Abandoned",
            min_value=0.0,
            max_value=1.0,
            value=0.01,
            step=0.01
        )

    with col2:
        st.write(" ")

    with col3:
        st.subheader("Professional Callers")
        st.text("Talk Time")
        st.write("How long will calls last?")
        prof_call_len = st.slider("Prof Call Length (minutes)", min_value=0, max_value=60, value=1)
        st.text("Write Up Time")
        st.write("How much time is spent on post-call admin?")
        prof_work_len = st.slider("Prof Work Length (minutes)", min_value=0, max_value=60, value=1)
        st.text("Call Back Probability - Handled Calls")
        st.write("Chance of calling back following a successful call?")
        # prof_cb_han = st.slider("Prof Call Back Probability Handled", min_value=0, max_value=1, value=0.01, step=0.01)
        st.text("Call Back Probability - Abandoned Calls")
        st.write("Chance of calling back following an unsuccessful call?")
        # prof_cb_abd = st.slider("Prof Call Back Probability Abd", min_value=0, max_value=1, value=0.01, step=0.01)
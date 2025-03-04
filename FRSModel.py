

#######################################################################
# To Do: 
#        - recalculate distinct callers per hour/day
#        - calculate call back  delays / probabilities
#        - professional caller    
#
######################################################################


import simpy
import random
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from sim_tools.time_dependent import NSPPThinning
from scipy.stats import lognorm
from scipy.stats import erlang

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
#############
#    MODEL SETUP 
#############


## Lognormal classs, used to calculate distribution 
class Lognormal:
        """
        Encapsulates a lognormal distirbution
        """
        def __init__(self, mean, stdev, random_seed=None):
            """
            Params:
            -------
            mean = mean of the lognormal distribution
            stdev = standard dev of the lognormal distribution
            """
            self.rand = np.random.default_rng(seed=random_seed)
            mu, sigma = self.normal_moments_from_lognormal(mean, stdev**2)
            self.mu = mu
            self.sigma = sigma

        def normal_moments_from_lognormal(self, m, v):
            '''
            Returns mu and sigma of normal distribution
            underlying a lognormal with mean m and variance v
            source: https://blogs.sas.com/content/iml/2014/06/04/simulate-lognormal
            -data-with-specified-mean-and-variance.html

            Params:
            -------
            m = mean of lognormal distribution
            v = variance of lognormal distribution

            Returns:
            -------
            (float, float)
            '''
            phi = math.sqrt(v + m**2)
            mu = math.log(m**2/phi)
            sigma = math.sqrt(math.log(phi**2/m**2))
            return mu, sigma

        def sample(self):
            """
            Sample from the normal distribution
            """
            return self.rand.lognormal(self.mu, self.sigma)        

class Erglang_dist: 
        def __init__(self, mu, sigma, random_seed=None):
            self.mu = mu   # 52 Mean call length
            self.sigma = sigma      # 8 Standard deviation

        def ErlangRes(self, mu, sigma):
        #Generates an erlang distribution

            random_seed = np.random.default_rng(seed=random_seed)

            # Compute shape and scale parameters
            k = int(mu**2 / sigma**2)  # Shape parameter (integer)
            theta = (sigma**2) / mu  # Scale parameter
        
            e = self.erlang.rvs(self.k, self.theta,random_seed)
            return  self.e


# Class to store global parameter values used in the model
class g:

    ## load csv files required for the model

    arrivals_public_df = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Public_IAT.csv")   
    arrivals_prof_df = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Prof_IAT.csv")  

    senior_resources_df = pd.read_csv("https://raw.githubusercontent.com/RichGHall/FRS_Model/main/files/Senior_Resources.csv")


    #load csv dataframes into new df 
    arrivals_public_time_dep_df = arrivals_public_df
    arrivals_prof_time_dep_df = arrivals_prof_df  
       
    #talk times   
    public_talk_shape = 0.8562401523401358
    public_talk_rate = 0.08372673973690065

    prof_talk_shape  = 1.2808212740988951 
    prof_talk_rate = 0.26374347311137214

    mean_public_work = 30       #average work time for public calls
    mean_prof_work = 45         #average work time for professional calls
    
    sd_public_work = 22         #standard deviation, public calls for lognormal dist
    sd_prof_work = 17           #standard deviation, prof calls for lognormal dist

    public_work_shape = 1.3395242423304587
    public_work_rate = 0.07315229368821419    

    number_of_junior = 1        #number of junior staff
    number_of_senior = 3        #number of senior staff

    prob_escalation = 0.40      #probability of a call requiring escalation/call back

    sim_duration = 2880         #duration of simulation in mins (2 x 24hrs)
    number_of_runs = 40         #number of runs of each simulation 

    public_patience = 5         #level of patience (ie how long before they hang up) for public calls
    public_pat_sd = 2           #SD of public patience 

    prof_patience = 3           #level of patience (ie how long before they hang up) for prof calls
    prof_pat_sd =  1            #SD of public patience 

    junior_staff = False       #switch for including the junior call handling process

    prob_break = 0.25      #probability that the call handler will go on a break next
    mean_break = 27            #average break time
    sd_break = 10              #break time standard deviation 

    call_back_prob_handled = 0.305   #probability of a call back if the call was handled 
    call_back_prob_abd = 0.523       #probability of a call back if the call was abandoned

    call_back_prob_handled_prof = 0.104   #probability of a call back if the call was handled 
    call_back_prob_abd_prof = 0.264       #probability of a call back if the call was abandoned

    cb_len_handled_pub = 52
    cb_sd_handled_pub = 40

    cb_len_abd_pub = 7.36
    cb_sd_abd_pub = 6.71
    
    cb_len_handled_prof = 91
    cb_sd_handled_prof = 89
    cb_len_abd_prof = 8.57
    cb_sd_abd_prof = 11.826
   




# Class representing public callers to the FRS Service.  There are public callers (members of the general public) and professional callers (GPs, Ambulance, Police etc) in Norfolk these are handled differently.
# each caller will be allocated a 'patience' level (ie how many minutes before they hang up) a priority (based on their call type) and a liklehood of neediing escalation

class Public_Caller: 
    def __init__(self, c_id, priority, call_type):
        self.id = c_id
        self.priority = priority
        self.cal_type = call_type 
        self.escalated = False  # New attribute to track if a call is escalated
        self.queue_entry_time = None  # Time the call was placed in the queue
        self.patience = 0


    def __lt__(self, other):
        """This method is required by PriorityStore to compare priorities."""
        return self.priority < other.priority

    def __repr__(self):
        return f"Public_Caller(priority={self.priority}, caller_id={self.id}, call_type={self.cal_type})"

# Class representing professional callers to the FRS Service
class Prof_Caller: 
    def __init__(self, c_id, priority, call_type):
        self.id = c_id
        self.priority = priority
        self.cal_type = call_type 
        self.escalated = False  # New attribute to track if a call is escalated
        self.queue_entry_time = None  # Time the call was placed in the queue
        self.patience = 0

    def __lt__(self, other):
        """This method is required by PriorityStore to compare priorities."""
        return self.priority < other.priority

    def __repr__(self):
        return f"Prof_Caller(priority={self.priority}, caller_id={self.id}, call_type={self.cal_type})"

# Class representing the simulation model
class Model:
    def __init__(self, run_number,df_public_demand):
        self.env = simpy.Environment()
        self.public_counter = 0
        self.prof_counter = 0
        
        self.public_arr_log = 0.0
        self.public_arr_sd = 1

        self.prof_arr_log = 0.0


        self.call_queue = simpy.PriorityStore(self.env) 
        self.juniors = simpy.Resource(self.env, capacity=g.number_of_junior)
        self.seniors = simpy.Resource(self.env, capacity=g.number_of_senior)
        self.public_demand = df_public_demand

        self.run_number = run_number

        # DataFrame to store call details
        self.results_df = pd.DataFrame(columns=[
                    "Run" , 
                    "Caller ID", 
                    "Call Type", 
                    "Call Start Time", 
                    "Queue Time", 
                    "Handled By", 
                    "Talk Start Time",
                    "Talk Time", 
                    "Escalated" , 
                    "End Time"  ,
                    "Work Time"  ,
                    "Hang Up"  ,
                    "Call Hour" 
                ])
                
                
        self.results_df = self.results_df.astype({
                    "Run" : 'int64', 
                    "Caller ID" : 'int64', 
                    "Call Type" : 'string', 
                    "Call Start Time" : 'float64', 
                    "Queue Time" : 'float64', 
                    "Handled By" : 'string', 
                    "Talk Start Time" : 'float64',
                    "Talk Time" : 'float64', 
                    "Escalated" : 'float64', 
                    "End Time" : 'float64',
                    "Work Time" : 'float64',
                    "Hang Up" : 'float64',
                    "Call Hour" : 'int64'         
                })
 
        self.results_agg = pd.DataFrame()
        self.results_agg["Run"] = [1]
        self.results_agg["Hour"] = [0.0]
        self.results_agg["Type"] = [0.0]
        self.results_agg["Call_Count"] = [0.0]
        self.results_agg["Av Queue"] = [0.0]
        self.results_agg["Av Talk"] = [0.0]
        self.results_agg["Av Work"] = [0.0]
        self.results_agg["Abd Rate"] = [0.0]

        self.results_tot = pd.DataFrame(columns=[
                    
                    "Hour",
                    "Type",

                    "Calls_min",
                    "Calls_max",
                    "Calls_Av",

                    "AvQ_min",
                    "AvQ_max",
                    "AvQ_Av",

                    "Talk_min",
                    "Talk_max",
                    "Talk_Av",

                    "Abd_min",
                    "Abd_max",
                    "Abd_Av",

                    "Work_min",
                    "Work_max",
                    "Work_Av"
                        ]  )



    def adjust_df(self,df_public_demand):
        
        self.df_public_demand = df_public_demand







    
    ## This function runs every hour and adjusts the level of resourcing and arrivals rates.
    ## It calculates the current hour by rounding down self.env.now, calculates the rates for that hour and then waits for another 60 minutes
    def adjust_senior_resources(self,df_public_demand):
        
        self.df_public_demand = df_public_demand 
        
        while True:
            
            if self.env.now > 1439:
                curr_hour = (int(self.env.now // 60) * 60)-1440
            else:    
                curr_hour = int(self.env.now // 60) * 60
            
            current_seniors = g.senior_resources_df.loc[g.arrivals_prof_df['t']==curr_hour, 'res'].iloc[0]            
            self.seniors = simpy.Resource(self.env, capacity=current_seniors)

            
            self.public_arr_log = g.arrivals_public_df.loc[g.arrivals_public_df['t']==curr_hour, 'mean_iat'].iloc[0]
            #self.public_arr_log = self.df_public_demand.loc[self.df_public_demand['t']==curr_hour, 'mean_iat'].iloc[0]
                       
            self.prof_arr_log = g.arrivals_prof_df.loc[g.arrivals_prof_df['t']==curr_hour, 'mean_iat'].iloc[0]

            
            yield self.env.timeout(60)  # Wait until the next hour

    # Generator for public calls
    def generator_public_calls(self):
        while True:
            self.public_counter += 1
            call = Public_Caller(self.public_counter, 1, 'Public')
            call.queue_entry_time = self.env.now  # Track when the call enters the queue

            sampled_inter = Lognormal(self.public_arr_log,1).sample()
                       
            call.patience = Lognormal(g.public_patience,g.public_pat_sd).sample()
            
            yield self.call_queue.put(call)
            yield self.env.timeout(sampled_inter)





    # Generator for professional calls
    def generator_prof_calls(self):
        while True:
            self.prof_counter += 1
            call = Prof_Caller(self.prof_counter, 0, 'Prof')
            call.queue_entry_time = self.env.now  # Track when the call enters the queue

            if self.env.now > 1440: 
#                sampled_inter = self.arrivals_prof_dist.sample(simulation_time=self.env.now-1440)
                sampled_inter = Lognormal(self.prof_arr_log,0.2).sample()   
            else:
#                sampled_inter = self.arrivals_prof_dist.sample(simulation_time=self.env.now)         
                sampled_inter = Lognormal(self.prof_arr_log,0.2).sample()   

            call.patience = random.expovariate(1 / g.prof_patience)

            yield self.call_queue.put(call)
            yield self.env.timeout(sampled_inter)


    # Method to handle calls by Seniors
    def handle_calls_senior(self):
        while True:
            call = yield self.call_queue.get()
            
            current_time = self.env.now

            if current_time - call.queue_entry_time > call.patience: 
                call_start_time = call.queue_entry_time
                talk_start_time = 0
                talk_Time = 0
                queue_time = call.patience 

                self.update_results(call,call_start_time,queue_time,call_start_time + queue_time,
                                                "None",0,0,0,call_start_time + queue_time,1)

                self.ring_back(call,0,call.cal_type)     #call the ring back process for abd calls


                continue    

            if call.cal_type == 'Prof' or call.priority == 1:
                #Add call start time to a variable 
                call_start_time = call.queue_entry_time

                #Add the talk start time to a variable
                talk_start_time = self.env.now

                #calculate the queue time
                queue_time = self.env.now - call_start_time  # Calculate queue time
                               

                # Simulate talk time for senior handling
                if call.cal_type == 'Prof':
                    talk_time = erlang.rvs(g.prof_talk_shape, g.prof_talk_rate)
                    work_time = random.expovariate(1/g.mean_prof_work)
                
                
                else:
                    talk_time = erlang.rvs(g.public_talk_shape, g.public_talk_rate) 
                    #work_time = erlang.rvs(g.public_work_shape, g.public_work_rate) 
                   
                   
                    work_time = Lognormal(g.mean_public_work,g.sd_public_work).sample() +5
                    
                                            
                                
                yield self.env.timeout(talk_time)
                

                self.ring_back(call,1,call.cal_type)   #call the ring back process for handled calls


                  ## update_results(self, call, call_start_time, queue_time,
                #                 talk_start_time, handled_by, talk_time, escalated,work_time)
                                                                                             
                self.update_results(call, call_start_time, queue_time,
                                    talk_start_time,'Senior', talk_time, 0,
                                    work_time,self.env.now,0)

                yield self.env.timeout(work_time)

                ## based on the data some  handlers will become unavailable for some reason,
                ## such as a break, lunch etc.  The following step replicates this in two parts,
                ## firstly, the probability they will become unavailable and secondly the length of time 
                ## they are away from the phone

                




                if random.uniform(0,1) < g.prob_break: 
                    break_time = Lognormal(g.mean_break,g.sd_break).sample()
                    yield self.env.timeout(break_time)
                


    def ring_back(self,call,handled,type):
        
        if handled == 1:   #Call handled 
            if random.uniform(0,1) < g.call_back_prob_handled:
            
                if type == 'Public':  #Public Caller
                    yield erlang.rvs(g.cb_len_handled_pub, g.cb_sd_handled_pub) 
                    yield self.call_queue.put(call)
                else:                 #ProfessionalCaller
                    yield erlang.rvs(g.cb_len_handled_prof, g.cb_sd_handled_prof) 
                    yield self.call_queue.put(call)
                            
        else:              #Call abandoned
                if type == 'Public':  #Public Caller
                    yield erlang.rvs(g.cb_len_abd_pub, g.cb_sd_abd_pub) 
                    yield self.call_queue.put(call)
                else:                 #ProfessionalCaller
                    yield erlang.rvs(g.cb_len_abd_prof, g.cb_sd_abd_prof) 
                    yield self.call_queue.put(call)    
    

        # Method to update the results DataFrame
    def update_results(self, call, call_start_time, queue_time,talk_start_time, 
                        handled_by, talk_time, escalated,work_time,end_time,hangup):
        

        if self.env.now >= 1440:

            new_row = {

                "Run": self.run_number, 
                "Caller ID": call.id,
                "Call Type": call.cal_type, 
                "Call Start Time": (call_start_time/24/60), 
                "Queue Time": queue_time,
                "Handled By": handled_by,
                "Talk Start Time": (talk_start_time/24/60),
                "Talk Time": talk_time, 
                "Escalated": escalated, 
                "End Time": end_time/24/60,
                "Work Time": work_time,
                "Hang Up": hangup,
                "Call Hour": math.floor((end_time - 1440)/60) 

                }

            # Use pd.concat to add the new row to the DataFrame
            self.results_df = pd.concat([self.results_df, pd.DataFrame([new_row])], ignore_index=True)

# Class representing a trial for our simulation
class Trial:
    def __init__(self):
        self.results_df = pd.DataFrame()
        self.results_agg = pd.DataFrame()
        self.results_agg["Run"] = [1]
        self.results_agg["Hour"] = [0.0]
        self.results_agg["Type"] = [0.0]
        self.results_agg["Call_Count"] = [0.0]
        self.results_agg["Av Queue"] = [0.0]
        self.results_agg["Av Talk"] = [0.0]
        self.results_agg["Av Work"] = [0.0]
        self.results_agg["Abandoned"] = [0.0]
        self.results_agg["Escalated"] = [0.0]
        self.results_agg["Abd Rate"] = [0.0]

        self.results_tot = pd.DataFrame()
        self.results_tot["Hour"] = [0]
        self.results_tot["Type"] = [0]
        self.results_tot["Calls_min"] = [0]
        self.results_tot["Calls_max"] = [0]
        self.results_tot["Calls_Av"] = [0]
        self.results_tot["AvQ_min"] = [0]
        self.results_tot["AvQ_max"] = [0]
        self.results_tot["AvQ_Av"] = [0]
        self.results_tot["Talk_min"] = [0]
        self.results_tot["Talk_max"] = [0]
        self.results_tot["Talk_Av"] = [0]
        self.results_tot["Abd_min"] = [0]
        self.results_tot["Abd_max"] = [0]
        self.results_tot["Abd_Av"] = [0]
        self.results_tot["Work_min"] = [0]
        self.results_tot["Work_max"] = [0]
        self.results_tot["Work_Av"] = [0]
        self.results_tot["Esc_min"] = [0]
        self.results_tot["Esc_max"] = [0]
        self.results_tot["Esc_Av"] = [0]  
 



    #Method to calculate and store the means accross the runs
 
    def run_trial(self):       
        
        for run in range(1, g.number_of_runs + 1):
            model = Model(run)

            # for _ in range(g.number_of_junior):
            #    model.env.process(model.handle_calls_junior())
            
            for _ in range(g.number_of_senior):
                model.env.process(model.handle_calls_senior())

            model.env.process(model.adjust_senior_resources())
            
            model.env.process(model.generator_public_calls())
            model.env.process(model.generator_prof_calls())
            model.env.run(until=g.sim_duration)
            self.results_df = pd.concat([self.results_df, model.results_df])



        return self.results_df
    

# Run the trial
#Trial().run_trial()
#print('model run complete')
#df = Trial().results_tot 



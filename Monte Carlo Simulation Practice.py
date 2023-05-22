#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np
import seaborn as sns
sns.set_style('whitegrid')

#One approach that can produce a better understanding of the range of potential outcomes and help avoid the “flaw of averages” is a Monte Carlo simulation.


# We will try to predict how much money we should budget for sales commissions for the next year. This problem is useful for modeling because we have a defined formula for calculating commissions and we likely have some experience with prior years’ commissions payments.
# 
# This problem is also important from a business perspective. Sales commissions can be a large selling expense and it is important to plan appropriately for this expense. In addition, the use of a Monte Carlo simulation is a relatively simple improvement that can be made to augment what is normally an unsophisticated estimation process.

# There are two components to running a Monte Carlo simulation:
# 
# 1. the equation to evaluate
# 2. the random variables for the input

# Because we have paid out commissions for several years, we can look at a typical historical distribution of percent to target:
# 
# 
# This distribution looks like a normal distribution with a mean of 100% and standard deviation of 10%. This insight is useful because we can model our input variable distribution so that it is similar to our real world experience.
# 
# 

# In[6]:


#As described above, 
#we know that our historical percent to target performance is centered 
#around a a mean of 100% and standard deviation of 10%. Let’s define those variables 
#as well as the number of sales reps and simulations we are modeling:

avg = 1
std_dev = .1
num_reps = 500
num_simulations = 1000


# In[7]:


#Now we can use numpy to generate a list of percentages that will replicate our historical normal distribution:
pct_to_target = np.random.normal(avg, std_dev, num_reps).round(2)

#This is definitely not a normal distribution. This distribution shows us that sales targets are set into 1 of 6 buckets and the frequency gets lower as the amount increases. This distribution could be indicative of a very simple target setting process where individuals are bucketed into certain groups and given targets consistently based on their tenure, territory size or sales pipeline.


# In[8]:


#For the sake of this example, we will use a uniform distribution but assign lower probability rates for some of the values.
sales_target_values = [75_000, 100_000, 200_000, 300_000, 400_000, 500_000]
sales_target_prob = [.3, .3, .2, .1, .05, .05]
sales_target = np.random.choice(sales_target_values, num_reps, p=sales_target_prob)


# In[9]:


#Now that we know how to create our two input distributions, let’s build up a pandas dataframe:

df = pd.DataFrame(index=range(num_reps), data={'Pct_To_Target': pct_to_target,
                                               'Sales_Target': sales_target})

df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']


# In[10]:


#The final piece of code we need to create is a way to map our Pct_To_Target to the commission rate. Here is the function:

def calc_commission_rate(x):
    """ Return the commission rate based on the table:
    0-90% = 2%
    91-99% = 3%
    >= 100 = 4%
    """
    if x <= .90:
        return .02
    if x <= .99:
        return .03
    else:
        return .04


# In[11]:


#Now we create our commission rate and multiply it times sales:
df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission_rate)
df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']


# In[12]:


# Define a list to keep all the results from each simulation that we want to analyze
all_stats = []

# Loop through many simulations
for i in range(num_simulations):

    # Choose random inputs for the sales targets and percent to target
    sales_target = np.random.choice(sales_target_values, num_reps, p=sales_target_prob)
    pct_to_target = np.random.normal(avg, std_dev, num_reps).round(2)

    # Build the dataframe based on the inputs and number of reps
    df = pd.DataFrame(index=range(num_reps), data={'Pct_To_Target': pct_to_target,
                                                   'Sales_Target': sales_target})

    # Back into the sales number using the percent to target rate
    df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']

    # Determine the commissions rate and calculate it
    df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission_rate)
    df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']

    # We want to track sales,commission amounts and sales targets over all the simulations
    all_stats.append([df['Sales'].sum().round(0),
                      df['Commission_Amount'].sum().round(0),
                      df['Sales_Target'].sum().round(0)])


# In[13]:


#In order to analyze the results of the simulation, I will build a dataframe from all_stats :

results_df = pd.DataFrame.from_records(all_stats, columns=['Sales',
                                                           'Commission_Amount',
                                                           'Sales_Target'])


# In[14]:


results_df.describe().style.format('{:,}')


# What can we observe from this monte carlo simulation?
# 
# Average of 2,864,009.04 USD for Commission Amount
# 
# Standard Deviation of 101,378.21 USD

# In[ ]:





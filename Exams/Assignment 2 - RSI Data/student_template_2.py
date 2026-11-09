"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""
from turtle import done

import numpy as np
import pandas as pd
from os import path
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel,ttest_ind, norm, chisquare
import scipy.stats as stats

def pairedttest(filepath):  #Task 1
    """
    Prompt:
    From a dataset of RSI values in csv file conduct a paired t-test comparing all the force plate and accelerometer RSI values.  
    Print the T-value, P values, the Null and Alternative hypothesis and show if the Null can be rejeceted or not.

    This method loads in a data from a csv file.  Conducts a paired t-test on the force plate and accelerometer data.  Prints the required values above
    and shows whether the null hypothesis is rejected or not.

    :param filepath:  A filepath to the RSI data used in this function
    :return NONE: Nothing is returned only printed from these functions
    """
    data = np.loadtxt(filepath, delimiter=',', skiprows=1, usecols=(1,2,3))  #Loading Data into Text skipping the first row and only using the columns with floating values
    force_plate = data[:,0]     #Getting the force plate data from the first column of data
    accelerometer = data[:,1]   #Getting the accelerometer data from the second column                

    alpha = 0.05 #Given Alpha 

    ttest, pvalue = ttest_rel(force_plate, accelerometer, alternative='two-sided')  #Running the TTest with the alternative hypothesis that the means are unequal

    print(f"The Null hypothesis is that the force plate data's mean and the accelerometers data's mean are the same")
    print(f"The Alternative hypothesis is that the force plate datas mean and the accelerometers mean are different")

    print(f"The T-value is {ttest:.5f}")
    print(f"The P-value is {pvalue:.5f}")

    if (pvalue <= alpha):  #Null hypothesis check
        print("The Null Hypothesis is Rejected")
    else:
        print("Null Hypothesis is failed to be Rejected")

def accelerometertesting(filepath):
    """
    Prompt:
    From a dataset of RSI values in csv file.  Fit a normal distribution and conduct a Chi2 Goodness of Fit Test on the RSI values gathered from the accelerometer.
    Print out the Chi2 stat, p-value, and an indication of if it is a good fit or not.  Also plot a histogram of the accelerometer data with the normal distrubtion curve 
    overlaid.  Label and note the histogram accordingly.

    This method loads the csv data.  Fits the accelerometers data to a normal distribution.  conducts a Chi2 goodness of fit test.  
    And plots a histogram of the data.  Prints all requried information noted above.

    :param filepath:  A filepath to the RSI data used in this function
    :return NONE: Nothing is returned only printed from these functions
    """
    data = np.loadtxt(filepath, delimiter=',', skiprows=1, usecols=(1,2))  #Loading Data into Text skipping the first row and only using the columns with floating values
    accelerometer = data[:,1]   #Getting the accelerometer data from the second column   

    #Fit the data onto a normal Fit
    mu, std = norm.fit(accelerometer)  #finding the normal fits mean and standard deviation for the data
    print(f"Fitted mean: {mu:.4f}, std: {std:.4f}") #Print the Mean and STD for reference

    #Defining the Bins Observed Counts and Expected Counts from the data
    #Copied from HW 5.4.2
    #creates the necessary input data for the Chisquare function
    #Dont need to recreate the function when it can be copied from a previosuly wokring exmaple
    #inputs are changed to match the names above
    bins = np.r_[-np.inf, np.linspace(mu - 2 * std, mu + 2 * std, 9), np.inf]
    observed_counts, _ = np.histogram(accelerometer, bins=bins, density=False)
    expected_prob = np.diff(norm.cdf(bins, loc=mu, scale=std))
    expected_counts = expected_prob * len(accelerometer)

    #Copied from HW 5.4.2
    #Chi2 goodness of fit test. Degree of freedom is 2.
    chi2_stat, p_value = chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2)
    
    alpha = 0.05 #Given Alpha to compare to

    #Printing required information noted above
    print(f"Chi2 statistic: {chi2_stat:.4f}")
    print(f"p-value: {p_value:.4f}")

    if p_value > alpha:  #Comparing Null hypothesis versus Alternative
        print("Data is a Good fit: Null hypothesis is not rejected")
    else:
        print("Data is not a good fit: Null hypothesis is rejected")


    #Plotting the data on a histogram, taking the bins from above along with the other values needed
    x = np.linspace(accelerometer.min(), accelerometer.max(), 300)
    plt.hist(accelerometer, bins=8, density=True, alpha=0.6, edgecolor="black", label="Accelerometer RSI")
    plt.plot(x, norm.pdf(x, mu, std), "r-", linewidth=2, label=f"Normal fit (μ={mu:.2f}, σ={std:.2f})")
    plt.xlabel("RSI")
    plt.ylabel("Probability density")
    plt.title("Accelerometer RSI with Fitted Normal Distribution")
    plt.legend()
    plt.show()


def ParticipantFtrials(filepath):
    """
    Prompt: From the force plate and accelerometer-based RSI data for all participants,
    create and print() a dataframe containing only the trials from Participant F. 
    Calculate the 95% confidence intervals for Participant Fs RSI for both the force plate and accelerometer measurements. 

    This method reads the csv data into a dataframe selects only the data from particpant F.  calculatges the confidnce interval of both the RSI and Force Plate data
    and prints out the required information asked above.

    :param filepath:  A filepath to the RSI data used in this function
    :return NONE: Nothing is returned only printed from these functions
    """
    data = pd.read_csv(filepath, header=0)  #reading the csv into a panda dataframe

    participant_col = data.columns[0]  #Taking the participant columns of data
    data_f = data[data[participant_col].str.startswith("F_") == True]  
    #Comparing the columns which start with F_ which are the participant F test and only selects those test 

    print(data_f)  #Prints the participant F data framne as required above
    print("")

    force_data = data_f['force_plate_rsi'].to_numpy(dtype=float)  #changes the data into numpy array to work with in future code
    accel_data = data_f['accelerometer_rsi'].to_numpy(dtype=float) #as above but with the accelerometers data

    #Calculate required inputs to the stats.t.interval function for the force plate and accelerometers
    confidence = 0.95
    df_force = len(force_data) - 1
    df_accel = len(accel_data) - 1

    mean_force = np.mean(force_data)
    mean_accel = np.mean(accel_data)

    sem_force = stats.sem(force_data)
    sem_accel = stats.sem(accel_data)

    #stats.t.interval functions to calculate both the lower and upper confidence intervals for both the
    #Force plate and Accelerometers data and then printing the results
    force_ci_lower, force_ci_upper = stats.t.interval(confidence, df_force, loc=mean_force, scale=sem_force)
    print(f"The force plates lower 95% confidence interval is {force_ci_lower:.5f} and the upper is {force_ci_upper:.5f}")

    accel_ci_lower, accel_ci_upper = stats.t.interval(confidence, df_accel, loc=mean_accel, scale=sem_accel)
    print(f"The accelerometer's lower 95% confidence interval is {accel_ci_lower:.5f} and the upper is {accel_ci_upper:.5f}")


if __name__ == "__main__":
    """
    Run all 3 Tasks in their own methods as written above.  
    Only defining filepath here and calling each method individually and spacing out the prints to be readable
    """
    directorypath = "../../data/drop-jump/"   #Direcctory path up 2 from the data folder
    filename = "all_participant_data_rsi"     #File name
    filepath = directorypath + filename + ".csv"    #Adding all the 3 parts together to form the filepath

    #filepath = r"C:\Users\Declan\Documents\GitHub\ENGR315-fa2026-student\data\drop-jump/all_participant_data_rsi.csv" #Emergency Testing for debugger

    print(f"")
    print(f"")
    print(f"TASK 1: RSI Ttests")
    pairedttest(filepath)
    print(f"")

    print(f"TASK 2: Accelerometer Chi2 Fit Test")
    accelerometertesting(filepath)
    print(f"")

    print(f"TASK 3: Participant F Trials")
    ParticipantFtrials(filepath)
    print(f"")

    print(f"")
    print("done")
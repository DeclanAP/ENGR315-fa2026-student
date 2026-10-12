import sys
import os

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


#Global Variables and Filepaths must be changed for the specific file on your personal computer
Countiesfilepath = r"C:\Users\Declan\Documents\GitHub\ENGR315-fa2026-student\data\covid\us-counties.csv"  #Change on personal computer


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data


### Main Function starting the code ###
if __name__ == "__main__":
    #Create Data sets for the Counties Data by running the premade function
    CountiesData = parse_nyt_data(Countiesfilepath)


    """First Positive COVID test in Harrisonburg"""
    Hburg_first_case_date = "" 

    # Index through each Tuple and in that tuple if the Location mathces Harrisonburg then
    # Get that date and store it and break out of the loop to prevent overwriting the first date
    for index in range(0,len(CountiesData)):
        if CountiesData[index][1] == "Harrisonburg city":
            Hburg_first_case_date = CountiesData[index][0]
            break

    print("Harrisonburg Cities First COVID Case was ", Hburg_first_case_date)

    """First Positive COVID test in Rockingham county"""
    #Variable set up
    Rockingham_first_case_date = "" 

    # Index through each Tuple and in that tuple if the Location mathces Rockingham County AND the state is Virginia then
    # Get that date and store it and break out of the loop to prevent overwriting
    for index in range(0,len(CountiesData)):
            if CountiesData[index][1] == "Rockingham" and CountiesData[index][2] == "Virginia":
                Rockingham_first_case_date = CountiesData[index][0]
                break
    
    print("Rockingham Counties First COVID Case was ", Rockingham_first_case_date)



    """Finding the Greatest Number of Cases reported in Harrisonburg by the Day"""
    # Variable Set Up
    Harrisonburg_Greatest_Cases_Number = 0
    Harrisonburg_Greatest_Cases_Date = ""
    Previous_Cases_Number = 0

    """Iterates through all of the tuples in the data set.  Determines if the data point is for Harrisonburg, then determines if the total cases has increased, 
    then determines if the change in cases is the greatest it has ever been comparing it to the the previous greatest and if it is the greatest then it updates the values accordingly.
    Then updates thje previous cases number after everything else has been accomplished to keep the calculations properly working"""

    for index in range(0,len(CountiesData)):
        if CountiesData[index][1] == "Harrisonburg city":
            if (CountiesData[index][4] > Previous_Cases_Number):
                if Harrisonburg_Greatest_Cases_Number < (CountiesData[index][4] - Previous_Cases_Number):
                    Harrisonburg_Greatest_Cases_Number = (CountiesData[index][4] - Previous_Cases_Number)
                    Harrisonburg_Greatest_Cases_Date = CountiesData[index][0]
            Previous_Cases_Number = CountiesData[index][4]

    print("Harrisonburgs Greatest number of cases in a day was", Harrisonburg_Greatest_Cases_Number, "on the Day", Harrisonburg_Greatest_Cases_Date)

    """Finding the Greatest Number of Cases reported in Rockingham County by the Day"""
    #Variable set up
    Rockingham_Greatest_Cases_Number = 0
    Rockingham_Greatest_Cases_Date = ""
    Previous_Cases_Number = 0
    
    """Iterates through all of the tuples in the data set.  Determines if the data point is for Rockingham, then determines if the total cases has increased, 
    then determines if the change in cases is the greatest it has ever been comparing it to the the previous greatest and if it is the greatest then it updates the values accordingly.
    Then updates the previous cases number after everything else has been accomplished to keep the calculations properly working"""
    #Code to Finding the answers
    for index in range(0,len(CountiesData)):
        if CountiesData[index][1] == "Rockingham" and CountiesData[index][2] == "Virginia":
            if Rockingham_Greatest_Cases_Number < (CountiesData[index][4] - Previous_Cases_Number):
                Rockingham_Greatest_Cases_Number = (CountiesData[index][4] - Previous_Cases_Number)
                Rockingham_Greatest_Cases_Date = CountiesData[index][0]
            Previous_Cases_Number = CountiesData[index][4]

    print("Rockinghams Greatest number of cases in a day was", Rockingham_Greatest_Cases_Number, "on the Day", Rockingham_Greatest_Cases_Date)

    """Finding the Greatest Number of Cases reported in Harrisonburg by the Week"""
    # Variable Set Up
    Harrisonburg_Weeks_Greatest_Cases = 0
    Harrisonburg_Weeks_Greatest_Cases_StartingDate = ""
    Harrisonburg_Weeks_Greatest_Cases_EndingDate = ""
    Previous_Weeks_Cases = 0
    This_Weeks_Cases = 0

    Harrisonburg_Data = []
    """This creates a seperate data set exclusively with data related to Harrisonburg.  This is used to be able to index by each day of data to be able to keep track of a change of week
    by week because a larger data set could not do that"""
    ###Making Just Data for Harrisonburg
    for index in range(0,len(CountiesData)):
        if CountiesData[index][1] == "Harrisonburg city":
            Harrisonburg_Data.append(CountiesData[index])

    """This indexs through the data set and gets the previous 7 days cases count by subtracting the current case number from the one 7 days ago.  
    it then compares it to the current highest weekly cases and updates that value and the starting and end dates"""
    for index in range(6,len(Harrisonburg_Data)):
        This_Weeks_Cases = Harrisonburg_Data[index][4] - Harrisonburg_Data[index-6][4]

        if (This_Weeks_Cases > Previous_Weeks_Cases):
            if (This_Weeks_Cases > Harrisonburg_Weeks_Greatest_Cases):
                Harrisonburg_Weeks_Greatest_Cases = This_Weeks_Cases
                Harrisonburg_Weeks_Greatest_Cases_StartingDate = Harrisonburg_Data[index-6][0]
                Harrisonburg_Weeks_Greatest_Cases_EndingDate = Harrisonburg_Data[index][0]

        Previous_Weeks_Cases = Harrisonburg_Data[index][4] - Harrisonburg_Data[index-6][4]

    print("Harrisonburgs worst 7 day period was from", Harrisonburg_Weeks_Greatest_Cases_StartingDate, "to", Harrisonburg_Weeks_Greatest_Cases_EndingDate, " with",Harrisonburg_Weeks_Greatest_Cases, "cases")

    """Finding the Greatest Number of Cases reported in Rockingham by the Week"""
    # Variable Set Up
    Rockingham_Weeks_Greatest_Cases = 0
    Rockingham_Weeks_Greatest_Cases_StartingDate = ""
    Rockingham_Weeks_Greatest_Cases_EndingDate = ""
    Previous_Weeks_Cases = 0
    This_Weeks_Cases = 0

    Rockingham_Data = []
    """This creates a seperate data set exclusively with data related to Harrisonburg.  This is used to be able to index by each day of data to be able to keep track of a change of week
    by week because a larger data set could not do that"""
    ###Making Just Data for Harrisonburg
    for index in range(0,len(CountiesData)):
        if CountiesData[index][1] == "Rockingham" and CountiesData[index][2] == "Virginia":
            Rockingham_Data.append(CountiesData[index])

    """This indexs through the data set and gets the previous 7 days cases count by subtracting the current case number from the one 7 days ago.  
    it then compares it to the current highest weekly cases and updates that value and the starting and end dates same as the harrisonburg one but with the rockingham data set"""
    for index in range(6,len(Rockingham_Data)):
        This_Weeks_Cases = Rockingham_Data[index][4] - Rockingham_Data[index-6][4]

        if (This_Weeks_Cases > Previous_Weeks_Cases):
            if (This_Weeks_Cases > Rockingham_Weeks_Greatest_Cases):
                Rockingham_Weeks_Greatest_Cases = This_Weeks_Cases
                Rockingham_Weeks_Greatest_Cases_StartingDate = Rockingham_Data[index-6][0]
                Rockingham_Weeks_Greatest_Cases_EndingDate = Rockingham_Data[index][0]

        Previous_Weeks_Cases = Rockingham_Data[index][4] - Rockingham_Data[index-6][4]

    print("Rockinghams worst 7 day period was from", Rockingham_Weeks_Greatest_Cases_StartingDate, "to", Rockingham_Weeks_Greatest_Cases_EndingDate," with",Rockingham_Weeks_Greatest_Cases, "cases")
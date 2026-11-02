import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data():
    return pd.read_csv('../bicycle_data.csv', sep=',')
# The columns of the dataframe are as follows:
#   date: string formatted as 'mm-dd-yyyyThh'
#   number of bicycles on 'Fremont Bridge Sidewalks, south of N 34th St Total' on a given day: numpy.float64
#   number of bicycles on 'Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk' on a given day: numpy.float64
#   number of bicycles on 'Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk' on a given day: numpy.float64


# there is already a totals column but I guess I will make another one for step 3 of the hw
# also counting hours from 0 to 23 so that AM and PM are distinguished for plot in set 6
def add_cols(bike_df):
    hours_data = [int(date[11:13]) for date in bike_df['Date']]
    aftnoon_adjust_data = [12 if (date[-2:] == 'PM') else 0 for date in bike_df['Date']]
    twelve_adjust_data = [-12 if (int(date[11:13]) == 12) else 0 for date in bike_df['Date']]
    hours_data_fixed = np.array(hours_data) + np.array(aftnoon_adjust_data) + np.array(twelve_adjust_data)
    years_data = [int(date[6:10]) for date in bike_df['Date']]
    totals_data = [east + west for (east, west) in zip(bike_df['Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk'], bike_df['Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk'])]

    bike_df.insert(1, 'hour', hours_data_fixed)
    bike_df.insert(1, 'year', years_data)
    bike_df['total'] = totals_data

    return bike_df

def bike_df_yr(bike_df, year):
    return bike_df.loc[bike_df['year'] == year]

# there is one row with missing bicycle counts 
# the date without data is 03/13/2016 02:00:00 AM and it is missing all four bicycle count columns
def removing_missing_data(bike_df):
    return bike_df.dropna()

def plot_hours(bike_df):
    bike_counts = {}
    for i in range(24):
        bike_counts[i] = sum([tot for hr, tot in zip(bike_df['hour'], bike_df['total']) if (hr == i)])
    
    fig, ax = plt.subplots()
    ax.plot(bike_counts.keys(), bike_counts.values())
    ax.set(xlim=(-0.5, 23.5), xticks=np.arange(0, 23))

    plt.title("Total Number of Cyclists per hour on the Fremont Bridge in 2016")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Cyclists")
    plt.savefig('counts_by_hour.png')
    #plt.show()

    return fig

def bike_counts(bike_df):
    bike_counts = {}
    for i in range(24):
        bike_counts[i] = sum([tot for hr, tot in zip(bike_df['hour'], bike_df['total']) if (hr == i)])
    return bike_counts

def busiest_hr(bike_counts):
    hr = max(bike_counts, key=bike_counts.get)
    return hr, bike_counts[hr]

bike_df = load_data()
bike_df = add_cols(bike_df)
bike_df_2016 = bike_df_yr(bike_df, 2016)
bike_df_2016 = removing_missing_data(bike_df_2016)
counts_fig = plot_hours(bike_df_2016)
bike_counts_hr = bike_counts(bike_df_2016)
busiest_hr_2016, max_bikes_hr = busiest_hr(bike_counts_hr)
print("busiest hour:", busiest_hr_2016)
print("total number of bikes during this hour:", max_bikes_hr)
print("average number of bikes during this hour:", max_bikes_hr / 366) # dividing by 366 because 2016 was a leap year

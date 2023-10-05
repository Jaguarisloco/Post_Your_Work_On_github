import time
import pandas as pd
import numpy as np

#dictionary for the three cities
CITY_DATA = { 'chicago': 'data/chicago.csv', 'Chicago': 'data/chicago.csv',
             'New York City': 'data/new_york_city.csv', 'New york city': 'data/new_york_city.csv',
              'new york city': 'data/new_york_city.csv', 'washington': 'data/washington.csv',
             'Washington': 'data/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        str (city): name of the city to analyze
        str (month): name of the month to filter by, or "all" to apply no month filter
        str (day): name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    ## TO get user input for city (chicago, new york city, washington)
    city = ''
    while city not in CITY_DATA.keys():
        print("\nWhich city would you like to analyze " +
                     "among: chicago, new york city or washington?\n\n")

        city = input().lower()
        #to make entries use small letters

        if city not in CITY_DATA.keys():
            print("\nPlease follow the format of the displayed cities.")

    print(f"\nYou have picked {city.title()} as your city.")

    #dictionary for the months including the 'all' option
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nWhich month would you like to analyze for " + city.title() +
                      "? You can choose between january, february, march, " +
                      "april, may and june, or type all if you do not wish "+
                      "to specify a month.\n\n")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nInvalid input. Please follow the format of the displayed months.")

    print(f"\nYou have picked {month.title()} as your month.")

    #a list that stores all the days including the 'all' option
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nNow choose one of the days of the week among: " +
                "monday, tuesday, wednesday, thursday, " +
                "friday, saturday, sunday " +
                "or if you do not wish to choose any type all. \n\n")
        day = input().lower()

        if day not in DAY_LIST:
            print("\nInvalid input. Please follow the format of the displayed days.")


    print(f"\nYou have chosen {day.title()} as your day.")
    print(f"\nYou have chosen to view data for city: {city.upper()}, month/s: {month.upper()} and day/s: {day.upper()}.")
    print('-'*80)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        param1 (str): name of the city to analyze
        param2 (str): name of the month to filter by, or "all" to apply no month filter
        param3 (str): name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    #read the dataframe of the selected city, using the pandas package
    df = pd.read_csv(CITY_DATA[city])

    #Convert Start Time to a datetime object, for subsequent extraction of
    # month and weekday and hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extraction of month and day
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #filtering of dataset, based on selections
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]


    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""


    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Use of mode method to find the most popular month
    popular_month = df['month'].mode()[0]

    print(f"The Most Popular Month is (1 = January,...,6 = June): {popular_month}")

    #Uses mode method to find the most popular day
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nThe Most Popular Day is: {popular_day}")

    #Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    #Uses mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print(f"\nThe Most Popular Start Hour is: {popular_hour}")


    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""


    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Uses mode method to find the most common start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most commonly used start station: {common_start_station}")

    #Uses mode method to find the most common end station
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station is: {common_end_station}")

    #display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    comb = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {comb}.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""


    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_duration = df['Trip Duration'].sum()

    #duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)

    #duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    #average trip duration
    average_duration = round(df['Trip Duration'].mean())

    #average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)

    #display mean travel time either in minutes if below one hour, or in hours if above
    #    and print average trip duration
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""



    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_type = df['User Type'].value_counts()

    print(f"The types of users by number are given below:\n\n{user_type}")

    #The try clause is implemented to display counts of gender
    #not every df may have the Gender column(washington)
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file. Try again")

    #display earliest, most recent, and most common year of birth
    # gender and year of birth are missing from the Washington dataset
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("Sorry. Gender and birth year information are not available.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print('-'*80)


def display_data(df):
    """Displays 5 lines of raw data at a time when yes is selected."""

    RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    counter = 0
    while rdata not in RESPONSE_LIST:
        print("\nWould you like to see 5 lines of raw data? Enter yes or no")
        rdata = input().lower()
        #the raw data from the df is displayed if user opts for it
        if rdata == "yes":
            print(df.head())
        elif rdata not in RESPONSE_LIST:
            print("\nInvalid input. Please input as displayed")

    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        #If user opts for it, this displays next 5 rows of data on output
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*80)

#Main function to call all the previous functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()

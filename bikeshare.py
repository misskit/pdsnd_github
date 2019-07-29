# Explore US Bikeshare Data
# Project 2 in Programming for Data Science - Nanodegree Udacity
# bikeshare.py by Sarah Kit 
# July 2019

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please enter the city (Chicago, New York City, Washington): ").lower()
    # validate city input
    while city not in ['chicago', 'new york city', 'washington']:
        print("Make sure you type in the city correctly. Try again.")
        city = input("2 Please enter the city (Chicago, New York City, Washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Please enter the month (all, january, february, ..., june): ").lower()
    # validate month input
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print("Make sure you type in the month correctly. Try again.")
        month = input("2 Please enter the month (all, january, february, ..., june): ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please enter the day of the week (all, monday, tuesday, ... sunday): ").lower()
    # validate day input
    while day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        print("Make sure you type in the day correctly. Try again.")
        day = input("2 Please enter the day of the week (all, monday, tuesday, ... sunday): ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # find the most popular month
    popular_month = df['month'].mode()[0]
    # display the most common month
    print('Most Popular Start Month:', popular_month)

    # find the most popular day
    popular_day = df['day_of_week'].mode()[0]
    # display the most common day of week
    print('Most Popular Start Week Day:', popular_day)

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    # display the most common start hour
    print('Most Popular Start Hour:', popular_hour)

    # display time spend to calculate stats
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find the most popular start station
    popular_start_station = df['Start Station'].mode()[0]
    # display most commonly used start station
    print('Most Popular Start Station:', popular_start_station)

    # find the most popular end station
    popular_end_station = df['End Station'].mode()[0]
    # display most commonly used end station
    print('Most Popular End Station:', popular_end_station)

    # create field that combine start and end station of a trip
    df['trip_station'] = df['Start Station'] + ' | ' + df['End Station']
    # find the most popular trip
    popular_trip = df['trip_station'].mode()[0]
    # display most frequent combination of start station and end station trip
    print('Most Popular Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['start_time'] = pd.to_datetime(df['Start Time'])
    # convert the Start Time column to datetime
    df['end_time'] = pd.to_datetime(df['End Time'])
    # caculate travel time
    df['travel_time'] = df['end_time'] - df['start_time']

    # Use trip duration (instead of calculated travel time)

    # display total travel time - in hour
    print('Total of all travel time in the city: %s hours.' % round(((df['Trip Duration'].sum())/60),2))

    # display min travel time - in hour
    print('Minimum Travel Time: %s hour(s).' % round(((df['Trip Duration'].min())/60),2))

    # display max travel time - in hour
    print('Maximum Travel Time: %s hours.' % round(((df['Trip Duration'].max())/60),2))

    # display mean travel time - in hour
    print('Mean Travel Time: %s hours.' % round(((df['Trip Duration'].mean())/60),2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df.groupby(['User Type'])['User Type'].count()
    print('Counts of User Types:\n', user_type)

    # When Gender data is missing like in Washington file
    try:
        # Display counts of gender
        gender = df.groupby(['Gender'])['User Type'].count()
        print('\nCounts of Gender:\n', gender)
    except KeyError:
        print('\nNo gender data available for stats.')

    # When birth date data is missing like in Washington file
    try:
        # Display earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        recent_yob = df['Birth Year'].max()
        common_yob = df['Birth Year'].mode()[0]
        print('\nEarliest year of birth: ', int(earliest_yob))
        print('Most recent year of birth: ', int(recent_yob))
        print('Most common year of birth: ', int(common_yob))
    except KeyError:
        print
        print('No birth year data available for stats.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data upon request by the user."""

    print('\nCalculating Display of raw data...\n')
    start_time = time.time()

    # initialize line at 0
    i = 0
    print('Display of raw data: \n', df.head(i))

    while True:
        # ask user if would like to see raw data
        showmore = input('Would you like to see more raw data? Enter yes or no.\n')
        if showmore.lower() == 'yes':
            # display per group of 5, adding to it each time
            i += 5
            print('Display of raw data: \n', df.head(i))
        else:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
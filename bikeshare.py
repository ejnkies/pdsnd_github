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
    # User input for city
    city = ''
    while city not in CITY_DATA:
        city = input("Which city would you like to explore - Chicago, New York City, or Washington? \
        \nPlease enter your selection : ").lower()
        if city not in CITY_DATA:
            print("\nDid you enter the full city name (i.e. New York City) - Nope; Try again!")
    # User input for month (all, january, february, ... , june)
    months = ('All', 'January', 'February', 'March', 'April', 'May', 'June')
    month = ''
    while month not in months:
        month = input("\nWhich month would you like to explore? \
        \nYou're choices are: All or any individual month from January to June \
        \nPlease enter your selection : ").title()
        if month not in months:
            print("\nDid you enter the full month name (i.e. February) - Nope; Try again!")

    # User input for day of week
    days = ('All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    day = ''
    while day not in days:
        day = input("\nWhich day of the week would you like to explore? \
        \nYou're choices are: All or any individual day from Monday to Sunday \
        \nPlease enter your selection : ").title()
        if day not in days:
            print("\nDid you enter the full day name (i.e. Sunday) - Nope; Try again!")

    restart()
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
    # Load data for user selcted city
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    #Adjust Start Time to requried month and day format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month to create the new dataframe
    if month != 'All':
        df = df[df['month'] == month]

    # filter by day of week to create the new dataframe
    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel, based on your filters...\n')
    start_time = time.time()

    # displays the most common month
    popular_month = df['month'].mode()[0]
    print("\nThe most common month is: {}".format(popular_month))

    # displays the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of week is: {}".format(popular_day))

    # displays the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most common start hour is: {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nThe most commonly used start station is: {}".format(popular_start_station))

    # displays most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is: {}".format(popular_end_station))

    # displays most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + ' --> ' + df['End Station']
    popular_route = df['Start End Station'].mode()[0]
    print("The most common travel route is: {}".format(popular_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays total travel time
    total_travel_time = (df['Trip Duration'].sum()/60)/60
    print("\nThe total travel time in hours is: {}".format(total_travel_time))

    # displays mean travel time
    mean_travel_time = df['Trip Duration'].mean() /60
    print("The mean travel time in minutes is: {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_type_count = df['User Type'].value_counts().reset_index()
    print("\nWe have the following counts of Subscribers & Customers: \n{}".format(user_type_count))

    # Displays counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts().reset_index()
        print("\nWe have the following counts for Male & Female users: \n{}".format(gender_count))
    else:
        print("\nSorry - we do not have the Gender data of our users...")

    # Displays earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        birth_year_min = df['Birth Year'].min()
        birth_year_max = df['Birth Year'].max()
        birth_year_common = df['Birth Year'].mode()[0]
        print("\nWe have the following Birth Year data of our users: \
        \nEarliest: {} \
        \nMost Recent: {} \
        \nMost Common: {}".format(int(birth_year_min), int(birth_year_max), int(birth_year_common)))
    else:
        print("\nSorry - we do not have the Birth Year data of our users...")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def u_data(df):
    """Displays underlying data to user 10 rows at a time, until the user exits"""
    underlying_data = input("\nWould you like to see the underlying data? If so, type YES: ").lower()
    start = 0
    end = 10

    while underlying_data == 'yes':
        print(df.iloc[start:end])
        start += 10
        end += 10
        underlying_data = input("\nWould you like to continue viewing the underlying data? If so, type YES: ").lower()

def restart():
    restart = input('\nWould you like to continue? Enter YES to continue.\n')
    if restart.lower() != 'yes':
        quit()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        u_data(df)
        restart()


if __name__ == "__main__":
	main()

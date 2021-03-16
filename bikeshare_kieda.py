"""
Bikeshare Project
Developed by Michael Kieda in January of 2021
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
    while True:
        #prompt user for city
        city = input('Please enter the name of the city to analyze: ').lower()
        # check for valid input
        if city not in CITY_DATA:
            # invalid input, notify user to try again
            print('There is no data for {}.'.format(city.title()),\
            " Let's try it again\n")
        else:
            # input is valid, move on
            print('OK {} it is.\n'.format(city.title()))
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        # prompt user for month
        month = input('Please enter a month to analyze or enter "all": ').lower()
        # check for valid input
        if month not in months and month != 'all':
            # invalid input, notify user to try again
            print('{} is not a recognized month.'.format(month.title()),\
            " Let's try it again.\n")
        else:
            # input is valid, move on
            print('Got it.\n')
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        # prompt user for day
        day = input('Please enter a day of the week to analyze or enter "all": ').lower()
        # check for valid input
        if day not in days and day != 'all':
            # invalid input, notify user to try again
            print('{} is not a recognized day.'.format(day.title()),\
            " Let's try it again.\n")
        else:
            # input is valid, move on
            print('Got it.\n')
            break


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

    # load data file for selected city into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month number from Start Time and create new column
    df['Month'] = df['Start Time'].dt.month
    # filter by month if applicable
    if month != 'all':
        # convert month name to month num (January = 1...June = 6)
        filter_num = months.index(month) + 1
        # update data to include only the specified month
        df = df[df['Month'] == filter_num]

    # extract day of week number from Start Time and create new column
    df['Day of Week'] = df['Start Time'].dt.dayofweek
    # filter by day if applicable
    if day != 'all':
        # convert day of week to day num (Monday = 0...Sunday = 6)
        filter_num = days.index(day)
        # update data to include only the specified day of week
        df = df[df['Day of Week'] == filter_num]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month:  ',\
    months[df['Month'].value_counts().index[0] - 1].title())

    # display the most common day of week
    print('Most common day of week:  ',\
    days[df['Day of Week'].value_counts().index[0]].title())

    # extract hour from Start Time and create new column
    df['Hour'] = df['Start Time'].dt.hour

    # display the most common start hour
    print('Most common start hour:  ', df['Hour'].value_counts().index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most common start station:  ',\
    df['Start Station'].value_counts().index[0])

    # display most commonly used end station
    print('Most common end station:  ',\
    df['End Station'].value_counts().index[0])

    # display most frequent combination of start station and end station trip
    station_combo = \
    df.groupby('Start Station')['End Station'].value_counts().index[0]
    print('Most frequent combination of start and end stations:  {} and {}'\
    .format(station_combo[0], station_combo[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert trip duration from seconds to Timedelta format
    """
    This can be done in a list comprehension using the Timedelta() function
    as shown in the code below.

    df['Trip Duration'] =
    [pd.Timedelta(trip_time, unit='s') for trip_time in df['Trip Duration']]

    This solution had a runtime of 2.488 seconds, whereas recalculating
    Trip Duration, as done below, produces the same result and is MUCH faster
    with a runtime of only 0.015 seconds!!
    """
    df['Trip Duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    print('Total travel time:  ', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time:  ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type   Count')
    print(df['User Type'].value_counts().to_frame()\
    .rename(columns = {'User Type':''}))

    # Display counts of gender
    if 'Gender' in df:
        print('\n\nGender  Count')
        print(df['Gender'].value_counts().to_frame()\
        .rename(columns = {'Gender':''}))
    else:
        print('\n\nSorry, gender data not available in this data set\n')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('\n\nBirth year stats\n')
        print('Earliest birth year:  ', int(df['Birth Year'].min()))
        print('Most recent birth year:  ', int(df['Birth Year'].max()))
        print('Most common birth year:  ',\
        int(df['Birth Year'].value_counts().index[0]))
    else:
        print('Sorry, birth year data not available in this data set\n')


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

        # prompt for display of raw data
        show_data = input\
        ('\nWould you like to see 5 lines of raw data?  Enter yes or no.\n')
        if show_data.lower() == 'yes':
            # start with row 0
            row = 0
            # omit the 3 added (non-original) columns
            last_col = len(df.columns) - 3
            # display all other columns
            pd.set_option('display.max_columns', None)

        while show_data.lower() == 'yes':
            # watch for end of data
            if row+5 < len(df.index):
                # display 5 rows
                print(df.iloc[row:row+5, 0:last_col])
            else:
                # display remain rows (less than 5)
                print(df.iloc[row:, 0:last_col])
                print('\nEnd of data.')
                break

            # advance to next row to be displayed
            row += 5

            show_data = input\
            ('\nWould you like to see more raw data?  Enter yes or no.\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

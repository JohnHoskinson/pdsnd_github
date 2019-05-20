import time
from os import system, name
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def clear():
    '''
    Function to clear terminal window
    '''
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def time_convert(seconds):
    '''
    Function to convert seconds to a string like
    x days y hours z minutes etc
    '''
    str = ''
    if seconds >= 86400: # 60 seconds * 60 minutes * 24 hours = 86400 sec per day
        days = int(seconds // 86400)
        str += '{:,} days '.format(days) # format days to have thousands comma
        seconds -= days * 86400
    else:
        str += '0 days '

    if seconds >= 3600: # 60 seconds * 60 minutes = 3600 sec per hour
        hours = int(seconds // 3600)
        str += '{} hours '.format(hours)
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds // 60)
        str += '{} minutes '.format(minutes)
        seconds -= minutes * 60

    if seconds > 0:
        str += '{} seconds '.format(round(seconds,2))

    return str


def status(invalid, chosen_city = 'na', filter_by = 'na'):
    '''
    Funtion to clear terminal and display users city and filter choice
    Waits 1 second to allow any invalid entry messages to show briefly
    Can be adjusted shorter or longer if need be
    '''

    if invalid: #if user input is invalid, clear screen and show alert
        clear()
        print('\n*** That is an invalid entry.  All user input must be an integer. ***\n')
        print('Please try again.\n\n')
        time.sleep(3)

    clear()

    if chosen_city != 'na':
        print('You have chosen to look at data for: {}'.format(chosen_city))

    if filter_by != 'na':
        print('Filtered by: {}'.format(filter_by))

    print('-'*40)

def print_menu(menu_list = ['Yes', 'No']):
    '''
    Function that take a list of items as input and prints an enumerated menu
    of those items
    '''
    for id, item in enumerate(menu_list):
        print('[{}] - {}'.format(id+1, item))

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    clear()
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    while True:
        city_input = input('\nWhich city do you want to explore?\n(Chicago, New York City or Washington): ').strip().lower()

        if city_input in CITY_DATA:
            city = city_input
            status(False, city_input.title())
            break
        else:
            status(True)

    filter_list = ['Month', 'Day', 'None at All']

    # get user input for month (all, january, february, ... , june)
    while True:
        print('Would you like to filter by month, day or not at all?\n')
        print_menu(filter_list)

        try:
            filter_input = int(input('\nEnter NUMBER KEY for your choice from menu above: '))
        except ValueError:
            print('Input must be an integer from 1 to {}.'.format(len(filter_list)))
            filter_input = len(filter_list) + 1

        if filter_input <= len(filter_list):
            month_day = filter_list[filter_input - 1]
            break
        else:
            status(True, city_input.title())

    if month_day == 'Month':
        day = 'all'
        month_list = ['January', 'February', 'March', 'April', 'May', 'June']

        while True:
            print('\nWhich month do you want to filter by?\n')
            print_menu(month_list)

            try:
                mon_input = int(input('\nEnter NUMBER KEY for your choice from menu above: '))
            except ValueError:
                print('Input must be an integer from 1 to {}.'.format(len(month_list)))
                mon_input = len(month_list) + 1

            if mon_input <= len(month_list):
                month = month_list[mon_input - 1].lower()
                status(False, city_input.title(), month_list[mon_input - 1])
                break
            else:
                status(True, city_input.title(), 'month')


    elif month_day == 'Day':
        month = 'all'
        day_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        while True:
            print('\nWhich day do you want to filter by?\n')
            print_menu(day_list)
            try:
                day_input = int(input('\nEnter NUMBER KEY for your choice from menu above: '))
            except ValueError:
                print('Input must be an integer from 1 to {}.'.format(len(day_list)))
                day_input = len(day_list) + 1

            if day_input <= len(day_list):
                day = day_list[day_input - 1].lower()
                status(False, city_input.title(), day_list[day_input - 1])
                break
            else:
                status(True, city_input.title(), 'day')

    else:
        month, day = 'all', 'all'
        status(False, city_input.title(), 'No Filter')

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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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
    time_data = []
    time_index = []
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    num_months = df['month'].unique().size

    if (num_months != 1):
        # display the most common month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        most_common_month = df['month'].value_counts().idxmax() - 1
        time_data.append(months[most_common_month].title())
        time_index.append('Most common month: ')

    num_days = df['day_of_week'].unique().size

    if num_days != 1:
        # display the most common day of week
        time_data.append(df['day_of_week'].value_counts().idxmax())
        time_index.append('Most common day: ')

    # display the most common start hour
    most_common_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    if  most_common_hour > 12:
        convert_hour = str(most_common_hour - 12) + 'pm'
    elif most_common_hour == 12:
        convert_hour = str(most_common_hour) + 'pm'
    else:
        convert_hour = str(most_common_hour) + 'am'

    time_data.append(convert_hour)
    time_index.append('Most common start hour: ')

    # display table of all the time stats
    time_df = pd.DataFrame(time_data, index=time_index)
    time_df.columns = ['']
    print(time_df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    station_data = []
    station_index = []
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    station_data.append(df['Start Station'].value_counts().idxmax())
    station_index.append('Most commonly used start station: ')

    # display most commonly used end station
    station_data.append(df['End Station'].value_counts().idxmax())
    station_index.append('Most commonly used end station: ')

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' --> ' + df['End Station']
    station_data.append(df['trip'].value_counts().idxmax())
    station_index.append('Most frequent trip (start to stop): ')

    # display table of all the time stats
    station_df = pd.DataFrame(station_data, index=station_index)
    station_df.columns = ['']
    print(station_df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    trip_data = []
    trip_index = []

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_data.append(time_convert(sum(df['Trip Duration'])))
    trip_index.append('Total travel time: ')

    # display mean travel time
    trip_data.append(time_convert(df['Trip Duration'].mean()))
    trip_index.append('Mean travel time: ')

    trip_df = pd.DataFrame(trip_data, index=trip_index)
    trip_df.columns = ['']
    print(trip_df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    user_data = []
    user_index = []

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = dict(df['User Type'].value_counts())
    user_data.append(' ')
    user_index.append('USER TYPE COUNTS - - - - - - ')

    for type, count in user_type_counts.items():
        user_data.append('{:,}'.format(count))
        user_index.append(type)

    if 'Gender' in df.columns:

        # Display counts of gender
        gender_counts = dict(df['Gender'].value_counts())
        user_data.append(' ') #add empty row to list for display purposes
        user_index.append(' ')#add empty row to list for display purposes

        user_data.append(' ')
        user_index.append('GENDER COUNTS - - - - - - - -')

        for gender, count in gender_counts.items():
            user_data.append('{:,}'.format(count))
            user_index.append(gender)

        # Display earliest, most recent, and most common year of birth
        user_data.append(' ') #add empty row to list for display purposes
        user_index.append(' ')#add empty row to list for display purposes

        user_data.append(int(df['Birth Year'].dropna(axis=0).min()))
        user_index.append('Earliest birth year: ')

        user_data.append(int(df['Birth Year'].dropna(axis=0).max()))
        user_index.append('Most recent birth year: ')

        user_data.append(int(df['Birth Year'].dropna(axis=0).mode()))
        user_index.append('Most common birth year: ')

    user_df = pd.DataFrame(user_data, index=user_index)
    user_df.columns = ['']
    print(user_df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    first_row = 0
    word = 'first'
    while True:
        print('-'*40)
        print('\nWould you like to view the {} 5 rows of raw data?\n'.format(word))
        print_menu()

        try:
            raw_input = int(input('\nEnter NUMBER KEY for your choice from menu above: '))
        except ValueError:
            print('Input must be an integer from 1 to {}.'.format(len(city_list)))

        if raw_input == 1:
            print('-'*40)
            end_row = first_row + 5
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(df.iloc[first_row:end_row, :])
            first_row += 5
            word = 'next'

        elif raw_input > 2:
            print('\n*** That is an invalid entry.  Input must be an integer - either 1 or 2. ***')
            print('Please try again.\n\n')
        else:
            clear()
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        print('\nWould you like to restart?\n')

        print_menu()
        try:
            restart = int(input('\nEnter NUMBER KEY for your choice from menu above: '))
        except ValueError:
            print('Input must be an integer - either 1 or 2.')

        if restart > 2:
            print('\n*** That is an invalid entry.  Input must be an integer - either 1 or 2. ***')
            print('Please try again.\n\n')
        elif restart == 2:
            clear()
            print('Goodbye!\n\n')
            break


if __name__ == "__main__":
	main()

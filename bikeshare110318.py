import time
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

def get_city():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data.')

    while True:
        get_city = input('Would you like to see data for Chicago, New York, or Washington?\n')
        if get_city.lower() in ('chicago', 'new york', 'washington'):
            if get_city.lower() == 'chicago':
                city_select = chicago

            elif get_city.lower() == 'new york':
                city_select = new_york_city

            elif get_city.lower() == 'washington':
                city_select = washington

            break
        print('ENTER a valid city name provided in the options!')
    df = pd.read_csv(city_select)
    # parse datetime and column names
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #replace white spaces with underscore for all column names
    df.columns = [x.strip().replace(' ', '_') for x in df.columns]
    city = get_city.lower()
    return df, city


def get_filter_way_month_day(df):
    while True:
        get_filter_way = input('Would you like to filter the data by "month", "day",\nor not at all(type"none")?\n')
        if get_filter_way.lower() in ('month', 'day', 'none'):
            break
        print('Please input: month, day or none\n')
    if get_filter_way =='month':
        #ask for the month of choice
        month = ('january', 'february', 'march', 'april', 'may', 'june')
        while True:
            get_month = input('\nWhich month? January, February, March, April, May, or June?\n')
            if get_month.lower() in month:
                #filter the data accourding to the get_month
                month_num = month.index(get_month.lower()) + 1
                filter_month_day = df[df['Start_Time'].dt.month==month_num]
                get_filter_way = get_month.lower()
                break
            print('Enter a valid month name provided in the options')

    elif get_filter_way =='day':
        weekdays = ('monday 0','tuesday 1','wednesday 2','thursday 3','friday 4','saturday 5','sunday 6')
        while True:
            #ask for the weekday of choice
            get_day = int(input('\nWhich day? Please type your response as an integer. E.g. Monday:0, Tuesday:1...\n'))
            if get_day in np.arange(0,6,1,'int'):
                #filter the data accourding to the get_day
                filter_month_day = df[df['Start_Time'].dt.dayofweek==get_day]
                get_filter_way=weekdays[get_day]
                break
            print('Enter a valid day name!')

    else:
        filter_month_day = df # for none option
    print('-'*40)
    return filter_month_day, get_filter_way


def time_stats(city,get_filter_way,filter_month_day):

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(filter_month_day['Start_Time'].dt.month.mode())
    most_month = months[index - 1]
    print('The most popular month is {}.'.format(most_month))


    # TO DO: display the most common day of week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    index = int(filter_month_day['Start_Time'].dt.dayofweek.mode())
    most_pop_day = days_of_week[index]
    print('The most popular day of week for start time is {}.'.format(most_pop_day))


    # TO DO: display the most common start hour

    pop_hour  = filter_month_day['Start_Time'].groupby([filter_month_day['Start_Time'].dt.hour]).agg('count')
    print("The most popular hour of the day for start time is {}:00 with {} total transactions.".format(pop_hour .argmax(), pop_hour [pop_hour .argmax()]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(city,get_filter_way,filter_month_day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popularstart_station = filter_month_day['Start_Station'].mode().to_string(index = False)
    print('The most popular start station is {}.'.format(popularstart_station ))

    # TO DO: display most commonly used end station
    popularend_statioin = filter_month_day['End_Station'].mode().to_string(index = False)
    print('The most popular end station is {}.'.format(popularend_statioin))

    # The 'journey' column is created in the main() function.
    filter_month_day['journey'] = filter_month_day['Start_Station'].str.cat(filter_month_day['End_Station'], sep=' to ')
    most_pop_trip = filter_month_day['journey'].mode().to_string(index = False)
    print('The most popular trip is {}.'.format(most_pop_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(city,get_filter_way,filter_month_day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total trip & average trip duration are {} seconds and {} seconds".format(format(filter_month_day['Trip_Duration'].max()), format(filter_month_day['Trip_Duration'].mean())))


    # TO DO: display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(city,get_filter_way,filter_month_day):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    sub = filter_month_day.query('User_Type == "Subscriber"').User_Type.count()
    cus = filter_month_day.query('User_Type == "Customer"').User_Type.count()
    print('There are {} Subscribers and {} Customers.'.format(sub, cus))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def gender_birthyear(city,get_filter_way,filter_month_day):

    print('\nCalculating gender, birth_year\n')
    start_time = time.time()

    if get_city.lower() == 'washington':
        print('NO present for Washingtion.')
    elif get_city == 'chicago' or 'new york':
        male = filter_month_day.query('Gender == "Male"').Gender.count()
        female = filter_month_day.query('Gender == "Female"').Gender.count()

        print('There are {} male users and {} female users.'.format(male, female))


    # TO DO: Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth_Year'].min())
        latest = int(df['Birth_Year'].max())
        mode = int(df['Birth_Year'].mode())
        print('The oldest user are born in {}.\nThe youngest user are born in {}.'
          '\nThe most people birth year is {}.'.format(earliest, latest, mode))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(city_name,get_filter_way,filter_month_day):

    count=0;
    while True:
        display = input('\nWould you like to view individual trip data (yes or no)\n')
        if display.lower() in ('yes', 'no'):
            if display.lower() == 'yes':
                print(filter_month_day[count:count+5])
                count +=5
            else:
                print('Display of the data ends!')
                break
        print('Enter a valid input provided in the options')

def main():
    while True:

        original_data, city_name = get_city()
        filtered_data, filter_method = get_filter_way_month_day(original_data)

        if filter_method == 'none':

            time_stats(city_name,filter_method,filtered_data)

    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
        month = ('january', 'february', 'march', 'april', 'may', 'june')
        if filter_method == 'none' or filter_method in month:
            time_stats(city_name,filter_method,filtered_data)
            print('\nCalculating the first statistic...')

        time_stats(city_name,filter_method,filtered_data)
        station_stats(city_name,filter_method,filtered_data)
        trip_duration_stats(city_name,filter_method,filtered_data)
        user_stats(city_name,filter_method,filtered_data)
        display_data(city_name,filter_method,filtered_data)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        main()

if __name__ == "__main__":
	main()

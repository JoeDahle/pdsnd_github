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

    #Get the Users input for City, Month, and Day, randomly select if user types incorrect option.
    city = None

    while city is None:
        user_city_input = input("Enter \"Chicago\", \"New York City\", or \"Washington\": ")

        if user_city_input.lower() == "chicago":
            city = "chicago"
        elif user_city_input.lower() == "new york city":
            city = "new york city"
        elif user_city_input.lower() == "washington":
            city = "washington"
        else:
            city = np.random.choice(["chicago", "new york city", "washington"])
            print("Your entry was not recognized, {} was picked instead.".format(city))

    month = None

    while month is None:
        user_month_input = input("Enter A Month, January-June or type All: ")

        if user_month_input.lower() == "january":
            month = "january"
        elif user_month_input.lower() == "february":
            month = "february"
        elif user_month_input.lower() == "march":
            month = "march"
        elif user_month_input.lower() == "april":
            month = "april"
        elif user_month_input.lower() == "may":
            month = "may"
        elif user_month_input.lower() == "june":
            month = "june"
        elif user_month_input.lower() == "all":
            month = "all"
        else:
            month = np.random.choice(["january", "february", "march", "april", "may", "june"])
            print("Your entry was not recognized, {} was picked instead.".format(month.upper()))

    day = None

    while day is None:
        user_day_input = input("Enter a Day of the Week or type All: ")

        if user_day_input.lower() == "sunday":
            day = "sunday"
        elif user_day_input.lower() == "monday":
            day = "monday"
        elif user_day_input.lower() == "tuesday":
            day = "tuesday"
        elif user_day_input.lower() == "wednesday":
            day = "wednesday"
        elif user_day_input.lower() == "thursday":
            day = "thursday"
        elif user_day_input.lower() == "friday":
            day = "friday"
        elif user_day_input.lower() == "saturday":
            day = "saturday"
        elif user_day_input.lower() == "all":
            day = "all"
        else:
            day = np.random.choice(["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"])
            print("Your entry was not recognized, {} was picked instead.".format(day.upper()))

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

    df = pd.read_csv(CITY_DATA[city])

    # convert to month text name from start date column
    df['Month_Name'] = pd.to_datetime(df['Start Time']).dt.strftime('%B').str.lower()

    # convert to year from start time column
    df['Year']  = pd.to_datetime(df['Start Time']).dt.year

    # convert to month int value for analytics from start time
    df['month'] = pd.to_datetime(df['Start Time']).dt.month

    # convert to weekday name from start time
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.strftime('%A').str.lower()

    # convert Start Time to a rounded hour
    df['start_hour_rounded'] = (pd.to_datetime(df['Start Time']).dt.round("H")).dt.strftime('%r')

    if month != 'all':
        # get the month index
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month
        df = df.loc[df['month'] == month,:]

    if day != 'all':
        # filter by day of the week
        df = df.loc[df['day_of_week'] == day,:]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()
    city, month, day = get_filters()

    # Show most frequent month if 'All' is selected
    if month == 'all':
        print("The most common month is: {}".format(str(df['Month_Name'].mode().values[0])))

    # Show most frequent day if 'All' is selected
    if day == 'all':
        print("The most common day of the week is: {}".format(str(df['day_of_week'].mode().values[0])))

    # Show most frequent start hour
    print("The most common start hour is: {}".format(str(df['start_hour_rounded'].mode().values[0])))

    # Display computation time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
    # SHow Most common Start area
        print("The most common Start Station is: {}".format(str(df['Start Station'].mode().values[0])))

    # Show most common End area
        print("The most common End Station is: {}".format(str(df['End Station'].mode().values[0])))

    # Show most common Starting & Ending Locations
        df['combination'] = df['Start Station'] + df['End Station']
        print('The most combination of start station and end station trip is\n {}'.format((df['combination'].mode()[0])))
    except:
        print("Could not gather inforation about Start and End stations for the selected query.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
        # Show Total Travel Time
        print("Total Travel Time: {}".format(df['Trip Duration'].sum()))

        # Show Average Travel Time
        print("Mean Travel Time: {}".format(df['Trip Duration'].mean()))
    except:
        print("Could not gather travel time information for the selected query.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Show Total User Types
    try:
        print("User Count Types: \n{}".format(str(df['User Type'].value_counts())))
        print('\n')
    except:
        print("Coubld not gather User Type information for this query.")

    # Show Gender Counts
    try:
        print("User Gender Types: \n{}".format(str(df['Gender'].value_counts())))
        print('\n')
    except:
        print("Could Not gather Gender Information for the selected query.")

    # Show Average Age, Oldest and Youngest Users
    try:
        print("Most common Birth Year: {}".format(int(df['Birth Year'].mode()[0])))
        print("Oldest Birth Year: {}".format(int(df['Birth Year'].min())))
        print("Youngest Birth Year: {}".format(int(df['Birth Year'].max())))
    except:
        print("Could not gather Birth Year Information for the selected query.")

    print('\n')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Shows raw data (5 rows) from the Dataframe as chosen by the user"""
    start_row = 0
    end_row = 4

    while True:
        raw = input('\nTo View 5 Lines of Raw Data, type \'Yes\', otherwise, press \'enter\' \n')

        if raw.lower() != 'yes':
            break
        else:
           print(df[df.columns[0:]].iloc[start_row:end_row])
           start_row += 5
           end_row += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

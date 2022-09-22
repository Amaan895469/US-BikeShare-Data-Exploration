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
    city=input("Enter the city ")
    city=city.lower()
    while city != 'chicago' and  city != 'new york city' and city != 'washington':
        city=input("Enter the city ")
        city=city.lower()

    # get user input for month (all, january, february, ... , june)
    month= input("Enter the month ")
    month=month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input ("Enter the name of day ")
    day = day.lower()
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
    df=pd.read_csv(str('D:/amaanfolder/')+CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #print(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['year']= df['Start Time'].dt.year
    df['month']= df['Start Time'].dt.month_name()
    
    dw_mapping={
    0: 'monday', 
    1: 'tuesday', 
    2: 'wednesday', 
    3: 'thursday', 
    4: 'friday',
    5: 'saturday', 
    6: 'sunday'} 
    
    df['day_of_week']=df['Start Time'].dt.weekday.map(dw_mapping)
    #f['day_of_week'] = df['Start Time'].dt.dayofweek
    df['day']= df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour
    #df= df.rename(columns=str.lower)
    df['month'] = df['month'].str.lower()
    df['day'] = df['day'].str.lower()
    df=df.query('month == @month')
    df=df.query('day == @day')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
   
    
    # display the most common month
    common_month=df['month'].mode()
    print('Common Month ',common_month)
    

    # display the most common day of week
    common_day=df['day_of_week'].mode()
    print('Common Day  ' ,common_day)
    # display the most common start hour
    
    common_hour=df['hour'].mode()
    print('Common Hour ' ,common_hour)
  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return common_month,common_day
    #https://towardsdatascience.com/working-with-datetime-in-pandas-dataframe-663f7af6c587
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_station=df['Start Station'].mode()
    print('Common Start Station : ',common_station)
    # display most commonly used end station
    common_station=df['End Station'].mode()
    print('Common End Station : ',common_station)
    # display most frequent combination of start station and end station trip
    common_combination=df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most Frequent Combination of Stations : ',common_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('Total Travel Time : ',total_travel_time)
    # display mean travel time
    mean_travel_time=df['Trip Duration'].mean()
    print('Mean Travel Time : ',mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    UserTypeCount=df['User Type'].value_counts()
    print('User Type Count :')
    print(UserTypeCount)
    
    if city != 'washington':
    # Display counts of gender
        GenderCount=df['Gender'].value_counts()
        print('Gender Count :')
        print(GenderCount)
    
        # Display earliest, most recent, and most common year of birth
        MostCommonyob= df['Birth Year'].mode()
        print("Most Common Year of Birth : ",MostCommonyob)
    
    
        Earliestyob= df['Birth Year'].min()
        print('Earliest Year Of Birth :',Earliestyob)
    
        mostrecentyob= df['Birth Year'].max()
        print("Most Recent Year of Birth :",mostrecentyob)
    else:
        print("Gender stats cannot be calculated as Gender column not found in dataframe")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data=input("Would you like to view 5 rows of individual trip data? Enter yes or no ").lower()
    start_loc=5
    while view_data == 'yes':
        print(df.iloc[:start_loc])
        start_loc +=5
        view_data= input ("Would you like to view 5 more rows of individual trip data? Enter yes or no?: ").lower()
    return view_data
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        try:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
            if display_data(df) != 'yes':
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() != 'yes':
                    break
            else:
                display_data(df)
        except:
            
            print("NO DATA FOUND!")
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break



if __name__ == "__main__":
	main()

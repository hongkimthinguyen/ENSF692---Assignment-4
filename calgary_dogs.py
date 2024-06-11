# calgary_dogs.py
# Author: Kim Nguyen
#
# This script is a terminal-based application for computing and printing statistics based on dog breed input.
# It reads data from an Excel file and performs various analyses based on the user's input.
# Detailed specifications are provided via the Assignment 4 README file.
# The script includes the main function, additional functions for user input, and data analysis.
# It imports necessary modules from the standard Python library.
# Docstrings and comments are included throughout the code for clarity.

import pandas as pd

def main():
    """
    The main function that orchestrates the execution of the program.
    It reads the data, gets user input, and calculates the breed statistics.
    """
    # Stage 1: DataFrame creation
    # Import data from the Excel file
    file_path = 'CalgaryDogBreeds.xlsx'
    df = pd.read_excel(file_path)

    # Set and sort the multi-index for the DataFrame
    # 'Breed' is used as the primary index for easier data access and analysis
    df.set_index(['Breed', 'Year', 'Month'], inplace=True)
    df.sort_index(inplace=True)

    print("\nENSF 692 Dogs of Calgary")

    # Stage 2: User input stage
    user_input = get_user_input(df)

    # Stage 3: Data analysis stage
    calculate_breed_stats(df, user_input)

def get_user_input(df):
    """
    Prompts the user to enter a dog breed and validates the input.

    Parameter:
        df (pd.DataFrame): The DataFrame loaded by reading the Excel dataset.

    Return:
        str: The valid dog breed input by the user in uppercase.
    """
    while True:
        try:
            # Prompt the user to enter a dog breed
            user_input = input("Please enter a dog breed: ").upper()
            # Check if the breed exists in the DataFrame index
            if user_input in df.index.get_level_values('Breed'):
                return user_input
            else:
                raise KeyError
        except KeyError:
            print("Dog breed not found in the data. Please try again.")

def calculate_breed_stats(df, breed):
    """
    Calculates and prints statistics for the given dog breed.

    Parameters:
        df (pd.DataFrame): The DataFrame loaded by reading the Excel dataset.
        breed (str): The dog breed provided by the user input.

    Return:
        None
    """
    # Use the IndexSlice object to slice the DataFrame
    idx = pd.IndexSlice

    # 3.1. Find all the years in which the breed appears
    breed_data = df.loc[idx[breed, :, :]]
    breed_years = ", ".join(map(str, breed_data.index.get_level_values('Year').unique()))
    print(f"The {breed} was found in the top breeds for years: {breed_years}. ")

    # 3.2. Calculate the total number of registrations of the selected breed
    total_breed_all_years = breed_data['Total'].sum()
    print(f"There have been {total_breed_all_years} {breed} dogs registered total.")

    # 3.3. Calculate the percentage of breed registrations for each year
    years = [2021, 2022, 2023]
    for year in years:
        total_dogs_per_year = df.loc[idx[:, year, :], 'Total'].sum()
        selected_breed_per_year = df.loc[idx[breed, year, :], 'Total'].sum()
        percentage_breed_per_year = round((selected_breed_per_year / total_dogs_per_year) * 100, 6)
        print(f"The {breed} was {percentage_breed_per_year}% of top breeds in {year}.")

    # 3.4. Calculate the percentage of breed registrations across all years
    total_dogs_all_years = df.loc[idx[:, years, :], 'Total'].sum()
    percentage_breed_all_years = round((total_breed_all_years / total_dogs_all_years) * 100, 6)
    print(f"The {breed} was {percentage_breed_all_years}% of top breeds across all years.")

    # 3.5. Find the most popular months for the selected breed
    breed_months = breed_data.groupby('Month')['Total'].sum()
    mean_registration = breed_months.mean()
    popular_months = breed_months[breed_months >= mean_registration].index.tolist()
    print(f"Most popular month(s) for {breed} dogs: {', '.join(popular_months)}")

if __name__ == '__main__':
    main()

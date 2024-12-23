# Customer_loans_in_finance
Exploratory Data Analysis - Customer Loans in Finance - Project 2.

## Description 
Project number 2 from AiCore extracting data from RDS

## Learnings
- Setting up an environment on Github ready to download info onto.
- Connecting to the cloud to download data.
- Setting up a .gitignore file with important confidential data that shouldn't be tracked. a.
- Pushing onto Github and writing a README relevant for the user.
- Data cleaning: Handling missing values, correcting data types, and addressing any inconsistencies.
- Data visualization: Utilizing tools like seaborn and matplotlib to create meaningful visual representations of the data.
- Statistical tests: Applying statistical methods to identify significant relationships and differences in the data.
- Machine learning preparation: Preparing data for machine learning models by normalizing, scaling, and splitting data.


## Installation Instructions

## Usage Instructions
- Useful for understanding the process of downloading from an external source, using passwords from another file.

## File Structure of Project
**Main files for review:**
- milestone_3.ipynb contains milestone 1-3 alongside the supplementary docs as listed below.
- transform_data is the supplementary code for milestone_3.
- milestone_4.ipynb contains just milestone 4

- db_utils.py pulls, extracts and saves the data as a csv folder.
- loan_payments.csv is the extracted data from the RDS in csv format.
- updated_dataframe.csv this is the csv of the data once I had removed all the null values as per the task (milestone_3 task 3)
- cleaned_dataframe.csv where outliers had been removed.
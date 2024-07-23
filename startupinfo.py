import pandas as pd
from IPython.display import display
import openai 
openai.api_key = 'YOUR_API_KEY'

# This script will do everything in Pandas Dataframes instead of CSV, after all the functions (such as deciding on the most relevant work experience and writing the resume sections are done),  we'll save the dataframe to CSV to store in our database.

def get_user_info():

    user_name = input("Enter your name: ")
    user_email = input("Enter your email: ")  # This is the unique identifier
    job_role_target = input("Enter the job role title or field you are pursuing: ")
    return user_name, user_email, job_role_target

def get_job_experience():

    job_title = input("Enter job title: ")
    start_date = input("Enter start date: ")
    end_date = input("Enter end date: ")
    return job_title, start_date, end_date

# Collect user details
user_name, user_email, job_target = get_user_info()

# List to hold multiple job experiences
job_experiences = []

# Loop to get multiple job experiences
while True:

    job_title, start_date, end_date = get_job_experience()
    job_experiences.append({
        "User Email": user_email,
        "User Name": user_name,
        "Job Title": job_title,
        "Start Date": start_date,
        "End Date": end_date
    })
    
    more = input("Do you have another job experience to add? (yes/no): ")
    if more.lower() != "yes":
        break

# Create a pandas DataFrame
df = pd.DataFrame(job_experiences)

# File path and name
filename = "job_experiences.csv"

# Writing to the CSV file
df.to_csv(filename, index=False) # We will need to edit this to make the program append to the CSV instead of rewriting it

print(f"Data successfully written to {filename}")
print('_____________')

work_experiences_dataframe = df[['Job Title', 'Start Date', 'End Date']] # Only displaying the work experience portion of the dataframe

display(work_experiences_dataframe)

def get_most_relevant_work_experience(dataframe): # Function to get GPT to decide on which work experience is the most suitable

    list_of_work_experience_dictionaries = []
    # Converting each row of the dataframe into a dictionary, then storing this as a list of dictionaries so that we can parse it through to GPT
    for index, row in work_experiences_dataframe.iterrows(): 

        new_work_experience_dict = {}
        new_work_experience_dict.update({'Job Title': row['Job Title'], 'Start Date': row['Start Date'], 'End Date': row['End Date']})
        list_of_work_experience_dictionaries.append(new_work_experience_dict)
        
    # This is the GPT prompt
    content = (f"You are choosing the most relevant work experiences in order to generate a resume/CV for the job role: {job_target}. Here is the list of work experiences as python dictionaries, including their job title, start date, and end date: {str[list_of_work_experience_dictionaries]}. Out of these, choose the two most relevant work experiences that you are going to write sections for on the resume. Your output should just be in a python list format, like this: [job_experience_1, job_experience_2]. Don't include any more text other than just the python list, because I'll need to parse your response through to the ChatGPT API again.")

    gpt_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}]
    )

    return gpt_response.choices[0].message.content # Function returns the GPT response

most_relevant_experiences_list = get_most_relevant_work_experience(work_experiences_dataframe)

print(most_relevant_experiences_list)



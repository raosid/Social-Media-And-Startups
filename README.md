# Social-Media-And-Startups

Analyzing the effect of Social Media use by startups.

## Twitter Data:
Fetches tweets for startups. Gets Tweets from two accounts:
    * The Company's handle
    * The CEO's handle

Gets the handles from a CSV File. For each of the company, creates a new Folder wit two files containing the tweets from each of the above mentioned accounts.

#### Files and Folders
**fetch-tweets.py**: The python script to fetch all the tweets.

**list-of-startups.csv**: A csv file containing the information of Startups (Handles for CEO and the company)

**tweets/**: Contains all tweets for each of the company in the csv file.

**initial-tweets/**: Contains the initial 200 tweets gathered for the first stage.

## Angel List Data:

Gathers information about startups based in the United States.
Uses the [Angel List API](https://angel.co/api/) to fetch information about the startups.

#### Files and Folders
**angellist_get_companies.py**: Script to fetch information about the startups in the United States.

Note: Have to specify the page numbers in order to fetch data.

**companies/**: Has JSON files for 500 companies each of which stores the companies information as gathered from the Angel List API.

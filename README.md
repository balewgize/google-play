# Google Play Scraper

Extract app information from Google Play Store

## Step 0: Install Python

- If you don't have Python installed already, install version 3.8 or higher at
https://www.python.org/downloads/ 

## Step 1: Provide data of 50k apps in CSV

- Copy the CSV file containing data of 50k apps into google-play folder

(There must be single CSV file inside google-play, if there are any other, move them to another folder)

## Step 2: Create a virtual environment

- Extract google-play.zip to a directory you want (e.g Desktop)

- Open CMD (Terminal) and navigate to the extracted google-play folder

(If you extract on Desktop)

cd Desktop/google-play/

- Create a virtual environment and activate it

(Windows: Run the following commands on the Command Prompt)

python -m venv venv

.\venv\Scripts\activate


(Linux & Mac: Run the following commands on the Terminal)

python3 -m venv venv

source venv/bin/activate

## Step 3: Install required packages

pip install -r requirements.txt

## Step 4: Run the script

- Open CMD (Terminal) and run the following command

python google_play_scraper.py (Windows)

python3 google_play_scraper.py (Linux & Mac)



# Using the script after first time installation

- Provide data of 50k apps in CSV

- Copy a CSV file containing data of 50k apps into google-play folder

(There must be a single CSV file inside google-play, if there are any other, move them to another folder)

- Open CMD (Terminal) and navigate to extracted google-play folder

cd Desktop/google-play/

- Activate the virtual environment

.\venv\Scripts\activate (Windows)

source venv/bin/activate (Linux & Mac)

- Run the script using the following command

python google_play_scraper.py (Windows)

python3 google_play_scraper.py (Linux & Mac)
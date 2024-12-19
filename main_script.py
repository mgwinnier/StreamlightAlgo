import os
import shutil
import zipfile
import pandas as pd
from odds import scrape_odds_to_excel
from results import scrape_ncaa_scores_to_excel
from algo import parse_data_from_file


def run_scraping_tasks(date):
    """Run scraping tasks, process the data, and save outputs into a ZIP file."""
    # Standardize date format
    formatted_date = date.replace('/', '-')

    # Directory for the date
    directory_name = os.path.join('.', formatted_date)
    os.makedirs(directory_name, exist_ok=True)

    # Define file paths
    odds_filename = os.path.join(directory_name, f"odds-{formatted_date}.xlsx")
    results_filename = os.path.join(directory_name, f"results-{formatted_date}.xlsx")
    processed_filename = os.path.join(directory_name, f"processed_data-{formatted_date}.xlsx")

    try:
        # Scrape odds
        scrape_odds_to_excel(date, odds_filename)

        # Scrape NCAA scores
        ncaa_url = f'https://www.ncaa.com/scoreboard/basketball-men/d1/{date.replace("/", "/")}/all-conf'
        scrape_ncaa_scores_to_excel(ncaa_url, results_filename)

        # Process data
        parse_data_from_file("data.txt", formatted_date)

        # Prepare ZIP file
        zip_filename = f"{formatted_date}.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            # Add all Excel files to the ZIP
            for file in [odds_filename, results_filename, processed_filename]:
                if os.path.exists(file):
                    zipf.write(file, os.path.basename(file))

        print(f"All data saved to {zip_filename}")
        return zip_filename
    except Exception as e:
        print(f"Error in run_scraping_tasks: {e}")
        raise

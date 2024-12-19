import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_odds_to_excel(date, output_file):
    """Scrape odds from Vegas Insider and save to an Excel file."""
    url = f'https://www.vegasinsider.com/college-basketball/odds/las-vegas/?date={date}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize lists
        top_team_names = []
        bottom_team_names = []
        top_team_odds = []
        bottom_team_odds = []

        # Find rows for odds
        divided_rows = soup.find_all('tr', class_='divided')
        footer_rows = soup.find_all('tr', class_='footer')

        # Extract data
        for row in divided_rows:
            team_name_element = row.select_one('.team-name')
            odds_element = row.find_all('td', class_='game-odds')[2].find('span', class_='data-value')

            if team_name_element and odds_element:
                top_team_names.append(team_name_element.get_text(strip=True))
                top_team_odds.append(odds_element.get_text(strip=True))

        for row in footer_rows:
            team_name_element = row.select_one('.team-name')
            odds_element = row.find_all('td', class_='game-odds')[2].find('span', class_='data-value')

            if team_name_element and odds_element:
                bottom_team_names.append(team_name_element.get_text(strip=True))
                bottom_team_odds.append(odds_element.get_text(strip=True))

        combined_data = []
        for top_name, top_odds, bottom_name, bottom_odds in zip(top_team_names, top_team_odds, bottom_team_names, bottom_team_odds):
            combined_data.append((top_name, top_odds))
            combined_data.append((bottom_name, bottom_odds))

        # Save to Excel
        df = pd.DataFrame(combined_data, columns=['Team Name', 'Odds Value'])
        df.to_excel(output_file, index=False)
        print(f'Odds data saved to {output_file}')
    else:
        print(f"Failed to fetch odds: {response.status_code}")


# Ensure this runs only when the script is executed directly
if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description='Scrape odds data and save to an Excel file.')
    parser.add_argument('date', help='Date in YYYY-MM-DD format')
    parser.add_argument('output_file', help='Output Excel file path')
    args = parser.parse_args()

    scrape_odds_to_excel(args.date, args.output_file)

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_ncaa_scores_to_excel(url, output_file):
    """Scrape NCAA scores and save them to an Excel file."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate all game containers
        games = soup.find_all(class_='gamePod-type-game')
        team_names = []
        team_scores = []

        for game in games:
            teams = game.find_all(class_='gamePod-game-team-name')
            scores = game.find_all(class_='gamePod-game-team-score')

            for team, score in zip(teams, scores):
                team_name = team.text.strip()
                # Apply normalization
                team_name = team_name.replace('St.', 'State').replace('U.', 'University').replace('Ky.', 'Kentucky')
                team_name = team_name.replace('Fla.', 'Florida').replace('La.', 'Louisiana').replace('Ill.', 'Illinois')
                team_name = team_name.replace('N.M.', 'New Mexico').replace('N.C.', 'North Carolina').replace('Ark.', 'Arkansas')
                team_name = team_name.replace('UIW', 'Incarnate Word').replace('Ala.', 'Alabama').replace('So.', 'Southern')
                team_name = team_name.replace('FIU', 'Florida International').replace('LSU', 'Louisiana State')
                team_name = team_name.replace('BYU', 'Brigham Young').replace('UNLV', 'Nevada-Las Vegas')
                team_name = team_name.replace('Seattle U', 'Seattle').replace('Miss.', 'Mississippi')
                team_name = team_name.replace('McNeese', 'McNeese State').replace('App State', 'Appalachian State')
                team_name = team_name.replace('Queens (NC)', 'Queens').replace('VCU', 'Virginia Commonwealth')
                team_name = team_name.replace('Alcorn', 'Alcorn State').replace('Col.', 'College')
                team_name = team_name.replace('Miami (FL)', 'Miami').replace('Ole Miss', 'Mississippi')
                team_name = team_name.replace('UCF', 'Central Florida').replace('Saint Francis (PA)', 'Saint Francis')
                team_name = team_name.replace('ETSU', 'East Tennessee State').replace('SIUE', 'SIU Edwardsville')

                team_names.append(team_name)
                team_scores.append(score.text.strip())

        # Save data to Excel
        scores_df = pd.DataFrame({'Team Name': team_names, 'Team Score': team_scores})
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        scores_df.to_excel(output_file, index=False)
        print(f"Saved NCAA scores to {output_file}")
        return output_file
    else:
        print(f"Failed to scrape NCAA scores: HTTP {response.status_code}")
        return None

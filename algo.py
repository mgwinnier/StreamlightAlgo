import os
import pandas as pd
from odds import scrape_odds_to_excel


def parse_data_from_file(file_path, date):
    """Parse the input data file and process odds into a structured Excel file."""
    directory_name = os.path.join('.', date.replace('/', '-'))
    os.makedirs(directory_name, exist_ok=True)

    # File paths
    odds_filename = os.path.join(directory_name, f"odds-{date}.xlsx")
    processed_filename = os.path.join(directory_name, f"processed_data-{date}.xlsx")

    # Scrape odds data
    scrape_odds_to_excel(date, odds_filename)

    # Read data from the input file
    with open(file_path, 'r') as file:
        raw_data = file.read()

    match_data = raw_data.split('##############################')
    results = []

    for match in match_data:
        if not match.strip():
            continue
        lines = match.strip().split('\n')
        if len(lines) < 10:
            print("Unexpected format in segment:\n", match)
            continue

        try:
            # Extract team details
            team1 = lines[0].split('(')[0].strip()
            team2 = lines[2].split('(')[0].strip()
            efg_statement = lines[4]
            efg_team = efg_statement.split(': ')[1].split(' by')[0].strip()
            team1_score = float(lines[8].split(':')[1].strip())
            team2_score = float(lines[10].split(':')[1].strip())
            team1_srs = float(lines[14].split(':')[1].strip())
            team2_srs = float(lines[16].split(':')[1].strip())

            # Compute spreads
            normal_spread_team1 = team1_score - team2_score
            normal_spread_team2 = team2_score - team1_score
            srs_spread_team1 = team1_srs - team2_srs
            srs_spread_team2 = team2_srs - team1_srs

            matchup = f'{team1} vs {team2}'

            # Append to results
            results.append({
                'Matchup': matchup,
                'Home/Away': "Away",
                'Team': team1,
                'eFG Statement': efg_team,
                'Team Spread': normal_spread_team1,
                'Team SRS Spread': srs_spread_team1,
            })
            results.append({
                'Matchup': matchup,
                'Home/Away': "Home",
                'Team': team2,
                'eFG Statement': efg_team,
                'Team Spread': normal_spread_team2,
                'Team SRS Spread': srs_spread_team2,
            })

        except Exception as e:
            print(f"Error processing match data: {e}")

    # Create a DataFrame
    df = pd.DataFrame(results)

    # Add VLOOKUP formulas
    for idx, row in df.iterrows():
        excel_row = idx + 2  # Excel rows start at 1
        if row['Home/Away'] == "Away":
            df.at[idx, 'Vegas Spread'] = f'=IFERROR(VLOOKUP(C{excel_row},\'[odds-{date}.xlsx]Sheet1\'!$A:$B,2,FALSE), G{excel_row + 1}*-1)'
        else:
            df.at[idx, 'Vegas Spread'] = f'=IFERROR(VLOOKUP(C{excel_row},\'[odds-{date}.xlsx]Sheet1\'!$A:$B,2,FALSE), G{excel_row - 1}*-1)'
    for idx in range(len(df)):
        excel_row = idx + 2  # Excel rows start at 1
        df.at[idx, 'Actual Score'] = f"=VLOOKUP(C{excel_row},'[results-{date}.xlsx]Sheet1'!$A:$B,2,FALSE)"

    # Save to Excel
    if not df.empty:
        os.makedirs(os.path.dirname(processed_filename), exist_ok=True)
        df.to_excel(processed_filename, index=False, engine='openpyxl')
        print(f"Processed data saved to {processed_filename}")
    else:
        print("No data available to save.")
    return df

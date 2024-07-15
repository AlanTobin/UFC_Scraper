import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import string
import csv
import webbrowser
import os
from pathlib import Path


url = "http://www.ufcstats.com/statistics/fighters"

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

fighters = []
base_url = 'http://www.ufcstats.com/statistics/fighters?char='

for char in string.ascii_lowercase:
#pagination setup
    url = base_url + char + '&page=all'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    fighter_html_cards = soup.find_all('tr', class_='b-statistics__table-row')
    for card in fighter_html_cards:
        fighter = {}
    # name of fighter
        if (card.find('a', class_='b-link_style_black') != None):
            fighter_page_url = requests.get(card.find('a', class_='b-link_style_black')['href'])
            fighter_soup = BeautifulSoup(fighter_page_url.text, 'html.parser')
            fighter_name = fighter_soup.find('span', class_='b-content__title-highlight').text.strip()
    # most recent opponent   
            recent_opponent = 'None'
            try:
                info_card_1 = fighter_soup.find('td', class_='b-fight-details__table-col l-page_align_left').text
                info_card_1 = info_card_1.strip().split()
                info_card_1 = ' '.join(info_card_1[2:])
                recent_opponent = info_card_1
            except:
                pass
    # decision
            W_L = ''
            try:
                decision = fighter_soup.find('i', class_='b-flag__text').text
            except: 
                decision = 'N/A'
            W_L = decision
    # last date fought
            last_date_fought = ''
            dates = fighter_soup.find_all('p', class_='b-fight-details__table-text')
            date_identification = re.compile(r'\b[A-Z][a-z]{2}\. \d{2}, \d{4}\b')
            dates = [tag.text.strip() for tag in dates if date_identification.match(tag.text.strip())]
            try:
                last_date_fought = dates[0]
            except:
                last_date_fought = 'N/A'
    # average rounds fought
            average_rounds = 0
            try:
                rounds = fighter_soup.find_all('p', class_='b-fight-details__table-text')
            except Exception as e: 
                 print(e)
            def convert_to_int(text):
                if text.strip().isdigit():
                    # Attempt to convert to integer
                    return int(text.strip())
                elif text.strip() == '--':
                    return 0
            rounds = [convert_to_int(el.text.strip()) for el in rounds]
            try:
                rounds[:] = (value for value in rounds if value != None)
            except:
                pass
            rounds = rounds[8::9]
            try:
                temp_avg_rounds = sum(rounds)/len(rounds)
            except:
                temp_avg_rounds = 0 
            average_rounds = temp_avg_rounds
    # Record
            record = ''
            record = fighter_soup.find('span', class_='b-content__title-record').text.strip()
            record = record[7:]
    # Dictionary updation       
            if last_date_fought != 'N/A':
                date_comparison = datetime.strptime(last_date_fought, '%b. %d, %Y')
                current_date = datetime.now()
                if date_comparison >= current_date:
                    fighter['Name'] = fighter_name
                    fighter['Last/upcoming opponent'] = recent_opponent + "(upcoming)"
                    fighter['Decision'] = W_L
                    fighter['Last/upcoming date of fight'] = last_date_fought + "(upcoming)"
                    fighter['Average rounds fought'] = average_rounds
                    fighter['Record'] = record
                else:
                    fighter['Name'] = fighter_name
                    fighter['Last/upcoming opponent'] = recent_opponent
                    fighter['Decision'] = W_L
                    fighter['Last/upcoming date of fight'] = last_date_fought
                    fighter['Average rounds fought'] = average_rounds
                    fighter['Record'] = record
            if (fighter):
                fighters.append(fighter)
                print(fighter)


def generate_html_table(csv_file_path):
    html_content = ""
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            html_content += f"""
                <tr>
                    <td>{row[0]}</td>
                    <td>{row[1]}</td>
                    <td>{row[2]}</td>
                    <td>{row[3]}</td>
                    <td>{row[4]}</td>
                    <td>{row[5]}</td>
                </tr>
            """
    return html_content

def save_html(html_content, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"HTML file '{output_file}' has been generated successfully.")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent

    fieldnames = ['Name', 'Last/upcoming opponent', 'Decision', 'Last/upcoming date of fight', 'Average rounds fought', 'Record']
    csv_file_path = base_dir / 'ufcFighters.csv'
    output_html_file = base_dir / 'Bootstrap Dashboard' / 'output.html'
    index_file_path = base_dir / 'Bootstrap Dashboard' / 'index.html'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)       
        writer.writeheader()        

        for fighter in fighters:
            writer.writerow(fighter)
    print(f"CSV file '{csv_file_path}' has been generated successfully.")
    
    html_content = generate_html_table(csv_file_path)
    
    save_html(html_content, output_html_file)


    with open(output_html_file, 'r') as file:
        output_content = file.read()

    with open(index_file_path, 'r') as file:
        index_content = file.readlines()

    start_insert = None
    end_insert = None
    for i, line in enumerate(index_content):
        if '<tbody id="tableBody">' in line:
            start_insert = i + 1
        if '</tbody>' in line and start_insert is not None:
            end_insert = i
            break

    if start_insert is not None and end_insert is not None:
        index_content[start_insert:end_insert] = []

    if start_insert is not None:
        index_content[start_insert:start_insert] = [output_content]
    else:
        print("Insertion point not found in index.html")

    with open(index_file_path, 'w') as file:
        file.writelines(index_content)
    
    webbrowser.open('file://' + str(index_file_path))
    
    os.remove(csv_file_path)

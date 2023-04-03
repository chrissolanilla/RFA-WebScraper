import requests
import pandas as pd
import cloudscraper
import json 
import csv 
from bs4 import BeautifulSoup

# Replace this list with the top 100 most popular zip codes in the US
zip_codes = [11101, 33172, 79936,
90011,
60629,
90650,
90201,
77084,
92335,
78521,
77449,
78572,
90250,
90280,
11226,
90805,
91331,
8701,   
90044,
92336,
926,
94565,
10467,
92683,
75052,
91342,
92704,
30044,
10025,
92503,
92804,
78577,
75217,
92376,
93307,
10456,
10002,
91911,
91744,
75070,
77036,
93722,
92345,
60618,
93033,
93550,
95076,
11230,
11368,
37013,
11373,
79912,
37211,
30043,
11206,
10453,
92154,
11355,
95823,
77479,
91706,
10458,
92553,
90706,
23464,
11212,
60617,
91709,
11214,
11219,
91910,
22193,
77429,
93535,
66062,
93257,
30349,
60647,
77584,
10452,
77573,
11377,
11207,
77494,
75211,
11234,
28269,
11235,
94544,
10029,
60625,
89110,
92509,
77083,
91335,
85364,
87121,
10468,
90255,
93065,
91710,
10462]

base_url = "https://rfaforlife.com/wp-json/physicians/v1/find/?lat=&lan=&procedure=30&zip={}&radius=100"

data = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
scraper = cloudscraper.create_scraper(browser=headers)

for zip_code in zip_codes:
    url = base_url.format(zip_code)
    response = scraper.get(url)
    if response.status_code == 200:
        json_data = response.json()
        html_content = json_data['data']
        soup = BeautifulSoup(html_content, 'html.parser')
        doctors_divs = soup.find_all('div', class_='finder-results__item')
        if len(doctors_divs) > 0:
            for doctor_div in doctors_divs:
                doctor_info = {}
                doctor_info['Doctor Name'] = doctor_div.find('h5', class_='title').text.strip()
                info_list = doctor_div.find('div', class_='finder-results__information-list')

                address = info_list.find_all('span')[1].text.strip().replace('\r\n', ', ')
                doctor_info['Address'] = address

                specialty = info_list.find_all('span')[3].text.strip()
                doctor_info['Specialty'] = specialty

                institution = info_list.find_all('span')[5].text.strip()
                doctor_info['Institution'] = institution

                contact = info_list.find_all('span')[7].text.strip()
                doctor_info['Phone Number'] = contact

                doctor_info['Zip Code'] = zip_code

                data.append(doctor_info)
        else:
            print(f"No doctors data found for zip code {zip_code}. Skipping.")
    else:
        print(f"Error fetching data for zip code {zip_code}. Skipping.")

df = pd.DataFrame(data)
df.to_csv("doctors_data.csv", index=False)
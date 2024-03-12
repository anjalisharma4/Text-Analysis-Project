import pandas as pd
from bs4 import BeautifulSoup
import requests
import openpyxl
input_file = "Input.xlsx"
df = pd.read_excel(input_file)
print(len(df))
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    try:
        webpage = requests.get(url).text
        soup = BeautifulSoup(webpage, 'html.parser')
        # print(soup.find('h1'), row['URL_ID'])
        article_title = soup.find('h1').text
        print(article_title)
        print(f'urlid-->{url_id}')
        element_list = soup.find_all('div', class_='td-post-content')
        for i in element_list:
            article_text = i.get_text("|", strip=True)
            print(article_text)

            content = f"{article_title}\n{article_text}"

            with open(f"{url_id}.txt", 'w', encoding='utf-8') as file:
                file.write(content)

    except Exception as e:
        print(f"Error occurred while processing URL '{url}': {e}")
        continue

print("Extraction completed.")


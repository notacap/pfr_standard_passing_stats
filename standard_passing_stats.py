from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import os

def scrape_data():
    # Set up Selenium WebDriver
    options = Options()
    options.headless = True
    # options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    # Path to your ChromeDriver
    driver_path = r'C:\chromedriver-win64\chromedriver.exe'  # Adjust this path to your ChromeDriver location

    # Initialize WebDriver using Service object
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the page
    url = 'https://www.pro-football-reference.com/years/2023/passing.htm'
    driver.get(url)

    # Get the page source and close the browser
    html = driver.page_source
    driver.quit()

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Update the ID to the table ID containing the data you want to scrape
    table = soup.find('table', {'id': 'passing'})

    if table:

        # Extract the header row from the <thead> section
        header_row = table.find('thead').find('tr')
        header_cols = header_row.find_all(['th', 'td'])
        column_names = [ele.text.strip() for ele in header_cols]
        keep_indices = [i for i, name in enumerate(header_cols) if name.text.strip() not in ['Rk', 'QBrec']]
        column_names = [name for name in column_names if name not in ['Rk', 'QBrec']]

        # Find all rows in the table body, excluding those with class containing 'thead'
        rows = [row for row in table.find('tbody').find_all('tr') if 'thead' not in ' '.join(row.get('class', []))]
        

        data = []
        for row in rows:
            cols = row.find_all(['th', 'td'])
            row_data = [ele.text.strip() for ele in cols]

            # Filter for 'QB' in 'Pos' column (5th column)
            if row_data[4] == 'QB':
                # Omit rows where 'Att' is <= 10 (10th column)
                if int(row_data[9]) > 10:
                    filtered_row_data = [row_data[i] for i in keep_indices]
                    data.append(filtered_row_data)
                    

        

        # Creating a DataFrame with the extracted column names
        df = pd.DataFrame(data, columns=column_names)

        output_dir = r'C:\Users\PC\Desktop\code\data_files'
        if not os.path.exists(output_dir):
                os.makedirs(output_dir)

        # Save the DataFrame to the CSV file in the specified directory
        df.to_csv(os.path.join(output_dir, 'standard_passing_stats.csv'), index=False)
    else:
        print("Table not found!")

if __name__ == '__main__':
    scrape_data()
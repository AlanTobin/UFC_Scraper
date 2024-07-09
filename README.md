# UFC Dashboard Project

## Overview

This project aims to create a dashboard that displays UFC fighter statistics scraped from UFC Stats website. The dashboard is designed to visualize and display fighter information such as names, recent opponents, fight decisions, dates of last fights, average rounds fought, and overall records.

## Features

-   Scrapes data from UFC Stats website using Python and BeautifulSoup.
-   Generates a CSV file (`ufcFighters.csv`) containing fighter statistics.
-   Converts the CSV data into an HTML table (`output.html`) for display in the dashboard.
-   Integrates the HTML table into `index.html` using Python scripting.
-   Opens the dashboard (`index.html`) in the default web browser.

## Requirements

-   Python 3.x
-   Requests library (`pip install requests`)
-   BeautifulSoup library (`pip install beautifulsoup4`)

## Setup

1.  Clone the repository:
    
    bash
    
    Copy code
    
    `git clone https://github.com/your-username/ufc-dashboard.git `<br />`
cd ufc-dashboard` 
    
3.  Install dependencies:
    
    `pip install requests beautifulsoup4` 
    
4.  Run the script to generate the dashboard:
    
    `python ufcScrapper.py` 
    
5.  Once the script completes, it will open `index.html` in your default web browser automatically.
    

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Acknowledgments

-   Thanks to [UFC Stats](http://www.ufcstats.com/) for providing the data.
-   Built as a learning project by Alan Tobin.
-   Utilized Bootstrap and dashboard template created by https://github.com/codzsword/

----------

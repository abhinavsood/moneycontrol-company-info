# moneycontrol-company-info
A program that reads a text file containing a list of stocks, looking for ISIN numbers on each line and looks up the contact information for the company and its registrar on MoneyControl.com, and saves everything in a nice CSV file

## Usage
`python moneycontrol.py <input_text_filename> <output_csv_filename>`

## Dependencies
Program uses `requests` and `BeautifulSoup` modules which can be installed as follows:
```
[sudo] pip install requests
[sudo] pip install beautifulsoup4
```

## Input file format
Input text file should have one stock per line. The program looks for the ISIN number on each line in the format `ISIN:<ISIN Number>` so as long as there is an ISIN number in this format, it doesn't matter what else is present on the line.

## Output file format
Output file is a CSV file containing the following fields
* ISIN
* Company Name
* Company Address
* Company City
* Company State
* Company PIN
* Company Telephone
* Company Fax
* Company Email
* Company Website
* Registrar Name
* Registrar Address
* Registrar City
* Registrar PIN
* Registrar State
* Registrar Telephone
* Registrar Fax
* Registrar Email
* Registrar Website

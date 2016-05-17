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

A sample input file may look like this:

```
ASTRA MICROWAVE PRODUCTS LIMITED (ISIN:INE386C01029)
BERGER PAINTS INDIA LIMITED (ISIN:INE463A01038)
Whatever Stock (ISIN:INE757A01017)
Company Name (ISIN:INE220B01022)
FORCE MOTORS LTD (ISIN:INE451A01017)
GATI LIMITED (ISIN:INE152B01027)
```

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

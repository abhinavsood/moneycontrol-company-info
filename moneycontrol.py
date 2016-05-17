import requests, re, json, sys, csv, logging
from bs4 import BeautifulSoup

# Configure the format and level of detail for logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# Fields to be written to the output CSV file
fieldNames = [
    'ISIN',
    'Company Name',
    'Company Address',
    'Company City',
    'Company State',
    'Company PIN',
    'Company Telephone',
    'Company Fax',
    'Company Email',
    'Company Website',
    'Registrar Name',
    'Registrar Address',
    'Registrar City',
    'Registrar PIN',
    'Registrar State',
    'Registrar Telephone',
    'Registrar Fax',
    'Registrar Email',
    'Registrar Website'
]


# Pattern to match and get ISIN from a given string
p   = re.compile('ISIN:([\d\w]+)\)[ ]*$')

# URL to search for Link corresponding to given ISIN
url = "http://www.moneycontrol.com/mccode/common/autosuggesion.php"

def successfulRequest( status_code ):
    '''Checks if the HTTP request was successful or not'''
    
    return status_code == 200


def getISIN( line ):
    '''Returns the ISIN number if found on the given line'''
    
    return p.search(line).group(1)


def getLinkSource( responseText ):
    '''Extracts the MoneyControl URL to lookup contact information from the search suggestion response'''
    
    # Extract valid JSON object from the Response Text
    valid_json  = re.sub("^[\d|\w]+\(\[|\]\)$", "", responseText)
    
    # Return the link source 
    return json.loads( valid_json )['link_src'].strip()



def getDetails( ISIN ):
    '''Fetches company and registrar contact details from MoneyControl.com for given ISIN number'''
    
    allDetails = {}
    
    payload = {
        "callback":   "suggest1",
        "type":       "1",
        "format":     "json",
        "query":      ISIN
    }
    
    r = requests.get(url, payload)

    linkSource = ''
    if successfulRequest( r.status_code ):
        linkSource = getLinkSource( r.text )

        if linkSource:
            r = requests.get( linkSource )
            if successfulRequest( r.status_code ):
                soup = BeautifulSoup( r.text, "lxml" )
                
                stockName = soup.find('h1', {'class': 'b_42'}).text
        
                # The container DIV that contains company information
                parentDiv   = soup.find('div', id = 'acc_hd8' )
            
                # The DIV that contains company information
                companyDiv  = parentDiv.find_all('div', attrs = {'class': 'w252 FL'})
            
                # The DIV that contains registrar information
                registrarDiv  = parentDiv.find_all('div', attrs = {'class': 'w230 FL PR25 PL25'})
            
                # Company information
                [compAddress,
                compCity,
                compState,
                compPIN,
                compTel,
                compFax,
                compEmail,
                compWeb] = [ info.string for info in companyDiv[0].find_all('div', attrs = {'class': 'FL w160 gD_12'}) ]

                # Registrar Information
                [regName,
                regAddress,
                regCity,
                regState,
                regTel,
                regFax,
                regEmail,
                regWeb] = [ info.string for info in registrarDiv[0].find_all('div', attrs = {'class': 'FL w150 gD_12'}) ]
    
                # Assemble
                allDetails['ISIN']                  = ISIN
                
                allDetails['Company Name']          = stockName
                allDetails['Company Address']       = compAddress
                allDetails['Company City']          = compCity
                allDetails['Company State']         = compState
                allDetails['Company PIN']           = compPIN
                allDetails['Company Telephone']     = compTel
                allDetails['Company Fax']           = compFax
                allDetails['Company Email']         = compEmail
                allDetails['Company Website']       = compWeb
                
                allDetails['Registrar Name']        = regName
                allDetails['Registrar Address']     = regAddress
                
                # This field is usually in the format [<City Name> - <PIN Code>]
                # so extract details as appropriate
                [
                    allDetails['Registrar City'],
                    allDetails['Registrar PIN']
                ] = [info.strip() for info in regCity.split('-')] if '-' in regCity else [None, None]
                
                
                allDetails['Registrar State']       = regState
                allDetails['Registrar Telephone']   = regTel
                allDetails['Registrar Fax']         = regFax
                allDetails['Registrar Email']       = regEmail
                allDetails['Registrar Website']     = regWeb
    
    return allDetails


def main():
    '''To execute, run: python  moneycontrol.py  <input_text_filename>  <output_CSV_filename>'''
    
    if len( sys.argv ) != 3:
        logging.error( main.__doc__ )
        sys.exit(-1)

    # Read the text file and store all found ISIN numbers in this list
    ISINList    = []
    
    # List of dictionaries, each of which contains the company and registrar contact details for a given stock
    detailsList = []
    
    # List of ISIN numbers for which the program couldn't find details automatically, must look these up manually
    manualList  = []
    
    logging.info('Reading file: {0:s}'.format( sys.argv[1] ) )
    with open( sys.argv[1], 'r' ) as input_file:
        for line in input_file:
            ISINList.append( getISIN(line) )
    
    logging.info('Starting to collect details...')
    for isin in ISINList:
        
        logging.info('Collecting details for ISIN: {0:s}'.format( isin ) )
        try:
            detailsList.append( getDetails( isin ) )
        
        except ValueError, e:
            logging.error('Error collecting data for ISIN: {0:s}'.format( isin ) )
            manualList.append( isin )
    
    logging.info('Writing details to CSV file: {0:s}'.format( sys.argv[2] ) )
    with open( sys.argv[2], 'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames = fieldNames )
        writer.writeheader()
        writer.writerows( detailsList )
    
    logging.info('{0:s} created successfully'.format( sys.argv[2] ) )
    
    if len( manualList ):
        logging.info('\nSearch for contact details for the following stocks manually:')
        logging.info( manualList )
    
if __name__ == '__main__': main()
    
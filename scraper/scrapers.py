import logging
import pdb
from bs4 import BeautifulSoup
import utils

def searchEmpty(soup):
    """
    Checks our html soup for the empty search results
    """
    err_msg = "Your search keyword did not return any matches. Please try a different search keyword."
    search_empty = err_msg in soup.text
    if search_empty:
        logging.info("Found the empty search text.")
    return search_empty


def extractCaseFromRow(row, headers, case_type):
    """
    Extracts a case from a row
    """
    logging.debug("Extracting case from row")
    cells = [td.text for td in row.findAll('td')]
    case_info = dict(zip(headers, cells))
    case = utils.normaliseCaseFields(case_info, case_type)
    return case


def extractCases(soup, case_type):

    logging.debug("Extracting cases now")
    table = soup.find('table', {'class' : 'list-orders'})
    
    headers = [th.text for th in table.findAll('th')]
    headers = utils.normaliseHeaders(headers)
    rows = table.findAll('tr')[1:]
    cases = [extractCaseFromRow(row, headers, case_type)
            for row in rows]
    return cases


def pageHasTable(soup):
    has_table = soup.find('table', {'class' : 'list-orders'}) is not None
    if not has_table:
        logging.info("Page doesn't have table")
    return has_table

def blankPage(page):
    soup = BeautifulSoup(page, 'html.parser')
    return not pageHasTable(soup)

def failedSearchPage(page):
    soup = BeautifulSoup(page, 'html.parser')
    return searchEmpty(soup)

def scrapePage(case_type, page):
    soup = BeautifulSoup(page, 'html.parser')
    logging.debug("Validating page for scraping")
    if searchEmpty(soup) or not pageHasTable(soup):
        err_msg = "No pages left. Exiting now"
        raise Exception(err_msg)

    return extractCases(soup, case_type)

import logging
import web
import database as db
import scraper_utils as scr
import file_handling
import os
import utils


def getPages(min_year, max_year, case_type):
    for year in range(min_year, max_year+1):
        num = 1
        pagesLeft = True        
        while pagesLeft:        
            try:
                page = web.getPage(year, case_type, num)
                file_handling.savePage(case_type, page, year, num)
            except (web.FailedSearchException,
                    web.EmptyPageException) as e:
                logging.info("Failed to get page: {0}".format(e))
                break
            except Exception as e:
                logging.error(e)
                break
            num += 1
        logging.info("Saved files for year: {0}".format(year))
    logging.info("Finished scraping run")
    return

def run():
    # Check last stored case page
    # Get the case page for the last
    # Get any additional case pages
    getPages(2014, 2017, 'tribunal')

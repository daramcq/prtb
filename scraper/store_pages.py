import logging
import os
import cases.constants as case_constants
import web
import scrapers as scr
import file_handling
import utils
import constants

def savePages(year, case_type, starting_num):
    pagesLeft = True
    while pagesLeft:        
        try:
            page = web.getPage(year, case_type, starting_num)
            print "Got page"
            file_handling.savePage(case_type, page, year, starting_num)
        except (web.FailedSearchException,
                web.EmptyPageException) as e:
            logging.info("Failed to get page: {0}".format(e))
            break
        except Exception as e:
            logging.error(e)
            break
        starting_num += 1
        logging.info("Saved files for year: {0}".format(year))
    logging.info("Finished scraping run")
    return

def run():
    # Check last stored case page
    # Get the case page for the last
    # Get any additional case pages
    case_types = [tp[1] for tp in case_constants.CASE_TYPES]
    print case_types
    for case_type in case_types:
        latest_year = file_handling.findLastYearSaved(case_type)
        print "Latest year!", latest_year
        for year in range(latest_year, constants.MAX_YEAR+1):
            print year
            latest_page = file_handling.findLastPageSaved(case_type, year)
            print "Latest page!", latest_page
            savePages(year, case_type, latest_page)

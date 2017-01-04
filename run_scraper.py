import logging
import web
import database as db
import scrapers as scr
import file_handling
import os
import utils

def scrapePages(case_type, min_year, max_year):
    total = 0
    for year in range(min_year, max_year+1):
        year_count = 0
        for fpath in os.listdir("{0}/{1}".format(case_type,
                                                 str(year))):
            with open("{0}/{1}/{2}".format(case_type,
                                           year, fpath)) as f:
                cases = scr.scrapePage(case_type, f.read())
                msg = "Attempting to store {0} cases".format(len(cases))
                logging.debug(msg)
                year_count += len(cases)
                if case_type == "adjudication":
                    [db.storeAdjudication(case) for case in cases]
                else:
                    [db.storeTribunal(case) for case in cases]
        print("Found {0} cases for year {1}".format(year_count,
                                                    year))
        total += year_count
    print("Found {0} cases in total for years {1}-{2}".format(total, min_year, max_year))
    return


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
    logging.basicConfig(level=logging.INFO)
    #getPages(2014, 2017, 'tribunal')
    scrapePages("tribunal", 2014,2016)
    
    # for year in [2014, 2015, 2015]:
    #     cases = db.getAdjudications(limit=500, year=year)
    #     print("{0}|{1}|{0}".format(("="*25),year))
    #     utils.produceQuickSubjectBreakdown(cases)

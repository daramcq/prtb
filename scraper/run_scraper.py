import logging
import scrapers as scr
import os
import utils

def scrapePages(case_type, min_year, max_year):
    total = 0
    for year in range(min_year, max_year+1):
        for fpath in os.listdir("{0}/{1}".format(case_type, str(year))):
            scrape_page(fpath)
        total += year_count
    print("Found {0} cases in total for years {1}-{2}".format(total, min_year, max_year))
    return

def scrape_page(case_type, year, num):
    with open("scraper/saved_pages/{0}/{1}/{2}.html".format(case_type, year, num)) as f:
        cases = scr.scrapePage(case_type, f.read())
        msg = "Attempting to store {0} cases".format(len(cases))
        logging.debug(msg)
        # Attempt to store as an Adjudication/Tribunal model
        #saveCases
def saveCase(case):
    applicants = save_applicant_parties(case.get("applicant_parties"))
    respondents = save_respondent_parties(case.get("respondent_parties"))
    subjects = save_subjects(case.get("subject_of_dispute"))
    case = save_case(case)
    case.applicant = applicants
    case.respondent = respondent
    


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    scrapePages("tribunal", 2014,2016)
    
    # for year in [2014, 2015, 2015]:
    #     cases = db.getAdjudications(limit=500, year=year)
    #     print("{0}|{1}|{0}".format(("="*25),year))
    #     utils.produceQuickSubjectBreakdown(cases)

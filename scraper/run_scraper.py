import logging
import os

from django.db import IntegrityError

from cases.models import Case, Subject, Party

import scrapers as scr
import utils
import constants

def scrapePages(case_type, min_year, max_year):
    """
    Extract cases from stored pages and save them
    to the database.
    """
    total = 0
    for year in range(min_year, max_year+1):
        for fpath in os.listdir("{0}/{1}".format(case_type, str(year))):
            cases = scrape_page(fpath)
            for case in cases:
                saveCase(case, case_type)
        total += year_count
    print("Found {0} cases in total for years {1}-{2}".format(total, min_year, max_year))
    return


def scrapePage(case_type, year, num):
    """
    Extract all cases from a given page
    """
    path = constants.BASE_FILE_DIR + "/{0}/{1}/{2}.html"
    with open(path.format(case_type, year, num)) as f:
        cases = scr.scrapePage(case_type, f.read())        
        return cases


def saveCase(case_info, case_type):
    """
    Save a case_info dict as a Case, with associated
    Subject and Party keys
    """
    case = Case(case_type=case_type,
                dr_no=case_info.get('dr_no'),
                determination_order=case_info.get('determination_order'),
                date=case_info.get('order_date'))
    if case_type == 'tribunal':
        case.tr_no = case_info.get('tr_no')
        case.tribunal_report = case_info.get('tribunal_report')
    case.save()
    subjects = [Subject.objects.get_or_create(name=subj)[0]
                for subj in case_info.get('subject_of_dispute')]

    parties = case_info.get("parties")
    respondents = [Party.objects.get_or_create(**resp)[0]
                   for resp in parties.get("respondent")]
    applicants = [Party.objects.get_or_create(**resp)[0]
                   for resp in parties.get("applicant")]

    for resp in respondents:
        case.respondents.add(resp)

    for app in applicants:
        case.applicants.add(app)

    for subj in subjects:
        case.subjects_of_dispute.add(subj)

    case.save()
    


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    scrapePages("tribunal", 2014,2016)
    
    # for year in [2014, 2015, 2015]:
    #     cases = db.getAdjudications(limit=500, year=year)
    #     print("{0}|{1}|{0}".format(("="*25),year))
    #     utils.produceQuickSubjectBreakdown(cases)

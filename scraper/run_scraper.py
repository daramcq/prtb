import logging
import os

from django.db import IntegrityError

from cases.models import Case, Subject, Party

import scrapers as scr
import utils


def saveObjects(object_list):
    for object in object_list:
        saved_obj = object.get_or_create()
    try:
        object.save()
    except IntegrityError:
        print "Duplicant entry found, proceeding"

def scrapePages(case_type, min_year, max_year):
    total = 0
    for year in range(min_year, max_year+1):
        for fpath in os.listdir("{0}/{1}".format(case_type, str(year))):
            cases = scrape_page(fpath)
            for case in cases:
                saveCase(case, case_type)
        total += year_count
    print("Found {0} cases in total for years {1}-{2}".format(total, min_year, max_year))
    return

def scrape_page(case_type, year, num):
    path = "scraper/saved_pages/{0}/{1}/{2}.html"
    with open(path.format(case_type, year, num)) as f:
        cases = scr.scrapePage(case_type, f.read())
        
        return cases
        # Attempt to store as an Adjudication/Tribunal model
        # saveCases
        # msg = "Attempting to store {0} cases".format(len(cases))
        # logging.debug(msg)



def saveCase(case_info, case_type):
    case = Case(case_type=case_type,
                dr_no=case_info.get('dr_no'),
                determination_order=case_info.get('determination_order'),
                date=case_info.get('order_date'))
    case.save()
    subjects = [Subject.objects.get_or_create(name=subj)[0]
                for subj in case_info.get('subject_of_dispute')]
    print subjects
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

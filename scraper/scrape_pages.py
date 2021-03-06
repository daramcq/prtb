import logging
import os
import sys

from django.db import IntegrityError

from cases.models import Case, Subject, Party
import cases.constants as case_constants

import scrapers as scr
import constants

def scrapePages(case_type, min_year, max_year):
    """
    Extract cases from stored pages and save them
    to the database.
    """
    total = 0
    for year in range(min_year, max_year+1):
        for fpath in os.listdir("{0}/{1}".format(case_type, str(year))):
            cases = scrapePage(fpath)
            for case in cases:
                saveCase(case, case_type)
        total += year_count
    print("Found {0} cases in total for years {1}-{2}".format(total, min_year, max_year))
    return


def caseExists(case_info):
    try:
        print "Checking if case exists"
        case = Case.objects.get(dr_no=case_info.get('dr_no'),
                                date=getCaseDate(case_info))
        print "Case {0} - {1} already exists!".format(case.dr_no, case.date)
        return True
    except Case.DoesNotExist:
        print "Case not found, saving now"
        return False


def getCaseDate(case_info):
    return case_info.get('order_date',
                         case_info.get('hearing_date'))


def saveCase(case_info, case_type):
    """
    Save a case_info dict as a Case, with associated
    Subject and Party keys
    """
    if caseExists(case_info):
        return

    case = Case(case_type=case_type,
                dr_no=case_info.get('dr_no'),
                date=getCaseDate(case_info),
                determination_order=case_info.get('determination_order'))

    if case_type == 'tribunal':
        case.tr_no = case_info.get('tr_no')
        case.tribunal_report = case_info.get('tribunal_report')
    print "Saving case: {0} | {1}".format(case.dr_no, case.date)
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


def scrapePage(case_type, path):
    """
    Extract all cases from a given page
    """
    with open(path) as f:
        cases = scr.scrapePage(case_type, f.read())        
        return cases


def run():
    try:
        case_types = [tp[1] for tp in case_constants.CASE_TYPES]

        for case_type in case_types:
            case_dir = constants.BASE_FILE_DIR + "/{0}".format(case_type)
            # For each year
            for year in os.listdir(case_dir):
                year_path = case_dir + "/{0}".format(year)
                for page in os.listdir(year_path):
                    page_path = year_path+"/{0}".format(page)
                    print "Scraping page: {0}".format(page_path)
                    cases = scrapePage(case_type, page_path)
                    print "{0} | {1} - {2} | {3} cases".format(case_type, year,
                                                               page, len(cases))
                    for c in cases:
                        saveCase(c, case_type)

    except Exception as e:
        print "Failed with exception: {0}".format(e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        cases_saved = Case.objects.count()
        total = 5066
        percentage = 100 * round((float(cases_saved)/total), 4)
        print "\n================================================\n"
        print "{0} cases saved.".format(cases_saved)
        print "That's {0}% of the total - {1}".format(percentage, total)
        print "\n================================================\n"

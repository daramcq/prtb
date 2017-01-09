import os
import logging

import constants

def getCaseDir(case_type):
    dir = constants.BASE_FILE_DIR + "/{0}".format(case_type)
    return dir

def savePage(case_type, page, year, num):
    """
    Saves a html page to a directory in format
    {case_type}/{year}/{num}.html
    """
    filename = "{0}.html".format(num)
    
    dir = getCaseDir(case_type)
    path = dir +"/{0}/{1}.html".format(year, str(num))
    logging.info("Saving page: {0}".format(path))

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(path, 'w') as f:
        f.write(page.encode('utf8'))

    logging.info("Wrote file: {0}".format(path))
    return

def getLatest(str_nums):
    nums = [int(num) for num in str_nums]
    latest_year = sorted(nums)[-1]
    return latest_year


def findLastYearSaved(case_type):
    """
    Finds the last year for which we have entries for a 
    given case_type
    """
    case_dir = getCaseDir(case_type)
    latest_year = getLatest(os.listdir(case_dir))
    return latest_year


def findLastPageSaved(case_type, year):
    """
    Identifies the last page saved for a given case_type and 
    returns the year and page_num as ints.
    """
    #TODO: Add error handling when no pages saved
    # for a given year
    case_dir = getCaseDir(case_type)
    print case_dir
    files = os.listdir(case_dir + "/{0}".format(year))
    print files
    drop_ext = lambda s: s.split('.')[0]
    # Remove the ".html" extension for file names
    files = [drop_ext(f) for f in files]
    latest_page = getLatest(files)
    return latest_page

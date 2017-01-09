import logging
import requests
import backoff
import scrapers as scr

import constants

class EmptyPageException(Exception):
    pass

class FailedSearchException(Exception):
    pass

@backoff.on_exception(backoff.expo, EmptyPageException, max_tries=3)
def getPage(year, case_type, num=1):
    print "Getting page"
    url = constants.TRIBUNAL_URL if case_type is "tribunal" else constants.ADJUDICATION_URL
    url = url + "/{0}?page={1}".format(year, num)
    req = requests.get(url)
    resp_text = req.text

    if req.status_code is not 200:
        err_msg = "Received status code {0} for page {1}".format(req.status_code, url)
        raise requests.Exception(err_msg)

    if scr.blankPage(resp_text):
        err_msg = "Blank page - Year {0} | Num {1}.".format(year, num)
        raise EmptyPageException(err_msg)

    if scr.failedSearchPage(resp_text):
        err_msg = "Failed Search Page - Year {0} | Num {1}".format(year, num)
        raise FailedSearchException(err_msg)
    
    logging.info("Got page - Year {0} | Num {1} ".format(year, num))
    return resp_text

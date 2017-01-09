from django.conf import settings

BASE_FILE_DIR = "{0}/scraper/saved_pages".format(settings.PROJECT_PATH)

BASE_URL = "http://www.rtb.ie/dispute-resolution"

ADJUDICATION_URL = BASE_URL + "/dispute-resolution/adjudication-orders/"

TRIBUNAL_URL = BASE_URL + "/tribunals/tribunal-reports-orders/"

MAX_YEAR = 2017

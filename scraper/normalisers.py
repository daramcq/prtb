from datetime import datetime
from functools import partial

from split_parties import splitCaseParties
from split_subject import splitCaseSubject

is_date = lambda k: "date" in k
is_order_num = lambda k: k in ("dr_no", "tr_no")
is_parties = lambda k: "parties" in k
is_subject = lambda k: "subject" in k
no_normalisation_needed = lambda k: True
normalise_order_num = lambda v: v.strip()
no_op = lambda v: v


def normaliseDate(d):
    date = datetime.strptime(d, "%d %B, %Y")
    return datetime.strftime(date, "%Y-%m-%d")


def normaliseCaseFields(case, case_type):
    """
    Normalise all fields of a case dict to
    match data requirements
    """
    # Apply case type to split Parties func so we
    # can be case type agnostic here
    split_case_parties = partial(splitCaseParties, case_type)
    normalise_fns = [(is_date, normaliseDate),
                     (is_order_num, normalise_order_num),
                     (is_parties, split_case_parties),
                     (is_subject, splitCaseSubject),
                     (no_normalisation_needed, no_op)]

    def apply_if_matches(fns, (k,v)):
        for f in fns:
            if f[0](k):
                return f[1](v)

    field_normalisers = partial(apply_if_matches, normalise_fns)
    try:
        normalised_vals = map(field_normalisers, case.items())
    except Exception as e:
        print "Unable to format case: {0}".format(case)
        raise e
    case = dict(zip(case.keys(), normalised_vals))
    return case


def normaliseHeaders(headers):
    def normaliseHeader(header):
        return header.lower().replace(" ", "_").replace(".","")
    return [normaliseHeader(h) for h in headers]

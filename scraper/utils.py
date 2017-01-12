from datetime import datetime
from functools import partial
from tabulate import tabulate

from cases import constants
from synonyms import SYNONYMS

class UnrecognisableStringException(Exception):
    pass

def normaliseDate(d):
    date = datetime.strptime(d, "%d %B, %Y")
    return datetime.strftime(date, "%Y-%m-%d")

is_date = lambda k: "date" in k

is_order_num = lambda k: k in ("dr_no", "tr_no")

normalise_order_num = lambda v: v.strip()

is_parties = lambda k: "parties" in k

is_subject = lambda k: "subject" in k

no_normalisation_needed = lambda k: True

no_op = lambda v: v

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
    normalised_vals = map(field_normalisers, case.items())
    case = dict(zip(case.keys(), normalised_vals))
    return case


def normaliseHeaders(headers):
    def normaliseHeader(header):
        return header.lower().replace(" ", "_").replace(".","")
    return [normaliseHeader(h) for h in headers]


def splitCaseSubject(subject):
    """
    Splits the Subject of Dispute string of an adjudication
    into an array of individual subjects, normalised.
    """
    def red_herring(s):
        return "standard and maintenance" in s \
            or "wear and tear" in s

    def parsed_str(s):
        return s.lower().strip().strip('.').replace("-", " ")

    def lookup_synonyms(s):
        return SYNONYMS.get(s, s) 
    
    # Need to filter out empty strings
    case_subjects = [parsed_str(s) for
                     s in subject.split(',')
                     if len(parsed_str(s)) > 0]
    for i, subj in enumerate(case_subjects):
        if " and " in subj and not red_herring(subj):
            case_subjects.pop(i)
            case_subjects += [s.strip() for s
                              in subj.split(" and ")]

    case_subjects = list(set(case_subjects))
    case_subjects = map(lookup_synonyms, case_subjects)

    return case_subjects


def anySynonymMatches(s, syn_key):
    return any([syn in s.lower()
                for syn in SYNONYMS.get(syn_key)])


def splitPartiesString(parties_str):
    """
    Splits the party_str into an applicant/appellant and a respondent
    """
    dash_locations = [i for i, l in enumerate(parties_str)
                      if l == '-']

    if len(dash_locations) < 2:
        return parties_str.split('-')
    
    for dash_loc in dash_locations:
        first, second = parties_str[:dash_loc], parties_str[dash_loc+1:]
        if anySynonymMatches(first.lower(), "applicant") \
           and anySynonymMatches(second.lower(), "respondent"):
            return [first, second]

    err_msg = "Unable to split string effectively: {0}".format(parties_str)
    raise UnrecognisableStringException(err_msg)

def formatPartyString(party_str, business_role=True):
    """
    Takes a party string and returns an array of dicts
    """
    role = matchBusinessRole(party_str)
    if ":" in party_str:
        party_str = party_str.split(":")[1]
    party_names = party_str.lower().split(",")
    if not business_role:
        return [{"name": nm.strip()} for nm in party_names]
    return [{"name": nm.strip(), "role" : role}
             for nm in party_names]

def matchBusinessRole(s):
    """
    Takes a party string and matches it to a business role
    """
    for role in constants.BUSINESS_ROLES:
        if anySynonymMatches(s, role[1]):
            return role[1]
    return "unknown"


def splitCaseParties(case_type, parties_str):
    """
    Split the party string into applicant and respondent 
    and format these so that we have a dict with applicant
    and respondent as keys
    """
    desired_fields = ['applicant', 'respondent']
    role_needed = case_type == 'adjudication'
    parties = splitPartiesString(parties_str)    
    role_matches = {}
    for field in desired_fields:
        for party in parties:
            if anySynonymMatches(party, field):
                # We expect 'landlord' and 'tenant' info to be included
                # only in Adjudication cases
                formatted_str = formatPartyString(party, business_role=role_needed)
                role_matches[field] = formatted_str
                desired_fields.remove(field)
                parties.remove(party)

    # If we have an unfilled role and an unattributed party,
    # match the remaining
    if parties and desired_fields and len(parties) == 1 and len(desired_fields) == 1:
        role_matches[desired_fields[0]] = formatPartyString(parties[0],
                                                            business_role=role_needed)
                
    return role_matches    

def produceQuickSubjectBreakdown(cases):
    subject_registry = {}
    for case in cases:
        subjects = splitCaseSubject(case.get("subject_of_dispute"))
        for subj in subjects:
            if subj in subject_registry:
                subject_registry[subj] += 1
            else:
                subject_registry[subj] = 1
    for k, v in subject_registry.items():
        if v < 5:
            subject_registry.pop(k)
    table = tabulate(subject_registry.items())
    print table

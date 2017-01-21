from cases import constants
from synonyms import SYNONYMS

from utils import anySynonymMatches

def splitCaseSubject(subject):
    """
    Splits the Subject of Dispute string of an adjudication
    into an array of individual subjects, normalised.
    """
    def red_herring(s):
        return "standard and maintenance" in s \
            or "wear and tear" in s

    def clean_str(s):
        return s.lower().strip().strip('.').replace("-", " ")

    def lookup_synonyms(s):
        return SYNONYMS.get(s, s) 

    def splitAndParseString(s, divider):
        return [clean_str(s) for s in subject.split(divider)
                if len(clean_str(s)) > 0]
    # Need to filter out empty strings
    case_subjects = splitAndParseString(subject, ',')
    if len(case_subjects) == 1:
        case_subjects = splitAndParseString(subject, ';')
    for i, subj in enumerate(case_subjects):
        if " and " in subj and not red_herring(subj):
            case_subjects.pop(i)
            case_subjects += [s.strip() for s
                              in subj.split(" and ")]

    case_subjects = list(set(case_subjects))
    case_subjects = map(lookup_synonyms, case_subjects)

    return case_subjects

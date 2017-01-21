from cases import constants
from synonyms import SUBJECT_SYNONYMS

from utils import anySynonymMatches


def splitAndParseString(subject, divider):
    return [clean_str(s) for s in subject.split(divider)
            if len(clean_str(s)) > 0]
    
def clean_str(s):
    return s.lower().strip().strip('.').replace("-", " ")

def lookupSynonyms(s):
    for key, synonyms in SUBJECT_SYNONYMS.items():
        if any([s == syn for syn in synonyms]):
            return key
    return s

def red_herring(s, conj):
    subjects = [subj.format(conj)
                for subj in ["wear{0}tear","standard{0}maintenance"]]
    return any([subj in s for subj in subjects])


def splitCaseSubject(subject_str):
    """
    Splits the Subject of Dispute string of a case
    into an array of individual subjects, normalised.
    """    
    # First try splitting on comma
    case_subjects = splitAndParseString(subject_str, ',')

    # If it's not any better, try splitting on semi-colon
    if len(case_subjects) == 1:
        case_subjects = splitAndParseString(subject_str, ';')

    # Now split on and/& if present
    for i, subj in enumerate(case_subjects):
        for conj in (" and ", " & "):
            if conj in subj and not red_herring(subj, conj):
                case_subjects.pop(i)
                case_subjects += [s.strip() for s
                                  in subj.split(conj)]

    case_subjects = list(set(case_subjects))
    case_subjects = map(lookupSynonyms, case_subjects)

    return case_subjects

from tabulate import tabulate
from synonyms import SYNONYMS


class UnrecognisableStringException(Exception):
    pass

def anySynonymMatches(s, syn_key):
    return any([syn in s.lower()
                for syn in SYNONYMS.get(syn_key)])

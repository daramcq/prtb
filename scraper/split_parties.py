from cases import constants
from synonyms import SYNONYMS

from utils import anySynonymMatches, UnrecognisableStringException


def splitPartiesString(parties_str):
    """
    Splits the party_str into an applicant/appellant and a respondent
    """
    def bothRolesMatched(first, second):
        return anySynonymMatches(first.lower(), "applicant") \
               and anySynonymMatches(second.lower(), "respondent")

    def anyRoleMatched(parties_str):
        return anySynonymMatches(parties_str.lower(), "applicant") \
               or anySynonymMatches(parties_str.lower(), "respondent")
    
    for separator in SYNONYMS.get("separator"):
        dash_locations = [i for i, l in enumerate(parties_str)
                          if l == separator]

        if len(dash_locations) is 1:
            return parties_str.split(separator)
    
        for dash_loc in dash_locations:
            first, second = parties_str[:dash_loc], parties_str[dash_loc+1:]
            if bothRolesMatched(first, second):
                return [first, second]

    try:
        parties = splitPartiesOnSpaces(parties_str)
        return parties
    except UnrecognisableStringException as e:
        pass

    if anyRoleMatched(parties_str):
        return [parties_str]


    err_msg = "Unable to split string effectively: {0}".format(parties_str)
    raise UnrecognisableStringException(err_msg)

def splitPartiesOnSpaces(parties_str):
    """
    Splits a case parties_str on spacing, find the locations of
    the applicant and respondent roles and splitting at the start
    of the second
    """
    def findFirstMatch(s, matching_strs):
        for m in matching_strs:
            if m in s.lower():
                return s.lower().find(m)

    roles = ['applicant', 'respondent']
    role_locations = [findFirstMatch(parties_str, SYNONYMS.get(r)) for r in roles if anySynonymMatches(parties_str, r)]
    if role_locations and len(role_locations)>1:
        print role_locations
        first = parties_str[:role_locations[1]-1]
        second = parties_str[role_locations[1]:]
        return [first, second]
    else:
        raise UnrecognisableStringException("Unable to split into parties on spaces")
    

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

    if not parties_str:
        return {
            'applicant': [],
            'respondent': []
        }

    parties = splitPartiesString(parties_str)
        
    if not parties:
        raise Exception("Parties fucked: {0}".format(parties_str))

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
    if len(parties) == 1 and len(desired_fields) == 1:
        role_matches[desired_fields[0]] = formatPartyString(parties[0],
                                                            business_role=role_needed)
    # If we have an unfilled role but no parties remaining
    # return the unfilled role as an empty list 
    if not parties and len(desired_fields) == 1:
        role_matches[desired_fields[0]] = []

    return role_matches    

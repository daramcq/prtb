from unittest import TestCase
from bs4 import BeautifulSoup

from scraper import split_parties

class TestSplitParties(TestCase):
    """
    Test the split_parties module
    """

    def test_splitCaseParties(self):
        """
        Test the splitCaseParties method by asserting that a string of parties will
        be accurately split into individual parties in format:
        { "applicant_parties" : [{"role": "landlord", "name": "mark kinsella"}],
          "respondent_parties" : [{"role": "tenant", "name": "amanda little"},
                                  {"role": "tenant", "name": "lawrence Griffin"}]}
        """
        parties_str = "Applicant Lanldord: Mark K - Respondent Tenants: Amanda L, Lawrence G"
        expected = { "applicant" : [{"role": "landlord", "name": "mark k"}],
                     "respondent" : [{"role": "tenant", "name": "amanda l"},
                                     {"role": "tenant", "name": "lawrence g"}]}
        result = split_parties.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

        parties_str = "Applicant Tenant: Alan O'K- Respondent Landlord: Noel McC"
        expected = { "applicant" : [{"role": "tenant", "name": "alan o'k"}],
                     "respondent" : [{"role": "landlord", "name": "noel mcc"}]}

        result = split_parties.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

        parties_str = "Applicant Tenant(s): Ahmed G, Fadumo I - Respondant Landlord: Audrey K"
        expected = { "applicant" : [{"role": "tenant", "name": "ahmed g"},
                                            {"role": "tenant", "name": "fadumo i"}],
                     "respondent" : [{"role": "landlord", "name": "audrey k"}]}

        result = split_parties.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

        parties_str = "Applicant Landlord(s): Theresa L, Francis W - Respondant Tenant: Denise n"
        expected = {
            "applicant" : [{"role": "landlord", "name": "theresa l"},
                                   {"role": "landlord", "name": "francis w"}],
            "respondent" : [{"role": "tenant", "name": "denise n"}]
        }
        result = split_parties.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

        parties_str = "Applicant landlord: Geraldine R - Andrey T"
        expected = {
            "applicant" : [{"role": "landlord", "name": "geraldine r"}],
            "respondent" : [{"role": "unknown", "name": "andrey t"}]
        }
        result = split_parties.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

    def test_splitPartiesStringPoorSpelling(self):
        """
        Ensures splitPartiesString can cope with poor spelling
        """
        parties_str = "Applicant Tenant : Abayomi Ol, Esther Aw - Respondat Landlord : Dermot K"
        expected = {
            "applicant": [{"role": "tenant", "name": "abayomi ol"},
                          {"role": "tenant", "name": "esther aw"}],
            "respondent": [{"role": "landlord", "name": "dermot k"}]
        }
        result = split_parties.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)
        
    def test_splitPartiesStringWithSlash(self):
        """
        Ensures splitPartiesString can cope with slash being used
        as a divider instead of dash
        """
        parties_str = "Appellant: Jurij M / Respondent: Gerry W"
        expected = {
            "applicant": [{"name": "jurij m"}],
            "respondent": [{"name": "gerry w"}]
        }
        result = split_parties.splitCaseParties("tribunal", parties_str)
        self.assertEqual(expected, result)

    def test_splitPartiesStringWithoutDivider(self):
        """
        Ensure splitPartiesString can cope with no divider 
        being present
        """
        parties_str = "Appellant: Denise O'B Respondent: Eugene D, Mary C"
        expected = {
            "applicant": [{"name": "denise o'b"}],
            "respondent": [{"name": "eugene d"},
                           {"name": "mary c"}]
        }
        result = split_parties.splitCaseParties("tribunal", parties_str)
        self.assertEqual(expected, result)

    def test_splitPartiesOnlyOneParty(self):
        """
        Ensures that splitPartiesString can cope with only one
        party being present
        """
        parties_str = "Applicant Tenant(s): Tabata A, Caio N"
        expected = {
            "applicant": [{"role": "tenant", "name": "tabata a"},
                          {"role": "tenant", "name": "caio n"}],
            "respondent": []
        }
        result = split_parties.splitCaseParties('adjudication', parties_str)
        self.assertEqual(expected, result)

    def test_formatPartyString(self):
        """
        Assert that the formatPartyString method will return an array of 
        dict with name and, if specified, a business role
        """
        party_str = "Applicant landlord: Geraldine R"
        expected = [{"name": "geraldine r", "role": "landlord"}]
        self.assertEqual(expected, split_parties.formatPartyString(party_str, True))

    def test_splitPartiesString(self):
        """
        Test the splitPartiesString method by ensuring that party strings 
        with multiple dashes are split correctly, returning arrays 
        of respondent and applicant
        """
        s = "Appellant: Lucy Johnston - Respondent: Mary-Jane Lawrence"
        expected = ["Appellant: Lucy Johnston "," Respondent: Mary-Jane Lawrence"]
        self.assertEqual(expected, split_parties.splitPartiesString(s))

from unittest import TestCase
from scraper import utils
from bs4 import BeautifulSoup

class TestUtils(TestCase):

    def test_normaliseDate(self):
        s = "12 February, 2016"
        expected = "2016-02-12"
        self.assertEqual(expected, utils.normaliseDate(s))


    def test_normaliseHeaders(self):
        headers = ["DR No.", "Subject of Dispute",
                   "Order Date", "Determination Order"]
        expected = ["dr_no", "subject_of_dispute",
                    "order_date", "determination_order"]

        self.assertEqual(expected, utils.normaliseHeaders(headers))


    def test_splitCaseSubject(self):
        """
        Tests the split_case_subject method
        """
        
        s1 = "Deposit retention, Breach of landlord obligations"
        expected = ["deposit retention", "breach of landlord obligations"]
        self.assertEqual(expected, utils.splitCaseSubject(s1))

        s2 = "Deposit retention, Invalid Notice of termination, Standard and maintenance of dwelling, Unlawful termination of tenancy (Illegal eviction)"
        expected = ["deposit retention",
                    "invalid notice of termination",
                    "standard and maintenance of dwelling",
                    "unlawful termination of tenancy"]
        res = utils.splitCaseSubject(s2)
        self.assertTrue(all([exp in res for exp in expected]))

        s3 = "Deposit Retention and Breach of Landlord Obligations, anti-social behaviour"
        expected = ["deposit retention",
                    "breach of landlord obligations",
                    "anti social behaviour"]
        res = utils.splitCaseSubject(s3)
        self.assertTrue(all([exp in res for exp in expected]))

        s4 = "Rent arrears, Standard and maintenance of Dwelling, Breach of tenant obligations"
        expected = ["rent arrears",
                    "standard and maintenance of dwelling",
                    "breach of tenant obligations"]
        res = utils.splitCaseSubject(s4)
        self.assertTrue(all([exp in res for exp in expected]))

        s5 = "Unlawful termination of tenancy (Illegal eviction), Deposit retention, Rent more than market rate"
        expected = ["unlawful termination of tenancy",
                    "deposit retention",
                    "rent more than market rate"]
        res = utils.splitCaseSubject(s5)
        self.assertTrue(all([exp in res for exp in expected]))

        s6 = "Unlawful termination of tenancy (Illegal eviction)"
        expected = ["unlawful termination of tenancy"]
        res = utils.splitCaseSubject(s6)
        self.assertEqual(expected, res)

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
        result = utils.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

        parties_str = "Applicant Tenant: Alan O'K- Respondent Landlord: Noel McC"
        expected = { "applicant" : [{"role": "tenant", "name": "alan o'k"}],
                     "respondent" : [{"role": "landlord", "name": "noel mcc"}]}

        result = utils.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

        parties_str = "Applicant Tenant(s): Ahmed G, Fadumo I - Respondant Landlord: Audrey K"
        expected = { "applicant" : [{"role": "tenant", "name": "ahmed g"},
                                            {"role": "tenant", "name": "fadumo i"}],
                     "respondent" : [{"role": "landlord", "name": "audrey k"}]}

        result = utils.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

        parties_str = "Applicant Landlord(s): Theresa L, Francis W - Respondant Tenant: Denise n"
        expected = {
            "applicant" : [{"role": "landlord", "name": "theresa l"},
                                   {"role": "landlord", "name": "francis w"}],
            "respondent" : [{"role": "tenant", "name": "denise n"}]
        }
        result = utils.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)

        parties_str = "Applicant landlord: Geraldine R - Andrey T"
        expected = {
            "applicant" : [{"role": "landlord", "name": "geraldine r"}],
            "respondent" : [{"role": "unknown", "name": "andrey t"}]
        }
        result = utils.splitCaseParties("adjudication", parties_str)
        self.assertEqual(expected, result)


    def test_formatPartyString(self):
        """
        Assert that the formatPartyString method will return an array of 
        dict with name and, if specified, a business role
        """
        party_str = "Applicant landlord: Geraldine R"
        expected = [{"name": "geraldine r", "role": "landlord"}]
        self.assertEqual(expected, utils.formatPartyString(party_str, True))

    def test_splitPartiesString(self):
        """
        Test the splitPartiesString method by ensuring that party strings 
        with multiple dashes are split correctly, returning arrays 
        of respondent and applicant
        """
        s = "Appellant: Lucy Johnston - Respondent: Mary-Jane Lawrence"
        expected = ["Appellant: Lucy Johnston "," Respondent: Mary-Jane Lawrence"]
        self.assertEqual(expected, utils.splitPartiesString(s))

    def test_normaliseOrderNums(self):
        data = {
            "tr_no": "TTTTTT  ",
            "dr_no": "  GGGGGG"
        }
        exp = {
            "tr_no": "TTTTTT",
            "dr_no": "GGGGGG"
        }
        
        self.assertEqual(exp, utils.normaliseCaseFields(data, "adjudication"))

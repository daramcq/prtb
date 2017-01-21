from unittest import TestCase

from scraper import split_subject

class TestSplitSubject(TestCase):
    """
    Test the split_subject module
    """

    def test_splitCaseSubject(self):
        """
        Tests the split_case_subject method
        """
        
        s1 = "Deposit retention, Breach of landlord obligations"
        expected = ["deposit retention", "breach of landlord obligations"]
        self.assertEqual(expected, split_subject.splitCaseSubject(s1))

        s2 = "Deposit retention, Invalid Notice of termination, Standard and maintenance of dwelling, Unlawful termination of tenancy (Illegal eviction)"
        expected = ["deposit retention",
                    "invalid notice of termination",
                    "standard and maintenance of dwelling",
                    "unlawful termination of tenancy"]
        res = split_subject.splitCaseSubject(s2)
        self.assertTrue(all([exp in res for exp in expected]))

        s3 = "Deposit Retention and Breach of Landlord Obligations, anti-social behaviour"
        expected = ["deposit retention",
                    "breach of landlord obligations",
                    "anti social behaviour"]
        res = split_subject.splitCaseSubject(s3)
        self.assertTrue(all([exp in res for exp in expected]))

        s4 = "Rent arrears, Standard and maintenance of Dwelling, Breach of tenant obligations"
        expected = ["rent arrears",
                    "standard and maintenance of dwelling",
                    "breach of tenant obligations"]
        res = split_subject.splitCaseSubject(s4)
        self.assertTrue(all([exp in res for exp in expected]))

        s5 = "Unlawful termination of tenancy (Illegal eviction), Deposit retention, Rent more than market rate"
        expected = ["unlawful termination of tenancy",
                    "deposit retention",
                    "rent more than market rate"]
        res = split_subject.splitCaseSubject(s5)
        self.assertTrue(all([exp in res for exp in expected]))

        s6 = "Unlawful termination of tenancy (Illegal eviction)"
        expected = ["unlawful termination of tenancy"]
        res = split_subject.splitCaseSubject(s6)
        self.assertEqual(expected, res)

    def test_splitCaseSubjectOnSemicolon(self):
        """
        Ensure that splitCaseSubject can handle a semi-colon
        being used as a separator
        """
        subj_str = "Standard and maintenance of dwelling; Damage in excess of normal wear and tear; Rent arrears; Invalid Notice of termination; Rent more than market rate; Breach of landlord obligations"
        expected = ["standard and maintenance of dwelling", "damage in excess of normal wear and tear", "rent arrears", "invalid notice of termination", "rent more than market rate", "breach of landlord obligations"]
        res = split_subject.splitCaseSubject(subj_str)
        print res
        self.assertItemsEqual(expected, res)

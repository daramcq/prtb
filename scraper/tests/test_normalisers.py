from unittest import TestCase

from scraper import normalisers


class TestNormalisers(TestCase):
    """
    Test the normalisers module.
    """
    
    def test_normaliseDate(self):
        s = "12 February, 2016"
        expected = "2016-02-12"
        self.assertEqual(expected, normalisers.normaliseDate(s))

    def test_normaliseOrderNums(self):
        data = {
            "tr_no": "TTTTTT  ",
            "dr_no": "  GGGGGG"
        }
        exp = {
            "tr_no": "TTTTTT",
            "dr_no": "GGGGGG"
        }
        
        self.assertEqual(exp, normalisers.normaliseCaseFields(data, "adjudication"))

        
    def test_normaliseHeaders(self):
        headers = ["DR No.", "Subject of Dispute",
                   "Order Date", "Determination Order"]
        expected = ["dr_no", "subject_of_dispute",
                    "order_date", "determination_order"]

        self.assertEqual(expected, normalisers.normaliseHeaders(headers))

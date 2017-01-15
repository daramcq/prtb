from unittest import TestCase

# Create your tests here.
import unittest
from scraper import utils
from scraper import scrapers as scr
from bs4 import BeautifulSoup


class TestScrapers(TestCase):

    def test_searchEmpty(self):
        html = "<html><body>{0}</body></html>"
        err_msg = "Your search keyword did not return any matches. Please try a different search keyword."

        soup = BeautifulSoup(html.format(""), 'html.parser')
        self.assertFalse(scr.searchEmpty(soup))
        
        soup = BeautifulSoup(html.format(err_msg), 'html.parser')
        self.assertTrue(scr.searchEmpty(soup))

    def test_pageHasTable(self):
        html = "<html><body>{0}</body></html>"
        table = "<table class='list-orders'><th><td>Table Header</td></th><tr><td>Table Cell</td></tr></table>"

        soup = BeautifulSoup(html.format(""), 'html.parser')
        self.assertFalse(scr.pageHasTable(soup))

        soup = BeautifulSoup(html.format(table), 'html.parser')
        self.assertTrue(scr.pageHasTable(soup))

    def test_extractAdjudications(self):
        html = "<html><body>{0}</body></html>"
        table = "<table class='list-orders'>{0}{1}</table>"
        headers = "<tr><th>DR No.</th><th>Subject of Dispute</th><th>Parties</th><th>Order Date</th><th>Determination Order</th></tr>"
        rows = "<tr><td>AAA-43-22</td><td>Rent Withholding</td><td>Applicant Tenant: Alan O'K- Respondent Landlord: Noel McC</td><td>12 February, 2016</td><td>www.rtb.ie/some/url</td></tr>"

        soup = BeautifulSoup(html.format(table.format(headers,rows)), 'html.parser')
        cases = scr.extractCases(soup, "adjudication")
        expected = [{
            u"dr_no": u"AAA-43-22",
            u"subject_of_dispute": [u"rent withholding"],
            u"order_date": u"2016-02-12",
            u"determination_order": u"www.rtb.ie/some/url",
            u"parties" : {
                u"applicant" : [{
                    u"role": u"tenant",
                    u"name": u"alan o'k"
                }],
                u"respondent" : [{
                    u"role": u"landlord", u"name": u"noel mcc"
                }]
            }
        }]
        self.assertEqual(expected, cases)

    def test_extractTribunalReports(self):
        html = "<html><body>{0}</body></html>"
        table = "<table class='list-orders'>{0}{1}</table>"
        headers = '<tr><th>TR No.</th><th>DR No.</th><th>Parties</th><th>Subject of Dispute</th><th>Hearing Date</th><th style="text-align:center">Tribunal Report</th><th style="text-align:center">Determination Order</th></tr>'
        rows = '<tr><td>TR-ABAA-22</td><td>0413-05463</td><td>Appellant: Lucy Johnston - Respondent: Mary-Jane Lawrence</td><td>Standard and maintenance of dwelling, Rent arrears and overholding  </td><td>8 January, 2014</td><td><div><a>www.rtb.ie/tribunal/report</a></div></td><td><div><a>www.rtb.ie/some/url</a></div></td></tr>'

        soup = BeautifulSoup(html.format(table.format(headers,rows)), 'html.parser')
        cases = scr.extractCases(soup, "tribunal")
        expected = {"tr_no": "TR-ABAA-22",
                    "dr_no": "0413-05463",
                    "subject_of_dispute": ["standard and maintenance of dwelling",
                                           "rent arrears",
                                           "overholding"],
                    "parties": {
                        "applicant" : [{"name": u"lucy johnston"}],
                        "respondent": [{"name": u"mary-jane lawrence"}]
                    },
                    "hearing_date": "2014-01-08",
                    "tribunal_report" : "www.rtb.ie/tribunal/report",
                    "determination_order": "www.rtb.ie/some/url"}

        for k,v in cases[0].items():
            self.assertEqual(expected.get(k), v)

        self.assertDictEqual(expected, cases[0])


from django.test import TestCase

from cases.models import Case, Subject, Party
# Create your tests here.
class TestCase(TestCase):

    def test_saveCase(self):
        case_info = {
            u'tribunal_report': u'http://www.rtb.ie/docs/default-source/tribunal-reports/tr0oct.docx?sfvrsn=0',
            u'dr_no': u'114-195',
            u'hearing_date': '2013-05-03',
            u'parties': {
                'applicant': [
                    {'name': u'colin f (receiver)'},
                    {'name': u'luke c (receiver)'},
                    {'name': u'michael f'}
                ],
                'respondent': [
                    {'name': u'karolina p'},
                    {'name': u'ibrahim m'}]},
            u'tr_no': u'065-0021',
            u'subject_of_dispute': [u'deposit retention'],
            u'determination_order': u'http://www.rtb.ie/docs/default-source/determination-orders/tr.pdf?sfvrsn=0'
        }

        cases = Case.objects.all()
        self.assertEqual(0, len(cases))

        case = Case(case_type="tribunal",
                    dr_no=case_info.get('dr_no'),
                    tr_no=case_info.get('tr_no'),
                    date=case_info.get('hearing_date'),
                    determination_order=case_info.get('determination_order'))
        case.save()
        cases = Case.objects.all()
        self.assertEqual(1, len(cases))

        subjects = Subject.objects.all()
        self.assertEqual(0, len(subjects))
        subjects = [Subject.objects.get_or_create(name=subj)[0]
                    for subj in case_info.get('subject_of_dispute')]
        subjects = Subject.objects.all()
        self.assertEqual(1, len(subjects))

        parties = Party.objects.all()
        self.assertEqual(0, len(parties))

        for resp in case_info.get('parties').get("respondent"):
            Party.objects.get_or_create(**resp)[0]

        for app in case_info.get('parties').get("applicant"):
            Party.objects.get_or_create(**app)[0]

        parties = Party.objects.all()
        self.assertEqual(5, len(parties))

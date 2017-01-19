from django.db.models import Count

"""
What are the most common issues for landlords to take a case over?

- Yearly breakdown

What are the most common issues for tenants to take a case over?

- Yearly breakdown

What landlords are involved with the most cases - as applicant/as respondent?

"""
qs = Subject.objects.annotate(Count('case'))
qs.first().case__count
Subject.objects.get(name='rent arrears').case_set.count()
subs = Subject.objects.annotate(num_cases=Count('case'))
subs.order_by('-num_cases')
subs.filter(case__case_type='adjudication').filter(case__applicants__role='landlord')
# Number of adjudication cases where applicants are landlord
Case.objects.filter(case_type='adjudication').filter(applicants__role='landlord').distinct().count()



top_10_dispute_subjects = """ SELECT subject.name, cnt.subject_id, count(*) AS count 
                              FROM cases_subject AS subject JOIN cases_case_subjects_of_dispute AS cnt
                              ON subject.id = cnt.subject_id
                              GROUP BY cnt.subject_id ORDER BY COUNT DESC LIMIT 10;
                          """

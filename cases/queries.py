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

#Get cases where applicant is a landlord:
"""
SELECT C.id, A.case_id, P.name, P.role FROM cases_case C JOIN cases_case_applicants A ON C.id = A.case_id JOIN cases_party P ON A.party_id = P.id WHERE P.role='landlord' limit 5;

"""
#GET TOP subjects of dispute for cases where the applicant is a landlord
"""
SELECT S.name, count(*) AS count FROM cases_subject S JOIN cases_case_subjects_of_dispute CS ON S.id=CS.subject_id WHERE CS.case_id IN (SELECT C.id FROM cases_case C JOIN cases_case_applicants A ON C.id = A.case_id JOIN cases_party P ON A.party_id = P.id WHERE P.role='landlord') GROUP BY CS.subject_id ORDER BY count DESC LIMIT 10;
"""


#GET TOP subjects of dispute for cases where the applicant is a tenant
"""
SELECT S.name, count(*) AS count FROM cases_subject S JOIN cases_case_subjects_of_dispute CS ON S.id=CS.subject_id WHERE CS.case_id IN (SELECT C.id FROM cases_case C JOIN cases_case_applicants A ON C.id = A.case_id JOIN cases_party P ON A.party_id = P.id WHERE P.role='tenant') GROUP BY CS.subject_id ORDER BY count DESC LIMIT 10;
"""


#GET top subjects of dispute for cases in 2016 where applicant is a tenant
"""
SELECT S.name, count(*) AS count FROM cases_subject S JOIN cases_case_subjects_of_dispute CS ON S.id=CS.subject_id WHERE CS.case_id IN (SELECT C.id FROM cases_case C JOIN cases_case_applicants A ON C.id = A.case_id JOIN cases_party P ON A.party_id = P.id WHERE P.role='tenant' AND C.date BETWEEN '2016-01-01' AND '2016-12-31') GROUP BY CS.subject_id ORDER BY S.name DESC LIMIT 20;
"""


#Get subjects of dispute for REIT
"""
SELECT S.name, count(*) AS count FROM cases_subject S JOIN cases_case_subjects_of_dispute CS ON S.id=CS.subject_id WHERE CS.case_id IN (SELECT C.id FROM cases_case C JOIN cases_case_applicants A ON C.id = A.case_id JOIN cases_party P ON A.party_id = P.id WHERE P.name LIKE '%REIT%') GROUP BY CS.subject_id ORDER BY count DESC;
"""

#Get number of cases by month
"""
SELECT extract(year_month FROM date) AS yearmonth, count(dr_no) as count 
FROM cases_case GROUP BY yearmonth ORDER BY yearmonth
"""

#Get number of cases by subject by month
"""
SELECT extract(year_month FROM date) AS yearmonth, S.name, count(*) as count FROM cases_case C JOIN cases_case_subjects_of_dispute CS ON C.id=CS.case_id JOIN cases_subject S ON CS.subject_id=S.id GROUP BY yearmonth, S.name ORDER BY yearmonth, count desc;
"""


#Get number of cases by month where applicant is tenant
"""
SELECT extract(year_month FROM date) AS yearmonth, count(*) as count FROM cases_case C JOIN cases_case_subjects_of_dispute CS ON C.id=CS.case_id JOIN cases_subject S ON CS.subject_id=S.id JOIN cases_case_applicants A ON CS.case_id=A.case_id JOIN cases_party P ON A.party_id=P.id WHERE P.role='tenant' GROUP BY yearmonth ORDER BY yearmonth, count desc;
"""

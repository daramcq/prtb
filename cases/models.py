from __future__ import unicode_literals

from django.db import models

import constants

class Party(models.Model):
    """
    Party model, stresenting a party to a dispute.
    Can be either a landlord or a tenant.
    """
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10,
                            choices=constants.BUSINESS_ROLES,
                            null=True)
    def __str__(self):
        return '<Party: {0} - {1}>'.format(self.name, self.role)
    
class Subject(models.Model):
    """
    Subject model, the subject of a dispute
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return '<Subject: {0}>'.format(self.name)

class Case(models.Model):
    """
    Base model for Adjudication and Tribunal Cases,
    with common attributes.
    """
    dr_no = models.CharField(max_length=20)
    subject_of_dispute = models.ManyToManyField(Subject)
    determination_order = models.CharField(max_length=100)
    
    class Meta:
        abstract = True

class Adjudication(Case):
    """
    Adjudication model, refers to a PRTB Adjudication.
    """
    applicant = models.ManyToManyField(Party,
                                       related_name="applicant_parties")
    respondent = models.ManyToManyField(Party,
                                        related_name="adj_respondent_parties")
    order_date = models.DateField()

    def __str__(self):
        return '<Adjudication: {0}>'.format(self.dr_no)
    

class Tribunal(Case):
    """
    Tribunal model, refers to a PRTB Tribunal.
    """
    tr_no = models.CharField(max_length=20)
    appellant = models.ManyToManyField(Party,
                                       related_name="appellant_parties")
    respondent = models.ManyToManyField(Party,
                                        related_name="trb_respondent_parties")
    tribunal_report = models.CharField(max_length=100)
    hearing_date = models.DateField()

    def __str__(self):
        return '<Tribunal: {0}>'.format(self.tr_no)

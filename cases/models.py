from __future__ import unicode_literals

from django.db import models

import constants

class Party(models.Model):
    """
    Party model, representing a party to a dispute.
    Can be either a landlord or a tenant.
    """
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20,
                            choices=constants.BUSINESS_ROLES,
                            null=True)
    class Meta:
        unique_together = ["name", "role"]

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.role)
    
class Subject(models.Model):
    """
    Subject model, the subject of a dispute
    """
    name = models.CharField(max_length=150,
                            unique=True)

    def __str__(self):
        return '{0}'.format(self.name)

class Case(models.Model):
    """
    Case model that covers both Adjudication and
    Tribunal Cases.
    """
    dr_no = models.CharField(max_length=50)
    tr_no = models.CharField(max_length=50,
                             null=True)
    case_type=models.CharField(max_length=15,
                               choices=constants.CASE_TYPES)
    subjects_of_dispute = models.ManyToManyField(Subject)
    determination_order = models.CharField(max_length=300)
    tribunal_report = models.CharField(max_length=300,
                                       null=True)
    applicants = models.ManyToManyField(Party,
                                        related_name='applicants')
    respondents = models.ManyToManyField(Party,
                                         related_name='respondents')
    date = models.DateField()

    class Meta:
        unique_together = ["dr_no", "case_type", "date"]
    
    def __str__(self):
        return "{0} - {1}".format(self.case_type,
                                  self.dr_no)

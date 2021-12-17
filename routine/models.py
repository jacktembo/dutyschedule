from django.contrib.auth.models import User
from django.db import models
from dutyrota.utils import *

from datetime import date, datetime

from django.db import models


class Week(models.Model):
    week_number = models.IntegerField()

    def __str__(self):
        return str(self.week_number)


class School(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo = models.ImageField(blank=True, null=True)
    headteacher = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    website = models.CharField(max_length=64, blank=True, null=True)
    facebook = models.URLField(max_length=255)
    twitter = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
     verbose_name='Select or create a username', 
     help_text='To create a new username, use the Add button on the right-side of this input field.')
    """an abstract person where different persons type will inherit"""
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    nrc = models.CharField(max_length=12, verbose_name='Your NRC Number')
    birth_date = models.DateField(verbose_name='Date of Birth')
    picture = models.ImageField(blank=True, null=True, verbose_name='Upload the portrait of you face')

    def __str__(self):
        return f"{self.title} {self.user.first_name} {self.user.last_name}"


class TeacherProfile(Person):
    phone_number = models.CharField(max_length=14)
    department = models.CharField(max_length=50)
    email = models.EmailField(max_length=64)

    class Meta:
        verbose_name = 'Teacher'.upper()
        verbose_name_plural = verbose_name + 'S'


class SupervisorProfile(Person):
    phone_number = models.CharField(max_length=14)
    department = models.CharField(max_length=50)
    email = models.EmailField(max_length=64)

    class Meta:
        verbose_name = 'Supervisor'.upper()
        verbose_name_plural = verbose_name + 'S'



class DutyRota(models.Model):
    """Duty Rota for a specific day"""
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name=
    "year for this Duty Schedule")
    term = models.ForeignKey(Term, on_delete=models.CASCADE,
    verbose_name="Select a Term for this Duty Schedule")
    week_number = models.ForeignKey(Week, on_delete=models.CASCADE,
    verbose_name="What Week of the term is this Duty Schedule?", unique=True)
    # Teachers on duty.
    teachers = models.ManyToManyField(
        TeacherProfile, related_name='+', verbose_name='Select Teachers who will be on duty')

    supervisors = models.ManyToManyField(
        SupervisorProfile, related_name='+', verbose_name='Select Supervisors who will be on duty')

    def __str__(self):
        # Date in format like Monday 10 January 2021.
        return f"Week {self.week_number}"

    class Meta:
        verbose_name = 'Duty Schedule'.upper()
        verbose_name_plural = verbose_name + 'S'



class Announcement(models.Model):
    """ Announcements to pupils or staff"""
    subject = models.CharField(max_length=200, verbose_name='Title of the announcement')
    body = models.TextField(verbose_name='Type the detailed announcement here')
    target_audience = models.CharField(max_length=50, choices=[
        ('Students', 'Students'),
        ('Teachers', 'Teachers'),
        ('Supervisors', 'Supervisors')
    ], verbose_name='To whom is this announcement being sent?')
    published_date_time = models.DateTimeField(
        auto_now_add=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'ANNOUNCEMENT'
        verbose_name_plural = verbose_name + 'S'
class LeavePermission(models.Model):
    """Permission for pupils to leave """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    explanation = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    date_leaving = models.DateField()
    time_leaving = models.TimeField()
    date_back = models.DateField()

    def __str__(self):
        return f"From {self.pupil_name}"


class Grade(models.Model):
    grade = models.CharField(max_length=20)

    def __str__(self):
        return self.grade


class PupilProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Select or create a username for this Pupil', 
     help_text='To create a new username, use the Add button on the right-side of this input field.')
    pupil_id = models.CharField(max_length=20, primary_key=True,
    verbose_name='Pupil\'s School ID Number')
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.DateField(verbose_name='Date of Birth', default=datetime(1999, 1, 1))
    picture = models.ImageField(blank=True, null=True, verbose_name='Upload a Portrait Photo')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    parent_phone = models.CharField(max_length=15, verbose_name='Phone number of Parents/Guadians')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'PUPIL'  
        verbose_name_plural = verbose_name + 'S'

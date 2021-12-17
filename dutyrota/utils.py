
""" utility classes and functions that will be used throughout the
project
"""
from django.db import models
from django.contrib.auth.models import User



class Year(models.Model):
    """Represents the year for the duty rota"""
    year = models.IntegerField(default=2021)

    def __str__(self):
        return f"{self.year}"


class Term(models.Model):
    """Represents a school term e.g term 1, term 2 and term 3."""
    term = models.CharField(max_length=10)
    number_of_weeks = 13

    def __str__(self):
        return self.term


class Month(models.Model):
    """
    Represents the month of the year
    """
    month = models.CharField(max_length=20)
    number_of_days = models.IntegerField(default=30)

    def __str__(self):
        return self.month


class Week(models.Model):
    """Represents the week number in a term. There are typically 13 weeks 
    in a standard term"""
    week = models.IntegerField()

    def __str__(self):
        return f"{self.week}"


class Day(models.Model):
    """Represents a day in a week. E.g Monday"""
    day = models.CharField(max_length=20)

    def __str__(self):
        return self.day


class Gender(models.Model):
    gender = models.CharField(max_length=15)

    def __str__(self):
        return self.gender


class Title(models.Model):
    title = models.CharField(max_length=5)

    def __str__(self):
        return self.title


class Province(models.Model):
    """province within a country"""
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class District(models.Model):
    """district within a province"""
    name = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Town(models.Model):
    """town within a district"""
    name = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Address(models.Model):
    """full address of the school"""
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    town = models.ForeignKey(Town, on_delete=models.CASCADE)
    box = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.box}, {self.town} - {self.district} {self.province} Zambia"


class OneTimePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    otp = models.CharField(max_length=10)

    def __str__(self):
        return self.otp

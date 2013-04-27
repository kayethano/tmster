#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django_facebook.models import FacebookProfileModel

SCHOOL_CHOICES = (
	('1','ITESM Campus Monterrey'),
	('2','UDEM'),
	('3','UANL'),
	('4','UR'),
	)

VARIANT_CHOICES = (
	('1','Puntualidad'),
	('2','Desempeño'),
	('3','Accesibilidad'),
	('4','Personalidad'),
	('5','Recomendable'),
	)

class Student(models.Model):
	name = models.CharField(max_length=40)
	school = models.CharField(max_length=2, choices=SCHOOL_CHOICES)
	facebook = models.CharField(max_length=50, blank=True, null=True)
	twitter = models.CharField(max_length=20, blank=True, null=True)

	def __unicode__(self):
		return u'%s' % (self.name)


class Profile(FacebookProfileModel):
	user = models.OneToOneField(User)

	def __unicode__(self):
		return u'%s' % (self.user)


	#Create profile when new user
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	#Signal to create user profile
	post_save.connect(create_user_profile, sender=User)

class Opinion(models.Model):
	variant = models.CharField(max_length=2, choices=VARIANT_CHOICES)
	value = models.BooleanField()

	def __unicode__(self):
		return u'%s' % (self.value)


class Comment(models.Model):
	text = models.CharField(max_length=300)

	def __unicode__(self):
		return u'%s' % (self.text)

class Survey(models.Model):
	user = models.ForeignKey(User)
	student = models.ForeignKey(Student)
	comment = models.ForeignKey(Comment)
	opinion = models.ManyToManyField(Opinion)

	def __unicode__(self):
		return u'%s' % (self.user)



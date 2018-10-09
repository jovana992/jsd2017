import os
from django.db import models
from django.utils import timezone

class Agencija(models.Model):
	naziv=models.CharField(max_length=100, null=True, default=1)
	adresa=models.CharField(max_length=50, null=True)
	telefon=models.IntegerField(max_length=15, null=True)

	'''
	You can chose one of these atributes to be returned instead of type object!
	def __str__(self):
		return self.naziv
		return self.adresa
		return self.telefon
	'''

class Korisnik(models.Model):
	agencija=models.ForeignKey(Agencija, on_delete=models.CASCADE)
	ime=models.CharField(max_length=10, null=True, default=1)
	prezime=models.CharField(max_length=15, null=True)
	adresa=models.CharField(max_length=50, null=True)
	datumRodjenja=models.DateTimeField(null=True, default=timezone.now)
	jmbg=models.IntegerField(default=1, null=True)
	email=models.EmailField(max_length=64, null=False, default=1)
	pol=models.BooleanField(default=1)

	'''
	You can chose one of these atributes to be returned instead of type object!
	def __str__(self):
		return self.agencija
		return self.ime
		return self.prezime
		return self.adresa
		return self.datumRodjenja
		return self.jmbg
		return self.email
		return self.pol
	'''
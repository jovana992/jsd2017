from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone


class Migration(migrations.Migration):

	initial = True

	dependencies = [
	]

	operations = [
		migrations.CreateModel(
			name='Agencija',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('naziv', models.CharField(max_length=100, null=True, default=1)),
				('adresa', models.CharField(max_length=50, null=True)),
				('telefon', models.IntegerField(max_length=15, null=True)),
			],
		),
		migrations.CreateModel(
			name='Korisnik',
			fields=[
				('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('agencija', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Agencija')),
				('ime', models.CharField(max_length=10, null=True, default=1)),
				('prezime', models.CharField(max_length=15, null=True)),
				('adresa', models.CharField(max_length=50, null=True)),
				('datumRodjenja', models.DateTimeField(null=True, default=timezone.now)),
				('jmbg', models.IntegerField(default=1, null=True)),
				('email', models.EmailField(max_length=64, null=False, default=1)),
				('pol', models.BooleanField(default=1)),
			],
		),
	]
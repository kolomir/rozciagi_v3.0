from django.db import models
import socket
import getpass
from django.contrib.auth.models import User


class GrupaRobocza(models.Model):
    nazwa = models.CharField(max_length=15)
    aktywna = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa


class Narzedzia(models.Model):
    grupa = models.CharField(max_length=15)
    uwagi = models.CharField(max_length=150,null=True,blank=True)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.grupa


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dzial = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Przekroje(models.Model):
    przekroj = models.CharField(max_length=7)
    wartosc = models.DecimalField(max_digits=5,decimal_places=1,default=0.0)
    aktywny = models.BooleanField(default=True)

    def __str__(self):
        return self.przekroj


class Listy(models.Model):
    nazwa = models.CharField(max_length=50)
    aktywna = models.BooleanField(default=True)

    def __str__(self):
        return self.nazwa


class Rozciagi(models.Model):

    hostname = socket.gethostname()
    login_username = getpass.getuser()
    user = User.username

    nr_zlecenia = models.CharField(max_length=10)# - form
    nr_pozycji = models.CharField(max_length=250)# - form
    lista = models.ForeignKey(Listy, on_delete=models.CASCADE)# - form
    nr_pracownika = models.DecimalField(max_digits=5,decimal_places=0)# - form
    rozciag = models.DecimalField(max_digits=5,decimal_places=2)# - przetworzone
    przekrojePrzewodow = models.ForeignKey(Przekroje, on_delete=models.CASCADE)# - form
    indeks_kontaktu = models.CharField(max_length=10)# - form                              - dodalbym przedrostek RIM a pole byłoby w formie liczby ???
    poprawkowe = models.BooleanField(default=False)# - przetworzone
    narzedzia = models.CharField(max_length=20)# - form
    grupa_robocza = models.ForeignKey(GrupaRobocza, on_delete=models.CASCADE)# - form
    wysokosc = models.DecimalField(max_digits=4,decimal_places=2,default=0, blank=True, null=True)# - przetworzone
    data_serwis = models.DateField('data serwis', blank=True, null=True)# - form
    data_dodania = models.DateField('data dodania')# - form
    narzedzia_rodzaj = models.ForeignKey(Narzedzia, on_delete=models.CASCADE)# - form
    potwierdzenie = models.BooleanField(default=False)# - przetworzone
    zalogowany_user = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)# - form


    def __str__(self):
        return self.indeks_kontaktu
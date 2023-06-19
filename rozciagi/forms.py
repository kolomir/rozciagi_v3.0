from django.forms import ModelForm
from .models import Rozciagi


#= Rozciągi =======================================================
class RozciagiForm(ModelForm):
    class Meta:
        model = Rozciagi
        fields = ['nr_zlecenia',
                  'nr_pozycji',
                  'lista',
                  'nr_pracownika',
                  'rozciag',
                  'przekrojePrzewodow',
                  'indeks_kontaktu',
                  'poprawkowe',
                  'narzedzia',
                  'grupa_robocza',
                  'wysokosc',
                  'narzedzia_rodzaj',
                  'potwierdzenie']
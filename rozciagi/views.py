from django.shortcuts import render, redirect
from .models import GrupaRobocza, Przekroje, Narzedzia, Author, Rozciagi, Listy, User
from .forms import RozciagiForm
from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import csv


# == WYSZUKANIE AUTORA ====================================================================================
def get_author(user):
    if user.is_anonymous:
        guest_user = User.objects.get(username="guest")  # or whatever ID or name you use for the placeholder user that no one will be assigned
        qs = Author.objects.filter(user=guest_user)
        if qs.exists():
            return qs[0]
        return None
    else:
        qs = Author.objects.filter(user=user)
        if qs.exists():
            return qs[0]
        return None


# == NOWY WPIS ====================================================================================
def nowy_wpis(request):
    form = RozciagiForm(request.POST or None, request.FILES or None)
    lista_rozciagi = Rozciagi.objects.all().order_by('-id')[:1000]
    lista_listy = Listy.objects.filter(aktywna=True)
    lista_przekroje = Przekroje.objects.filter(aktywny=True)
    lista_grupy = GrupaRobocza.objects.filter(aktywna=True)
    lista_rodzaj = Narzedzia.objects.filter(aktywny=True)

    edycja = 0

    moja_Data = datetime.now()
    data_dodania = moja_Data.strftime("%Y-%m-%d")

    #- PRZYGOTOWANIE SESJI ---------------------------------------------------------
    nr_zlecenia_form = '-'
    indeks_kontaktu_form = '-'
    popraw_form = False
    nr_pozycji_form = '-'
    lista_form = 1
    lista_wpis_form = '-'
    przekrojePrzewodow_form = 1
    przekrojePrzewodow_wpis2_form = '-'
    rozciag_form_ed = 0
    potw_form = False
    narzedzia_form = '-'
    nr_pracownika_form = 0
    wysokosc_form = 0
    grupa_robocza_form = 1
    grupa_robocza_wpis_form = '-'
    narzedzia_rodzaj_form = 1
    narzedzia_rodzaj_wpis_form = '-'
    data_serwis_form = data_dodania
    #-------------------------------------------------------------------------------

    if request.method == 'POST':
        if form.is_valid():
            print('* test danych *****************************************************')


            print('* koniec testu ****************************************************')

            # - ZAPIS -----------------------------------------------------------------------------------

            przekrojePrzewodow_form = request.POST.get('przekrojePrzewodow')
            przekrojePrzewodow_form_wart = Przekroje.objects.values_list('wartosc').get(pk=przekrojePrzewodow_form)
            przekrojePrzewodow_wpis2_form = Przekroje.objects.filter(pk=przekrojePrzewodow_form)
            rozciag_form = Decimal(request.POST.get('rozciag').replace(',', '.'))
            rozciag_form_ed = str(rozciag_form)
            nr_zlecenia_form = request.POST.get('nr_zlecenia')
            indeks_kontaktu_form = request.POST.get('indeks_kontaktu')
            poprawkowe_form = request.POST.get('poprawkowe')
            popraw_form = False
            if poprawkowe_form == 'on':
                popraw_form = True
            nr_pozycji_form = request.POST.get('nr_pozycji')
            lista_form = request.POST.get('lista')
            lista_form_wart = Listy.objects.filter(id = lista_form)
            lista_wpis_form = lista_form_wart[0]
            potwierdzenie_form = request.POST.get('potwierdzenie')
            potw_form = False
            if potwierdzenie_form == 'on':
                potw_form = True
            narzedzia_form = request.POST.get('narzedzia')
            narzedzia_rodzaj_form = request.POST.get('narzedzia_rodzaj')
            narzedzia_rodzaj_form_wart = Narzedzia.objects.filter(id = narzedzia_rodzaj_form)
            narzedzia_rodzaj_wpis_form = narzedzia_rodzaj_form_wart[0]
            nr_pracownika_form = request.POST.get('nr_pracownika')
            grupa_robocza_form = request.POST.get('grupa_robocza')
            grupa_robocza_form_wart = GrupaRobocza.objects.filter(id = grupa_robocza_form)
            grupa_robocza_wpis_form = grupa_robocza_form_wart[0]
            wysokosc_form = Decimal(request.POST.get('wysokosc').replace(',', '.'))
            data_serwis_form = request.POST.get('data_serwis')
            data_dodania_form = request.POST.get('data_dodania')
            autor = get_author(request.user)
            gosc = autor.user
            print('serwis:',data_serwis_form)


            if rozciag_form < przekrojePrzewodow_form_wart[0]:
                print('--- NIE DZIAŁA!!! ---')
                messages.error(request, f"Nieodpowiedni rozciąg! Zmień przekrój przewodu lub wykonaj kolejny pomiar!")
                edycja = 1
            else:
                print('--- jest OK ---')
                dopisz = form.save(commit=False)
                dopisz.rozciag = rozciag_form
                dopisz.poprawkowe = popraw_form
                dopisz.wysokosc = wysokosc_form
                dopisz.potwierdzenie = potw_form
                dopisz.data_dodania = data_dodania_form
                dopisz.zalogowany_user = autor
                if str(gosc) != "guest":
                    if data_serwis_form == '':
                        data_serwis_form = data_dodania_form
                    dopisz.data_serwis = data_serwis_form
                dopisz.save()
                messages.success(request, f"Pomiar poprawny! Dane zostały dodane do bazy danych!")


        else:
            print('Nie jest VALID!')
            print('Error: ', form.errors)
    else:
        print('Coś nie tak!')


    context = {
        'nr_zlecenia': nr_zlecenia_form,
        'indeks_kontaktu': indeks_kontaktu_form,
        'poprawkowe': popraw_form,
        'nr_pozycji': nr_pozycji_form,
        'lista': lista_form,
        'lista_wpis': lista_wpis_form,
        'przekrojePrzewodow': przekrojePrzewodow_form,
        'przekrojePrzewodow_wpis': przekrojePrzewodow_wpis2_form[0],
        'rozciag': rozciag_form_ed,
        'potwierdzenie': potw_form,
        'narzedzia': narzedzia_form,
        'nr_pracownika': nr_pracownika_form,
        'wysokosc': wysokosc_form,
        'grupa_robocza': grupa_robocza_form,
        'grupa_robocza_wpis': grupa_robocza_wpis_form,
        'narzedzia_rodzaj': narzedzia_rodzaj_form,
        'narzedzia_rodzaj_wpis': narzedzia_rodzaj_wpis_form,
        'data_serwis': data_serwis_form,

        'lista_rozciagi': lista_rozciagi,
        'lista_listy': lista_listy,
        'lista_przekroje': lista_przekroje,
        'lista_grupy': lista_grupy,
        'lista_rodzaj': lista_rodzaj,
        'data_dodania': data_dodania,
        'edycja': edycja,
    }

    return render(request, 'rozciagi/wpis_form.html', context)

# =============================================================================================


# == WSZYSTKIE WPISY ====================================================================================
def wszystkie_wpisy(request):
    rozciag = Rozciagi.objects.all().order_by('-id')[:1000]

    context = {
        'rozciag': rozciag
    }

    return render(request, 'rozciagi/wszystkie_wpisy.html', context)
# =============================================================================================


# == LOGIN ====================================================================================
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info( request, f"Witaj {username}! Właśnie się zalogowałeś.")
                return redirect("/")
            else:
                messages.error(request, f"Błędny login lub hasło")
        else:
            messages.error(request, f"- Błędny login lub hasło -")
    form = AuthenticationForm()

    context = {
        "form": form
    }
    return render(request, "rozciagi/login.html", context)
# =============================================================================================



# == LOGOUT ====================================================================================
def logout_request(request):
    logout(request)
    messages.info(request, "Właśnie wylogowałeś się!")
    return redirect("/")
# =============================================================================================


# == VALIDACJA DANYCH ====================================================================================
def is_valid_queryparam(param):
    return param != '' and param is not None
# =============================================================================================


# == EKSPORT DANYCH ====================================================================================
@login_required
def filtrowanie(request):
    qs = Rozciagi.objects.all()
    indeks_kontaktu_contains_query = request.POST.get('indeks_kontaktu_contains')
    numer_zlecenia_contains_query = request.POST.get('numer_zlecenia_contains')
    pracownik_contains_query = request.POST.get('pracownik_contains')
    narzedzia_contains_query = request.POST.get('narzedzia_contains')
    data_od = request.POST.get('data_od')
    data_do = request.POST.get('data_do')
    data_serwis_od = request.POST.get('data_serwis_od')
    data_serwis_do = request.POST.get('data_serwis_do')
    eksport = request.POST.get('eksport')

    print('data_od: ',data_od)
    print('data_do: ',data_do)
    print('indeks_kontaktu: ',indeks_kontaktu_contains_query)

    if is_valid_queryparam(indeks_kontaktu_contains_query):
        qs = qs.filter(indeks_kontaktu__icontains = indeks_kontaktu_contains_query)

    elif is_valid_queryparam(numer_zlecenia_contains_query):
        qs = qs.filter(nr_zlecenia__icontains = numer_zlecenia_contains_query)

    elif is_valid_queryparam(pracownik_contains_query):
        qs = qs.filter(nr_pracownika = pracownik_contains_query)

    elif is_valid_queryparam(narzedzia_contains_query):
        qs = qs.filter(narzedzia = narzedzia_contains_query)

    if is_valid_queryparam(data_od):
        qs = qs.filter(data_dodania__gte = data_od)

    if is_valid_queryparam(data_do):
        qs = qs.filter(data_dodania__lte = data_do)

    if is_valid_queryparam(data_serwis_od):
        qs = qs.filter(data_serwis__gte = data_serwis_od)

    if is_valid_queryparam(data_serwis_do):
        qs = qs.filter(data_serwis__lte = data_serwis_do)

    if eksport == 'on':

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="eksport.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, dialect='excel', delimiter=';')
        writer.writerow(
            [
                'nr_zlecenia',
                'nr_pozycji',
                'lista',
                'nr_pracownika',
                'rozciag',
                'przekroj_przewodu',
                'indeks_kontaktu',
                'poprawkowe',
                'nr_narzedzia',
                'grupa_robocza',
                'wysokosc',
                'data_serwis',
                'data_dodania',
                'narzedzia_rodzaj',
                'potwierdzenie',
                'dział'
            ]
        )

        for obj in qs:
            if obj.zalogowany_user is None:
                zalogowany = ''
            else:
                zalogowany = '{}'.format(obj.zalogowany_user.dzial)
            writer.writerow(
                [
                    obj.nr_zlecenia,
                    obj.nr_pozycji,
                    obj.lista,
                    obj.nr_pracownika,
                    obj.rozciag,
                    obj.przekrojePrzewodow.przekroj,
                    obj.indeks_kontaktu,
                    obj.poprawkowe,
                    obj.narzedzia,
                    obj.grupa_robocza,
                    obj.wysokosc,
                    obj.data_serwis,
                    obj.data_dodania,
                    obj.narzedzia_rodzaj,
                    obj.potwierdzenie,
                    zalogowany,
                ]
            )
        return response

    context = {
        'queryset': qs,
    }
    return render(request, 'rozciagi/eksport.html', context)
# =============================================================================================
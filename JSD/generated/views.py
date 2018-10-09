from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from .models import Agencija
from .models import Korisnik


# Create view for Agencija model.
class AgencijaCreateView(CreateView):
    template_name = '.html'
    model = Agencija
    fields = ['naziv', 'adresa', 'telefon']
    success_url = reverse_lazy('')


# Update view for Agencija model.
class AgencijaUpdateView(UpdateView):
    template_name = '.html'
    model = Agencija
    fields = ['naziv', 'adresa', 'telefon']


# Delete view for Agencija model.
class AgencijaDeleteView(DeleteView):
    template_name = '.html'
    model = Agencija
    success_url = reverse_lazy('')


# List view for Agencija model.
class AgencijaListView(generic.ListView):
    template_name = '.html'
    context_object_name = 'all_Agencija'

    def get_queryset(self):
        return Agencija.object.all


# Create view for Korisnik model.
class KorisnikCreateView(CreateView):
    template_name = '.html'
    model = Korisnik
    fields = ['agencija', 'ime', 'prezime', 'adresa', 'datumRodjenja', 'jmbg', 'email', 'pol']
    success_url = reverse_lazy('')


# Update view for Korisnik model.
class KorisnikUpdateView(UpdateView):
    template_name = '.html'
    model = Korisnik
    fields = ['agencija', 'ime', 'prezime', 'adresa', 'datumRodjenja', 'jmbg', 'email', 'pol']


# Delete view for Korisnik model.
class KorisnikDeleteView(DeleteView):
    template_name = '.html'
    model = Korisnik
    success_url = reverse_lazy('')


# List view for Korisnik model.
class KorisnikListView(generic.ListView):
    template_name = '.html'
    context_object_name = 'all_Korisnik'

    def get_queryset(self):
        return Korisnik.object.all
from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Trip, Note
# Create your views here.

class HomeView(TemplateView):
    template_name = 'triptrack/index.html'


def index(request):
    return HttpResponse('hi')


# filter by user's trips
# FUNCTION BASED VIEW
def trips_list(request):
    trips = Trip.objects.filter(owner = request.user)
    context = {
        "trips":trips
    }
    return render(request,'triptrack/trip_list.html',context)


# CLASS BASED VIEW
class TripCreateView(CreateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city','countryCode','start_date','end_date']
    # template model_form.html


    def form_valid(self,form):
        # overwrite the function
        # set the owner field = logged in user
        form.instance.owner = self.request.user
        return super().form_valid(form) # call the super with the updated form
    

# CLASS BASED
    
class TripDetailView(DetailView):
    model = Trip
    # we also want the Note data associated with Trip
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = context['object'] # by default data it's called "object"
        notes = trip.mynotes.all() # related_name is mynotes

        context['allnotes'] = notes 
         # in our template model_detail.html
        # we will have access to trip and 'allnotes'
        return context
    

class TripUpdateView(UpdateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city','countryCode','start_date','end_date']

class TripDeleteView(DeleteView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    # no template needed - send a post req to this URL

# CLASS BASED VIEW 
class NoteDetailView(DetailView):
    model = Note 


class NoteListView(ListView):
    model = Note 

    # we only want to return the note of whoever log ins
    # in our function based Trip list view
    # trips = Trip.objects.filter(owner = request.user)

    # overwrite method
    def get_queryset(self):
        # print(Note.objects.get(pk=1).trip.owner)
        # Field lookups format - field__lookuptype=value. 
        queryset = Note.objects.filter(trip__owner = self.request.user)
        return queryset
    

class NoteCreateView(CreateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = "__all__"

    # overwrite method
    # we only want to see the Trip belongs to the login user
    def get_form(self):
        form = super(NoteCreateView, self).get_form()
        user_trips = Trip.objects.filter(owner = self.request.user)
        # print(form.fields)
        form.fields['trip'].queryset = user_trips # dropdown menu
        return form
    


class NoteUpdateView(UpdateView):
    model = Note
    success_url = reverse_lazy('note-list')
    fields = "__all__"

    # overwrite method
    # we only want to see the Trip belongs to the login user
    def get_form(self):
        form = super(NoteUpdateView, self).get_form()
        user_trips = Trip.objects.filter(owner = self.request.user)
        # print(form.fields)
        form.fields['trip'].queryset = user_trips # dropdown menu
        return form

class NoteDeleteView(DeleteView):
    model = Note
    success_url = reverse_lazy('note-list')
    # no template needed - send a post req to this URL




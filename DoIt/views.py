from .models import Stuff
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .forms import PositionForm




class CustomLoginView(LoginView):
    template_name = 'DoIt/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('stuffs')


class RegisterSection(FormView):
    template_name = 'DoIt/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('stuffs')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterSection, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('stuffs')
        return super(RegisterSection, self).get(*args, **kwargs)



class StuffList(LoginRequiredMixin, ListView):
    model = Stuff
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = context['list'].filter(user = self.request.user)
        context['count'] = context['list'].filter(completed = False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['list'] = context['list'].filter(title__startswith = search_input) 


        context['search_input'] = search_input
        return context
    

class StuffDetail(LoginRequiredMixin, DetailView):
    model = Stuff
    context_object_name = 'task'
    template_name = 'DoIt/stuff.html'


class StuffCreate(LoginRequiredMixin, CreateView):
    model = Stuff
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('stuffs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(StuffCreate, self).form_valid(form)


class StuffUpdate(LoginRequiredMixin, UpdateView):
    model = Stuff
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('stuffs')


class StuffDelete(LoginRequiredMixin, DeleteView):
    model = Stuff
    context_object_name = 'task'
    success_url = reverse_lazy('stuffs')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)



class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_stuff_order(positionList)

        return redirect(reverse_lazy('stuffs'))
   



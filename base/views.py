from asyncio import Task
from calendar import c
from multiprocessing import context
from turtle import title
from urllib import request
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import FormView
from . models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/main.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin, DetailView):
     model = Task
     template_name = 'base/detail.html'
     context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    template_name = 'base/create.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    template_name = 'base/create.html'
    success_url = reverse_lazy('main')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('main')

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    redirect_authenticated_user = True
    fields = '__all__'
    
    def get_success_url(self):
        return reverse_lazy('main')

class RegisterPage(FormView):
    template_name = 'base/registration.html'
    redirect_authenticated_user = True
    form_class = UserCreationForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super(RegisterPage, self).get(*args, **kwargs)
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login                       #to make logged in after registering

from django.contrib.auth.views import LoginView,LogoutView

from django.contrib.auth.mixins import LoginRequiredMixin


from .models import task
# Create your views here.



class registerpage(FormView):
    template_name='api/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('tasks') 

    def form_valid(self,form):
       user=form.save()              #returns user
       if user is not  None:
           login(self.request,user)
       return super().form_valid(form)

    def get(self, *args, **kwargs):                      #overriden coz redirect true not working
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(registerpage,self).get(*args, **kwargs)




class customloginview(LoginView):
    template_name='api/login.html'
    fields='__all__'

    redirect_authenticated_user=True

    def get_success_url(self):                     #redirect to our url else it direct to inbuilt account/ url
        return reverse_lazy('tasks')




class taskview(LoginRequiredMixin,ListView):
    model=task
    context_object_name ='tasks'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)              #retrieving data of particular user
        context['count']=context['tasks'].filter(complete=False).count()
        return context


                                                       
class taskdetail(LoginRequiredMixin,DetailView):                                #put = AND not :
    model= task   
    context_object_name= 'task'
    template_name='api/task.html'
    
    
    
class taskcreate(LoginRequiredMixin,CreateView):
    model=task
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')     #url to redirect
     
    def form_valid(self,form):                             #triggered by post req   and overrided to add data without selecting a specific user
         form.instance.user=self.request.user
         return super(taskcreate,self).form_valid(form)

class taskupdate(LoginRequiredMixin,UpdateView):
    model=task
    fields='__all__'
    success_url=reverse_lazy('tasks')


class taskdelete(LoginRequiredMixin,DeleteView):
    model=task
    fields='__all__'
    context_object_name='task'
    success_url=reverse_lazy('tasks')
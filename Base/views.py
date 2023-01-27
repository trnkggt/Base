from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm

# Create your views here.


class TaskList(ListView):
    model = Task
    template_name = 'Base/home-page.html'
    context_object_name = 'tasks'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user_id=self.request.user.pk)
        print(self.request.user.pk)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area')
        if search_input is not None:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        context['search_input'] = search_input
        return context



## Class Based View to create a task
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'Base/task-create.html'
    fields = ['content', 'title', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

## Function Based View to create a task
@login_required
def create_task(request):

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'Base/task-create.html', {'form':form})

class TaskUpdate(UpdateView):
    model = Task
    fields = ['content', 'title', 'complete']
    template_name = 'Base/task-create.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

## Function Based View to update a task
@login_required
def update_task(request, task_pk):
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=Task.objects.get(pk=task_pk))
        if form.is_valid():
            form.save()
        return redirect('tasks')
    else:
        form = TaskForm(instance=Task.objects.get(pk=task_pk))
    return render(request, 'Base/task-create.html', {'form':form})

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'Base/task-delete.html'

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'Base/login.html'
    def get_success_url(self):
        return reverse_lazy('tasks')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Username or Password')
        return self.render_to_response(self.get_context_data(form=form))

## Function Based View for Login
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('tasks')
    else:
        messages.error(request, 'Invalid Username or Password')
    return render(request, 'Base/login.html')

class MyLogOut(LogoutView):
    next_page = 'login'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(request, username=form.cleaned_data['username'],
                                    password = form.cleaned_data['password1'])
            login(request, new_user)

        messages.success(request, 'Account created successfully')
        return redirect('tasks')
    else:
        form = UserCreationForm()
    return render(request, 'Base/register.html', {'form':form})
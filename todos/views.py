from django.db.models import query
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from .forms import TodoForm
from django.http import HttpResponseRedirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def todo_list_view(request):
    context = {}
    queryset = Todo.objects.filter(user=request.user)
    context['lists'] = queryset
    return render(request,'todos/index.html', context)

@login_required
def add(request):
    context = {}
    forms = TodoForm()
    if request.method == "POST":
        forms = TodoForm(request.POST or None)
        if forms.is_valid():
            forms = forms.save()
            forms.user = request.user
            forms.save()
            return redirect("index")
        else:
            context['form'] = forms
            return render(request, "todos/add.html", context)
    
    context['form'] = forms
    return render(request, "todos/add.html", context)

@login_required
def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.delete()

    return redirect('index')

@login_required
def update(request, todo_id):
    context = {}
    todo_query = Todo.objects.filter(id=todo_id).first()

    if request.method == "POST":
        forms = TodoForm(request.POST,instance=todo_query)
        if forms.is_valid():
            task = forms.save()
            task.user = request.user
            task.save()
            return redirect("index")
        else:
            context['form'] = forms
            return render(request, "todos/update.html", context)

    forms = TodoForm(instance=todo_query)
    context['form'] = forms
    context['task_id'] = todo_query
    return render(request, "todos/update.html", context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('index')

        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'todos/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=user_name,
                                                password=password1,
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()
                print('user created')

        else:
            messages.info(request, "password not matching...")
            return redirect('register')
        return redirect('login')

    else:
        return render(request, 'todos/register.html')


def sent_view(request,id):
    if request.method == "POST":
        sent_user = request.POST['sent_user']
        read_only = request.POST.get("read_only", None)
        queryset_task = Todo.objects.filter(id=id).first()
        user_sent_query = User.objects.filter(username=sent_user).first()
        if user_sent_query:
            
            queryset_task.user_to = user_sent_query
            queryset_task.send_to = True
            queryset_task.send_from = True
            queryset_task.save()
            if read_only:
                queryset_task.read_only = True
                queryset_task.save()
    
    return render(request, 'todos/index.html')


def sent_to_view(request):
    context= {}
    queryset_todos = Todo.objects.filter(user_to_id=request.user.id,send_from=True)
    context['sent_from_tasks'] = queryset_todos
    return render(request, "todos/send_from.html",context)



def sent_from_view(request):
    context= {}
    queryset_todos = Todo.objects.filter(user_id=request.user.id,send_to=True)
    print(queryset_todos)
    context['sent_to_tasks'] = queryset_todos
    return render(request, "todos/send_to.html",context)

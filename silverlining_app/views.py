from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

#sign up & login

def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for (key, values) in errors.items():
                messages.error(request, values)
            return redirect('/')
        pw_hash= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(user_name=request.POST['user_name'], email=request.POST['email'], password=pw_hash)
        print(new_user.password)
        request.session['name'] = new_user.user_name
        request.session['id'] = new_user.id
        return redirect('/')
    return redirect('/')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        user=user[0]
    else:
        messages.error(request, 'Email or password incorrect.')
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user'] = user.user_name
        request.session['id'] = user.id
        print(User.objects.all())
        return redirect('/tasks')
    else:
        messages.error(request, 'Email or password is incorrect')
        return redirect('index.html')

def logout(request):
    request.session.flush()
    print(request.session)
    return redirect('/')

# CRUD Silver Lining aka task

def post(request):
   # todo = Todo.objects.all
    #if request.method == 'POST':
    #    new_todo = Todo(
     #       title = request.POST['title']
        #)
        #new_todo.save()
      #  return redirect ('/')

   # return render( request, 'task.html', {'todos': todo})

    if request.method =='POST':
       Todo.objects.create(title=request.POST['title'], poster=User.objects.get(id=request.session['id']))
       print(Todo.objects.all())
    return redirect('/tasks')


def delete(request, id):
    #todo = Todo.objects.get(id=pk)
    #todo.delete()
    #return redirect('/')
    to_delete = Todo.objects.get(id=id)
    if to_delete.poster_id == request.session['id']:
        to_delete.delete()
    return redirect('/tasks')

def tasks(request):
    if 'user' not in request.session:
        return redirect('/')
    context ={
        'wall_thoughts': Todo.objects.all(),
        'log_user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'task.html', context)

def showtask(request, id):
    context = {
        'task': Todo.objects.get(id=id),
        'current_user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'task.html', context)

def thoughts(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'wall_thoughts': Todo.objects.all(),
        'log_user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'task.html', context)
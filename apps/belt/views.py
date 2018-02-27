from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request):
    if 'id' in request.session:
        request.session.clear()
    return render(request,'belt/index.html',{'Users':User.objects.all()})

def register(request):
    if request.method != 'POST':
        messages.error(request, "Create User")
        return redirect('/')
    else:
        print request.POST['hire_date']
        errors = User.objects.simple_validator(request.POST)
        if len(errors):
            for key,values in errors.iteritems():
                messages.success(request, values)
            return redirect('/')
        else:
            id = User.objects.get(username=request.POST['username']).id
            name = User.objects.get(username=request.POST['username']).first_name
            request.session['id'] = id
            request.session['name'] = name
            return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key,values in errors.iteritems():
            messages.success(request, values)
        return redirect('/')
    else:
        id = User.objects.get(username=request.POST['username']).id
        name = User.objects.get(username=request.POST['username']).first_name
        request.session['id'] = id
        request.session['name'] = name
        # move to models
        return redirect('/dashboard')

def dashboard(request):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    content = {"user_list": User.objects.get(id = request.session['id'])}
    return render(request, 'belt/dashboard.html',content)

def create_item(request):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    return render(request, 'belt/create.html')

def add(request):
    errors = Wishlist.objects.wish_validator(request.POST)
    if len(errors):
        for key,values in errors.iteritems():
            messages.success(request, values)
        return redirect('/wish_items/create')
    else:
        idz = int(request.session['id'])
        Wishlist.objects.create(name=request.POST['item'], uploader=User.objects.get(id=idz))
        return redirect('/dashboard')

def destroy(request):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        return redirect('/dashboard')

def remove(request):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        return redirect('/dashboard')

def items(request, number):
    if not "id" in request.session:
        messages.error(request, "Login")
        return redirect('/')
    else:
        content = {"item_list": User.objects.all(),
        "num": number}
        print content
        return render(request,'belt/items.html', content)
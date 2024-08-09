from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'login.html')

def update(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    context = {
        'user': User.objects.get(id=user_id),
        'idea': Idea.objects.get(id=id)
    }
    return render(request, 'update.html', context)

def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/')
    context = {
        'user': User.objects.get(id=user_id),
        'ideas': Idea.objects.all(),  # Fetch all ideas
    }
    return render(request, 'dashboard.html', context)

def registration(request):
    if request.method == 'POST':
        errors = User.objects.basic_register(request.POST)
        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')
        else:
            user = create_user(request.POST)
            request.session['user_id'] = user.id
            messages.success(request, "Successfully Registered")
            return redirect('/dashboard')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.basic_login(request.POST)
        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')

        user = check_email(request.POST)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                messages.success(request, "Successfully logged in")
                return redirect('/dashboard')
        messages.error(request, "Invalid credentials")
        return redirect('/')
    return redirect('/')

def add_idea(request):
    if request.method == 'POST':
        create_idea(request)
        messages.success(request, "Idea added successfully")
        return redirect('/dashboard')
    return redirect('/')

def logout(request):
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')

def update_idea(request, idea_id):
    if request.method == 'POST':
        user_id = request.session['user_id']
        idea = Idea.objects.get(id=idea_id, user_id=user_id)
        if idea:
            update_idea(request.POST, idea_id, user_id)
            messages.success(request, "Idea updated successfully")
        else:
            messages.error(request, "You are not authorized to update this idea")
    return redirect('/dashboard')

def delete(request):
    if request.method == 'POST':
        delete_idea(request.POST)
        messages.success(request, "Idea deleted successfully")
    return redirect('/dashboard')

def idea_detail(request, id):
    idea = get_object_or_404(Idea, id=id)
    context = {
        'idea': idea
    }
    return render(request, 'idea_detail.html', context)

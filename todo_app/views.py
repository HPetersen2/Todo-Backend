from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .forms import LoginForm, RegisterForm, TodoForm
from .models import Todo

User = get_user_model()

def get_user_from_jwt(request):
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(request.COOKIES.get('access_token'))
        user = jwt_authenticator.get_user(validated_token)
        return user if user and user.is_authenticated else None
    except (InvalidToken, TokenError):
        return None

def login_required_jwt(view_func):
    def wrapper(request, *args, **kwargs):
        user = get_user_from_jwt(request)
        if not user:
            return redirect('login')
        request.user = user
        return view_func(request, *args, **kwargs)
    return wrapper

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            # Set tokens in cookies
            response = redirect('todo_list')
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
            return response
    else:
        form = LoginForm()
    return render(request, 'todo_app/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'todo_app/register.html', {'form': form})

def logout_view(request):
    response = redirect('login')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response

@login_required_jwt
def todo_list(request):
    todos = Todo.objects.filter(creator=request.user)
    return render(request, 'todo_app/todo_list.html', {'todos': todos})

@login_required_jwt
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.creator = request.user
            todo.save()
            messages.success(request, 'Todo created successfully.')
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo_app/todo_form.html', {'form': form, 'title': 'Create Todo'})

@login_required_jwt
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, creator=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully.')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo_app/todo_form.html', {'form': form, 'title': 'Update Todo'})

@login_required_jwt
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, creator=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully.')
        return redirect('todo_list')
    return render(request, 'todo_app/todo_confirm_delete.html', {'todo': todo})

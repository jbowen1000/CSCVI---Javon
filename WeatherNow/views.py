from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect(reverse('login'))  # Redirect to login page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or dashboard page
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')
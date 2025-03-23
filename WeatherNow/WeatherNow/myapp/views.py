from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from myapp.forms import CustomUserCreationForm
import requests

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            return redirect('weather')  # Redirect to the weather page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

# Weather Search View
def weather_view(request):
    api_key = 'f8995150c2e6d29062867ba7620b96f2'  # OpenWeather API Key
    city = request.GET.get('city', '')  # Get city from user input

    weather = None
    error_message = None

    if city:  # Fetch weather only if a city is provided
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if weather_data.get('cod') != 200:
            error_message = "City not found. Please try again."
        else:
            weather = {
                'city': weather_data['name'],
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'],
                'humidity': weather_data['main']['humidity'],
            }

    return render(request, 'weather.html', {'weather': weather, 'error_message': error_message})

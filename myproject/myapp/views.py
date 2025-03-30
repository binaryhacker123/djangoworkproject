from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User  # Add this import
from .forms import ContactForm
from .models import Service

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registration_view(request):
    if request.method == 'POST':
        # Process the data manually instead of using form.is_valid()
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Create your validation logic here
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
        else:
            messages.error(request, "Passwords don't match.")
    
    # Pass an empty object instead of a form
    return render(request, 'registration.html', {'form': None})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def dashboard(request):
    return render(request, 'dashboard.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message! We'll respond as soon as possible.")
            return redirect('contact')
    else:
        form = ContactForm()
        
    return render(request, 'contact.html', {'form': form})


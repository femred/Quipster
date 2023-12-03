from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Profile, Quip
from .forms import QuipForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms

def home(request):
	quips = []
	if request.user.is_authenticated:
		form = QuipForm(request.POST or None)
		if request.method == "POST":
			if form.is_valid():
				quip = form.save(commit=False)
				quip.user = request.user
				quip.save()
				messages.success(request, ("Your Quip Has Been Posted!"))
				return redirect('home')
			
		quips = Quip.objects.all().order_by("-created_at")
		return render(request, 'home.html', {"quips":quips, "form":form})
	else:
		messages.success(request, ("You must be logged in to view this page."))
	return render(request, 'home.html', {"quips":quips})


def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'profile_list.html', {"profiles":profiles})
	else:
		return redirect('home')

def profile(request, pk):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user_id = pk)
		quips = Quip.objects.filter(user_id=pk).order_by("-created_at")

		if request.method == "POST":
			current_user_profile = request.user.profile
			action = request.POST['follow']
			if action == "unfollow":
				current_user_profile.follows.remove(profile)
			elif action == "follow":
				current_user_profile.follows.add(profile)
			current_user_profile.save()

		return render(request, "profile.html", {"profile":profile, "quips":quips})
	else:
		return redirect('home')	

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In! Get Quipping! "))
			return redirect('home')
		else:
			messages.success(request, ("There was an error logging in! "))
			return redirect('login')
	else:	
		return render(request, "login.html", {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out"))
	return redirect('home')

def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			#first_name = form.cleaned_data['first_name']
			#second_name = form.cleaned_data['second_name']
			#email = form.cleaned_data['email']

			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Successfully registered! "))
			return redirect('home')
		
	return render(request, "register.html", {'form':form})
from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Profile, Quip

def home(request):
	quips = []
	if request.user.is_authenticated:
		quips = Quip.objects.all().order_by("-created_at")
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

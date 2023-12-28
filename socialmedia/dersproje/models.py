from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import datetime

class Quip(models.Model):
	user = models.ForeignKey(
		User, related_name="quips",
		on_delete=models.DO_NOTHING
		)
	body = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User, related_name='quip_like', blank=True)

	def number_of_likes(self):
		return self.likes.count()

	def time_ago(self):
		time = datetime.now()
		if self.created_at.day == time.day:
			return str(time.hour - self.created_at.hour) + " hours ago"
		else:
			if self.created_at.month == time.month:
				return str(time.day - self.created_at.day) + " days ago"
			else:
				if self.created_at.year == time.year:
					return str(time.month - self.created_at.month) + " months ago"
		return self.created_at

	def __str__(self):
		return(
			f"{self.user} "
			f"({self.created_at:%Y-%m-%d %H:%M}): "
			f"{self.body}..."
			)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	follows = models.ManyToManyField("self",
		related_name="followed_by",
		symmetrical=False,
		blank=True)

	date_modified = models.DateTimeField(User, auto_now=True)
	profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
	
	profile_bio = models.CharField(null=True, blank=True, max_length=500)
	homepage_link = models.CharField(null=True, blank=True, max_length=500)
	facebook_link = models.CharField(null=True, blank=True, max_length=100)
	instagram_link = models.CharField(null=True, blank=True, max_length=100)
	linkedin_link = models.CharField(null=True, blank=True, max_length=100)

	def __str__ (self):
		return self.user.username

	def number_of_follows(self):
		return self.follows.count()
	
	def number_of_followers(self):
		return self.followed_by.count()

def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()

		user_profile.follows.set([instance.profile.id])
		user_profile.save()

post_save.connect(create_profile, sender=User)		
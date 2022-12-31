from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, RegisterUserOtpForm 
from accounts.models import User
import requests
from django.conf import settings

def login_user(request):
	if request.method == "POST":
		try:
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(request, email=email, password=password)
			print(email, user)
			user2 = User.objects.get(email = email)
			#print(user2.is_verified)
			
			print(user2.verified)
			if user is not None and user2.verified:
				login(request, user)
				params = {"username": email, "password": password}
				headers = {"content-type": "application/json"}
				r = requests.post(settings.API_URL+"api/token-auth/", params, headers)
				print(r.json())
				user2.aut_token = "Token " + r.json()['token']
				print(user2.aut_token, r.json()['token'])
				user2.save()
				return redirect('dashboard')
			elif (user is not None) and (not user2.verified):
				login(request, user)
				messages.success(request, ("OTP is not Verified. Kindly verify it"))	
				return redirect('verifyotp')

			else:
				messages.success(request, ("There Was An Error Logging In, Try Again..."))	
				return redirect('login')	
		except Exception as e:
			print(e)
			messages.success(request, ("User Doesn't Exist"))
			return redirect('login')
	else:
		return render(request, 'loginuser/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('login')


def register_user(request):
	print(request.method)
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			#form.save()
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			data = {
				'email':email,
				'password':password
			}
			print("here1")
			response = requests.post(settings.API_URL+'register/', data=data)
			print(response.json())

			if response.status_code==200:
				user = authenticate(email=email, password=password)
				login(request, user)

				params = {"username": email, "password": password}
				headers = {"content-type": "application/json"}
				r = requests.post(settings.API_URL+"api/token-auth/", params, headers)
				print(r.json())
				user2 = User.objects.get(email = email)
				user2.aut_token = "Token "+r.json()['token']
				user2.save()
				messages.success(request, ("Registration Successful! Enter OTP"))
				print("here2")
				
				print(user2.primarykey)
				return redirect('verifyotp')
	else:
		form = RegisterUserForm()
        
	print("here2i")
	return render(request, 'loginuser/register_user.html', {
		'form':form,
		})


def verifyotp(request):
	print("here3 iii - ")
	loggedinuser = request.user
	print(loggedinuser.emailid)
	if (request.method == "POST" ):
		print("here4")
		form = RegisterUserOtpForm(request.POST)
		print("here5")
		if form.is_valid():
			#form.save()
			otp = form.cleaned_data['otp']
			email = loggedinuser.emailid
			data = {
				'email':email,
				'otp':otp,
			}
			print(data)

			print("here6")
			try:
				user2 = User.objects.get(email = email)
				headers = {"Authorization": user2.aut_token}

				response = requests.post(settings.API_URL+'verify/', data=data, headers=headers)
				print(response.json())
				if response.status_code==200:
					print("here7")
					messages.success(request, ("Registration Successful!"))
					return redirect('dashboard')

			except:
				print("here3 i")
				form = RegisterUserOtpForm()
				return render(request, 'loginuser/verifyotp.html', {
				'form':form
				})

	else:
		print("here3 i")
		form = RegisterUserOtpForm()
        
	print("here3 ii", form)
	return render(request, 'loginuser/verifyotp.html', {
		'form':form
		})


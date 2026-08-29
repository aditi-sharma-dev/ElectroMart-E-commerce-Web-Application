from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method=="POST":
        full_name=request.POST['full_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password!=confirm_password:
            messages.error(request,"Password do not match")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already taken")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')
        user=User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.first_name=full_name
        user.save()
        Profile.objects.create(user=user)
        messages.success(request,'Registration Successfull')
        return redirect('login_user')
    return render(request,'register.html')
        

def login_user(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            messages.error(
                request,
                "Invalid username or password."
            )
            return redirect('login_user')

        if user.is_staff or user.is_superuser:
            messages.error(
                request,
                "Admin user cannot login from customer page. Please use Admin panel."
            )
            return redirect('login_user')

        login(request, user)

        messages.success(
            request,
            "Login Successfully."
        )
        return redirect('home')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request,'Logout Successful')
    return redirect('login_user')
@login_required
def profile(request):
    profile,created=Profile.objects.get_or_create(user=request.user)
    if request.method=="POST":
        profile.phone=request.POST['phone']
        profile.address=request.POST['address']
        profile.city=request.POST['city']
        profile.state=request.POST['state']
        profile.pincode=request.POST['pincode']
        profile.save()
        messages.success(request,'Profile updated successfully')
        return redirect('profile')
    return render(request,'profile.html',{'profile':profile})
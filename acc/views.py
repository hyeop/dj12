from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages

# Create your views here.
from .models import User

def chpass(request):
    u = request.user
    cp = request.POST.get("cpass")
    if check_password(cp, u.password):
        np = request.POST.get("npass")
        u.set_password(np)
        u.save()
        return redirect("acc:login")
    return redirect("acc:update")


def update(request):
    if request.method == "POST":
        u = request.user
        ue = request.POST.get("umail")
        uc = request.POST.get("ucom")
        up = request.FILES.get("upic")
        u.email, u.comment = ue, uc
        if up:
            u.pic.delete()
            u.pic = up
        u.save()
        return redirect("acc:profile")
    return render(request, "acc/update.html")


def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        uc = request.POST.get("ucom")
        pi = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=up, comment=uc, pic=pi)
            return redirect("acc:login")
        except:
            pass # 마지막날!!

    return render(request, "acc/signup.html")

def delete(request):
    u = request.user
    ck = request.POST.get("ckpass")
    if check_password(ck, u.password):
        u.pic.delete()
        u.delete()
    else:
        pass # 마지막
    return redirect("acc:index")



def profile(request):
    return render(request, "acc/profile.html")

def ulogout(request):
    logout(request)
    return redirect("acc:index")

def ulogin(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un, password=up)
        if u:
            login(request, u)
            messages.success(request, f"{un}님 환영합니다!!")
            return redirect("acc:index")
        else:
            messages.error(request, "계정정보가 일치하지 않습니다")
            pass # 마지막날
    return render(request, "acc/login.html")

def index(request):
    return render(request, "acc/index.html")
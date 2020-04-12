from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import Developer, Player, Game

def index(request):
    if request.method=="GET":
        return render(request, 'shop/index.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    return render(request, 'shop/signup.html')

def logout_view(request):
    logout(request)
    return redirect("shop:login")

def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    return render(request, 'shop/login.html')

def login_user(request):
    pass

def home(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            return  redirect("shop:index")
        games = Game.objects.all()
        return render(request, "shop/home.html",{"games":games})
    else:
        return HttpResponse(status=500)
def create(request):
    if request.method=="POST":
        username=request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        developer = False
        try:
            if request.POST['developer']:
                developer=True
        except KeyError:
            developer=False
        if username is not None and email is not None and password is not None:
            if not username or not password or not email:
                return render(request, "shop/signup.html", {"error": "some error in data"})
            if User.objects.filter(username=username).exists():
                return render(request, "shop/signup.html", {"error": "username exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "shop/signup.html", {"error": "username exists"})
            user = User.objects.create_user(username, email, password)
            if developer:
                if Group.objects.filter(name='developer').exists():
                    dev_groups = Group.objects.get(name="developers")
                else:
                    Group.objects.create(name='developer').save()
                    dev_groups = Group.objects.get(name="developers")
                dev_groups.user_set.add(user)
                Developer.objects.create(user=user).save()
            else:
                Player.objects.create(user=user).save()
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect("shop:index")
    else:
        return redirect("shop:signup")


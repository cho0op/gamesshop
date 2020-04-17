from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from .models import Developer, Player, Game, Transaction

def index(request):
    if request.method=="GET":
        user=request.user
        if not request.user.is_authenticated:
            return redirect("shop:home")
        if user.groups.filter(name="developers").count()!=0:
            return redirect("shop:developer")
        transaction = Transaction.objects.filter()#some error here
        purchased_games=[]
        for transaction in transaction:
            purchased_games.append(transaction.game)
        return render(request, "shop/index.html", {"user":user, "purchased_games":purchased_games})

def signup(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    return render(request, 'shop/signup.html')

def logout_view(request):
    logout(request)
    return redirect("shop:login")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("shop:index")
    return render(request, 'shop/login.html')

def login_user(request):
    if request.method=="POST":
        username=request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request, 'shop/login.html', {"error":"one field is empty"})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shop:index")
        else:
            return render(request, "shop/login.html", {"error":"wrong username or password"})
    else:
        return redirect("shop:index")

def home(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            return  redirect("shop:index")
        games = Game.objects.all()
        return render(request, "shop/home.html",{"games":games})
    else:
        return HttpResponse(status=500)

def create(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        developer = False
        try:
            if request.POST['developer']:
                developer = True
        except KeyError:
            developer = False
        if username is not None and email is not None and password is not None:
            if not username or not email or not password:
                return render(request, "shop/signup.html", {"error": "Please fill in all required fields"})
            if User.objects.filter(username=username).exists():
                return render(request, "shop/signup.html", {"error": "Username already exists"})
            elif User.objects.filter(email=email).exists():
                return render(request, "shop/signup.html", {"error": "Email already exists"})
            user = User.objects.create_user(username, email, password)
            if developer:
                if Group.objects.filter(name="developers").exists():
                    dev_group = Group.objects.get(name="developers")
                else:
                    Group.objects.create(name='developers').save()
                    dev_group = Group.objects.get(name='developers')
                dev_group.user_set.add(user)
                Developer.objects.create(user=user).save()
            else:
                Player.objects.create(user=user).save()
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("shop:index")
    else:
        return redirect("shop:signup")

def  catalog_view(request):
    pass

def play_game(requests, game_id):
    pass

def developer_view(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            games = Game.objects.filter(developer=user.developer.id)
            statistics = []
            for game in games:
                transactions = Transaction.objects.filter(game=game.id)
                for transaction in transactions:
                    statistics.append(transaction)
            return render(request, "shop/developer.html", {"statistics": statistics})
        else:
            return redirect("shop:index")

def search(request):
    pass

def publish_page_view(request):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            redirect("shop:login")
        if user.groups.filter(name="developers").count() != 0:
            return render(request, "shop/publish_game_form.html")
        else:
            redirect("shop:index")


def developer_games(request):
    if request.method=="GET":
        user=request.user
        if not user.is_authenticated:
            redirect("shop:login")
        if user.groups.filter(name="developers").count()!=0:
            games = user.developer.game_set.all()
            return render (request, "shop/developer_games.html", {"games":games})
        else:
            redirect("shop:index")

def edit_game(request, game_id):
    if request.method == "GET":
        user = request.user
        if not user.is_authenticated:
            return redirect("shop:login")
        if user.groups.filter(name="developers").count() == 0:
            return redirect("shop:index")
        game = get_object_or_404(Game, pk=game_id)
        if game.developer.user_id == user.id:
            return render(request, "shop/edit_game.html", {"game": game})
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)

def create_game(request):
    if request.method=="POST":
        user=request.user
        if not user.is_authenticated or user.groups.filter(name="developers").count()==0:
            return HttpResponse(status=500)
        developer = user.developer
        title = request.POST["title"]
        price = request.POST["price"]
        url = request.POST["url"]
        validator = URLValidator()
        if not title and not url and not price:
            return render(request, "shop/publish_game_form.html", {"error":"fill all the gaps"})
        try:
            float_price=float(price)
        except:
            return render(request, "shop/publish_game_form.html", {"error": "price is not a number"})
        if float_price<=0:
            return render(request, "shop/publish_game_form.html", {"error": "price must be more then 0"})
        try:
            validator(url)
        except ValidationError:
            return render(request, "shop/publish_game_form.html", {"error": "URL is not valid"})
        try:
            Game.objects.create(title=title, price=float_price, url=url, developer=developer)
        except(ValidationError, IntegrityError) as e:
            return render(request, "shop/publish_game_form.html", {"error": "URL is not uniq"})
        return redirect("shop:developer_games")
    else:
        redirect("shop:signup")

def edit_game_update(request, game_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        if user.groups.filter(name="developers").count() == 0:
            return HttpResponse(status=500)
        game = get_object_or_404(Game, pk=game_id)
        if game.developer.user_id == user.id:
            title = request.POST["title"]
            price = request.POST["price"]
            url = request.POST["url"]
            if not title and not price and not url:
                return render(request, "shop/edit_game.html", {"error": "At least one of the field must be filled",
                    "game":game})
            if title.strip():
                Game.objects.filter(pk=game_id).update(title=title)
            if price.strip():
                try:
                    float_price = float(price)
                except ValueError:
                    return render(request, "shop/edit_game.html",{"error": "Price is not number",
                        "game":game})
                if float_price <= 0:
                    return render(request, "shop/edit_game.html",{"error": "Price is negative",
                        "game":game})
                Game.objects.filter(pk=game_id).update(price=price)
            if url.strip():
                try:
                    URLValidator()(url)
                except ValidationError:
                    return render(request, "shop/edit_game.html",{"error": "URL is malformed",
                        "game":game})
                try:
                    Game.objects.filter(pk=game_id).update(url=url)
                except (ValidationError, IntegrityError) as e:
                    return render(request, "shop/edit_game.html",{"error": "URL is not unique",
                        "game":game})
            return redirect("shop:developer_games")
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)

def edit_game_delete(request,game_id):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            return HttpResponse(status=500)
        if user.groups.filter(name="developers").count() == 0:
            return HttpResponse(status=500)
        game = get_object_or_404(Game, pk=game_id)
        if game.developer.user_id == user.id:
            Game.objects.get(pk=game_id).delete()
            return redirect("shop:developer_games")
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def welcome(request):
    if not "user_id" in request.session:
        return redirect("/home")

    context = {
        "rides": Ride.objects.all()
    }
    return render(request, 'welcome.html', context)

def register_biker(request):
    if request.method == "POST":
        errors = User.objects.validate(request.POST)
        
        if errors:
            for error in errors.values():
                messages.error(request, error)
            return redirect('/register')

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=username, password=pw_hash)
        request.session["user_id"] = user.id
        request.session["user_name"] = f"{user.first_name} {user.last_name}"
        return render(request, 'welcome.html')
        
    return redirect('/home')

def login(request):
    if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            logged_user = User.objects.filter(username=username)

    if logged_user:
        logged_user = logged_user[0]
        if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
            request.session["user_id"] = logged_user.id
            request.session["user_name"] = logged_user.username
            return render(request, 'welcome.html')
        else:
            messages.error(request, "Password and username do not match.")
            return redirect('/home')
    else:
        messages.error(request, "User does not exist.")
        return redirect('/home')

    return render(request, 'welcome.html')

def log_ride(request):
    date = request.POST['date']
    trail = request.POST['trail']
    distance = request.POST['distance']
    time = request.POST['time']
    notes = request.POST['notes']
    rider = User.objects.get(id=request.session["user_id"])
    Ride.objects.create(date=date, trail=trail, distance=distance, time=time, notes=notes, rider=rider)
    return render(request, 'welcome.html')

def logout(request):
    request.session.flush()
    return redirect('/home')

def newsfeed(request):
    if not "user_id" in request.session:
        return redirect("/home")
    
    context = {
        "posts": Post.objects.all()
    }

    return render(request, "newsfeed.html", context)

def create_post(request):
    message = request.POST["message"]
    poster = User.objects.get(id=request.session["user_id"])
    Post.objects.create(message=message, poster=poster)
    return redirect('/newsfeed')

def add_comment(request, id):
    poster = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=id)
    comment = request.POST["comment"]
    Comment.objects.create(comment=comment, poster=poster, post=post)
    return redirect('/newsfeed')

def like(request, id):
    post = Post.objects.get(id=id)
    user = User.objects.get(id=request.session["user_id"])
    post.likes.add(user)
    return redirect('/newsfeed')

def delete(request, id):
    ride_to_delete = Ride.objects.get(id=id)
    ride_to_delete.delete()
    return redirect('/welcome')

def edit(request, id):
    one_ride = Ride.objects.get(id=id)
    context = {
        'ride': one_ride
    }
    return render(request, 'edit.html', context)

def delete_post(request, id):
    post_to_delete = Post.objects.get(id=id)
    post_to_delete.delete()
    return redirect('/newsfeed')

def delete_comment(request, id):
    comment_to_delete = Comment.objects.get(id=id)
    comment_to_delete.delete()
    return redirect('/newsfeed')

def photos(request):
    return render(request, 'photos.html')
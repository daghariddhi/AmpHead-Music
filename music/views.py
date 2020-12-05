from django.shortcuts import render
from music.models import Song, Watchlater


from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect
from django.db.models import Case, When
def songs(request):
    song = Song.objects.all()
    return render(request, 'music/songs.html',  {'song': song})

def songpost(request, id):
    song = Song.objects.filter(song_id=id).first()
    return render(request, 'music/songpost.html', {'song': song})

def login(request):
    # if request.method == "POST":
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(username=username, password=password)

    #     if user is not None:
    #         login(request, user)
    #         return redirect("/")
    #     else:
    #         messages.info(request, 'Invalid Username or Password')
    #         return redirect('login')

    # else:
    #     return render(request, 'music/login.html')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        from django.contrib.auth import login
        login(request, user)   
        redirect("/")

    return render(request, 'music/login.html')

def signup(request): 
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please try another one !")
            return redirect("/")

        if len(username) > 15:
            messages.error(request, "Username must be less than 15 characters")
            return redirect("/")
        
        if not username.isalnum():
            messages.error(request, "Username should only contain Letters and Numbers.")

        if pass1 != pass2:
            messages.error(request, "Password Do not Match. Please Sign Up Again")
            return redirect("/")


            
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        user = authenticate(username=username, password=pass1)
        from django.contrib.auth import login
        login(request, user)

        # channel = Channel(name=username)
        # channel.save()

        return redirect('/')

    return render(request, 'music/signup.html')

def logout_user(request):
    logout(request)
    return redirect("/")

# def listenlater(request):
#     if request.method == "POST":
#         user = request.user
#         video_id = request.POST['video_id']

#         watch = Listenlater.objects.filter(user=user)
        
#         for i in watch:
#             if video_id == i.video_id:
#                 message = "Your Video is Already Added"
#                 break
#         else:
#             watchlater = Listenlater(user=user, video_id=video_id)
#             watchlater.save()
#             message = "Your Video is Succesfully Added"

#         song = Song.objects.filter(song_id=video_id).first()
#         return render(request, "music/songpost.html", {'song': song, "message": message})
#     wl = Listenlater.objects.filter(user=request.user)
#     ids = []
#     for i in wl:
#         ids.append(i.video_id)
    
#     preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
#     song = Song.objects.filter(song_id__in=ids).order_by(preserved)

#     return render(request, "music/listenlater.html", {'song': song})

def watchlater(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user=user)
        
        for i in watch:
            if video_id == i.video_id:
                message = "Your Video is Already Added"
                break
        else:
            watchlater = Watchlater(user=user, video_id=video_id)
            watchlater.save()
            message = "Your Video is Succesfully Added"

        song = Song.objects.filter(song_id=video_id).first()
        return render(request, f"music/songpost.html", {'song': song, "message": message})

    wl = Watchlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "music/watchlater.html", {'song': song})


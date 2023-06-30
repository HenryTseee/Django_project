from django.shortcuts import render
import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from forum.forms import LogMessageForm
from forum.models import LogMessage


from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from forum.models import Post, Replie, Profile
from forum.forms import ProfileForm
from django.contrib.auth.decorators import login_required


class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "forum/about.html")

def contact(request):
    return render(request, "forum/contact.html")

def hello_there(request, name):
    return render(
        request,
        'forum/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )
    
def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "forum/log_message.html", {"form": form})
    
##forum

def discussionforum(request):
    profile = Profile.objects.all()
    if request.method=="POST":   
        user = request.user
        image = request.user.profile.image
        content = request.POST.get('content','')
        post = Post(user1=user, post_content=content, image=image)
        post.save()
        alert = True
        return render(request, "forum/discussionforum.html", {'alert':alert})
    posts = Post.objects.filter().order_by('-timestamp')
    return render(request, "forum/discussionforum.html", {'posts':posts})

def discussion(request, myid):
    post = Post.objects.filter(id=myid).first()
    replies = Replie.objects.filter(post=post)
    if request.method=="POST":
        user = request.user
        image = request.user.profile.image
        desc = request.POST.get('desc','')
        post_id =request.POST.get('post_id','')
        reply = Replie(user = user, reply_content = desc, post=post, image=image)
        reply.save()
        alert = True
        return render(request, "forum/discussion.html", {'alert':alert})
    return render(request, "forum/discussion.html", {'post':post, 'replies':replies})
    
def UserRegister(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'forum/login.html')        
    return render(request, "forum/register.html")

def UserLogin(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/myprofile")
        else:
            messages.error(request, "Invalid Credentials")
        alert = True
        return render(request, 'forum/login.html', {'alert':alert})            
    return render(request, "forum/login.html")

def UserLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

@login_required(login_url = '/login')
def myprofile(request):
    if request.method=="POST":
        user = request.user
        profile = Profile(user=user)
        profile.save()
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "forum/profile.html",{'obj':obj})
    else:
        form=ProfileForm()
    return render(request, "forum/profile.html", {'form':form})
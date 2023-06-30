from django.urls import path
from forum import views
from forum.models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="forum/home.html",
)

urlpatterns = [
    path("home", home_list_view, name="home"),
    path("", views.discussionforum, name="Forum"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("forum/<name>", views.hello_there, name="hello_there"),
    path("log/", views.log_message, name="log"),
    path("discussion/<int:myid>/", views.discussion, name="Discussions"),
    path("register/", views.UserRegister, name="Register"),
    path("login/", views.UserLogin, name="Login"),
    path("logout/", views.UserLogout, name="Logout"),
    path("myprofile/", views.myprofile, name="Myprofile"),
]
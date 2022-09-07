from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

admin.autodiscover()

import mainapp.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("stuff", mainapp.views.index, name="index"),
    path("db/", mainapp.views.db, name="db"),
    path("admin/", admin.site.urls),
    path("", mainapp.views.home),
    path("register/", mainapp.views.home, name="register"),
    path("dbdump/", mainapp.views.dbdump),
    path("main/", mainapp.views.main, name="main"),
    path("profile/", mainapp.views.profile),
    path("editprofile/", mainapp.views.editprofile),
    path("saveprofile/", mainapp.views.saveprofile),
    path("matchhistory/", mainapp.views.matchhistory),
    path("gamepreferences/", mainapp.views.gamepreferences),
    path("opengames/", mainapp.views.opengames),
    path("event/", mainapp.views.event, name='event'),
    path('login/', auth_views.LoginView.as_view(template_name='checkmates/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='checkmates/logout.html'), name='logout'),
    path('main/locateUsr', mainapp.views.main, name="locateUsr"),
    path('getfeed/',mainapp.views.getfeed),
    path('like/',mainapp.views.like),
    path('dislike/',mainapp.views.dislike),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

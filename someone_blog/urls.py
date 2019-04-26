from django.contrib import admin
from django.urls import path, include
from .views import Login, Logout, handler404, handler500

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r"login/", Login.as_view(), name="login_url"),
    path(r"logout/", Logout.as_view(), name="logout_url"),
    path(r'', include("cms.urls"))
]

handler404 = handler404
handler500 = handler500

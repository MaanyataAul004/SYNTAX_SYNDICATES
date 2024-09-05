from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('report/', views.report_view, name="report"),
    path('report_success/', views.report_success_view, name="report_success"),
    path('reports/', views.report_list_view, name="report_list"),
    path('about/',views.about, name="about"),
    path('contact',views.contact,name="contact")

]



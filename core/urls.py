from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("programme/", views.programme, name="programme"),
    path(
        "programme/session/<int:pk>/",
        views.session_detail,
        name="session_detail",
    ),

    path("members/", views.members, name="members"),
    path(
        "members/<slug:slug>/",
        views.member_detail,
        name="member_detail",
    ),

    path("subgroups/", views.subgroups, name="subgroups"),
    path(
        "subgroups/<slug:slug>/",
        views.subgroup_detail,
        name="subgroup_detail",
    ),

    path("contact/", views.contact, name="contact"),
]
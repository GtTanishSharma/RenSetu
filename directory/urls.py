from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("solutions/", views.solutions, name="solutions"),
    path("solutions/<slug:slug>/", views.category_detail, name="category"),
    path("dealers/", views.dealers, name="dealers"),
    path("dealers/<slug:slug>/", views.city_detail, name="city"),
    path("tools/", views.tools, name="tools"),
    path("tools/<slug:slug>/", views.tool_detail, name="tool"),
    path("learn/", views.learn, name="learn"),
    path("learn/<slug:slug>/", views.guide_detail, name="guide"),
    path("get-quotes/", views.enquiry, name="enquiry"),
    path("list-your-business/", views.list_business, name="list_business"),
    path("about/", views.about, name="about"),
]
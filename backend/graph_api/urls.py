from django.urls import path

from . import views

urlpatterns = [
    path("people/", views.people, name="people"),
    path("skills/", views.skills, name="skills"),
    path("jobs/", views.jobs, name="jobs"),
    path("companies/", views.companies, name="companies"),

    path(
        "people/<str:name>/skills/",
        views.person_skills,
        name="person_skills",
    ),

    path(
        "people/<str:name>/recommendations/",
        views.recommendations,
        name="recommendations",
    ),

    path(
        "people/<str:name>/companies/",
        views.company_recommendations,
        name="company_recommendations",
    ),
]
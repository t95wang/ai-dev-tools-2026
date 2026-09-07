from django.urls import path

from . import views

app_name = "chores"

urlpatterns = [
    path("", views.chore_list, name="list"),
    path("new/", views.chore_create, name="create"),
    path("<int:chore_id>/claim/", views.chore_claim, name="claim"),
    path("<int:chore_id>/complete/", views.chore_complete, name="complete"),
]

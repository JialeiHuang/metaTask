from django.urls import path

from lists import views

app_name = "lists"
urlpatterns = [
    path("", views.index, name="index"),
    path("todolist/<int:todolist_id>/", views.todolist, name="todolist"),
    path("todolist/new/", views.new_todolist, name="new_todolist"),
    path("todolist/add/", views.add_todolist, name="add_todolist"),
    path("todo/add/<int:todolist_id>/", views.add_todo, name="add_todo"),
    path("todolists/", views.overview, name="overview"),

    path("grouplist/<int:grouplist_id>/", views.grouplist, name="grouplist"),
    path("grouplist/new/", views.new_grouplist, name="new_grouplist"),
    path("grouplist/add/", views.add_grouplist, name="add_grouplist"),
    path("group/add/<int:grouplist_id>/", views.add_group, name="add_group"),
]

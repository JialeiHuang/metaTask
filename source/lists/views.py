from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib import messages

from lists.forms import TodoForm, TodoListForm, GroupForm, GroupListForm
from lists.models import Todo, TodoList, Group, GroupList

def index(request):
    return render(request, "lists/index.html", {"form": TodoListForm()})
    #return render(request, "lists/index.html", {"form": TodoForm()})
   # return render(request, "lists/base.html", {"form": TodoForm()})


def todolist(request, todolist_id):
    todolist = get_object_or_404(TodoList, pk=todolist_id)
    if request.method == "POST":
        redirect("lists:add_todo", todolist_id=todolist_id)

    return render(
        request, "lists/todolist.html", {"todolist": todolist, "form": TodoForm()}
    )


def add_todo(request, todolist_id):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todo = Todo(
                description=request.POST["description"],
                title=request.POST["title"],
                todolist_id=todolist_id,
                creator=user,
            )
            todo.save()
            return redirect("lists:todolist", todolist_id=todolist_id)
        else:
            return render(request, "lists/todolist.html", {"form": form})

    return redirect("lists:index")


@login_required
def overview(request):
    if request.method == "POST":
        return redirect("lists:add_todolist")
    return render(request, "lists/overview.html", {"form": TodoListForm()})


def new_todolist(request):
    if request.method == "POST":
        form = TodoListForm(request.POST)
        print("#"*40)
        print(form)
        print("#"*40)
        print(request.POST)
        if form.is_valid():
            # create default todolist
            user = request.user if request.user.is_authenticated else None
            print(request)
            todolist = TodoList(creator=user, title=request.POST['title'])
            todolist.save()
            return redirect("lists:todolist", todolist_id=todolist.id)
        else:
            return render(request, "lists/index.html", {"form": TodoListForm})

    return redirect("lists:index")


def add_todolist(request):
    if request.method == "POST":
        form = TodoListForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todolist = TodoList(title=request.POST["title"], creator=user)
            todolist.save()
            return redirect("lists:todolist", todolist_id=todolist.id)
        else:
            return render(request, "lists/overview.html", {"form": TodoListForm})

    return redirect("lists:index")


def grouplist(request, grouplist_id):
    grouplist = get_object_or_404(GroupList, pk=grouplist_id)
    if request.method == "POST":
        redirect("lists:add_group", grouplist_id=grouplist_id)

    return render(
        request, "lists/grouplist.html", {"grouplist": grouplist, "form": GroupForm()}
    )


def add_group(request, grouplist_id):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            group = Group(
                description=request.POST["description"],
                grouplist_id=grouplist_id,
                creator=user,
            )
            group.save()
            return redirect("lists:grouplist", grouplist_id=grouplist_id)
        else:
            return render(request, "lists/grouplist.html", {"form": form})

    return redirect("lists:index")
# # only one useful
# def join_group(request, grouplist_id):
#     if request.method == "POST":
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             user = request.user if request.user.is_authenticated else None
             
#             return redirect("lists:grouplist", grouplist_id=grouplist_id)
#         else:
#             return render(request, "lists/grouplist.html", {"form": form})

#     return redirect("lists:index")


def new_grouplist(request):
    print("here is new grouplist")
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            # create default todolist
            user = request.user if request.user.is_authenticated else None
            # print(request.title)
            # import ipdb; ipdb.set_trace()
            grouplist = GroupList(creator=user)
            grouplist.save()
            group = Group(
                description=request.POST["description"],
                grouplist_id=grouplist.id,
                creator=user,
            )
            group.save()
            return redirect("lists:grouplist", grouplist_id=grouplist.id)
        else:
            return render(request, "lists/index.html", {"form": form})

    return redirect("lists:index")


def add_grouplist(request):
    if request.method == "POST":
        form = GroupListForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            grouplist = GroupList(title=request.POST["title"], creator=user)
            grouplist.save()
            return redirect("lists:grouplist", grouplist_id=grouplist.id)
        else:
            return render(request, "lists/overview.html", {"form": form})

    return redirect("lists:index")

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import ToDoList, ToDoItem

# Create your views here.

def todo_view(request):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')
    else:
        todos = ToDoList.objects.filter(user_id=user_id)
        if len(todos) == 0:
            return redirect('todo_detail', id=0)
        return redirect('todo_detail', id=todos[0].id)

def todo_detail_view(request, id):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')
    else:
        todos = ToDoList.objects.filter(user_id=user_id)
        items = ToDoItem.objects.filter(todo_list_id=id)
        context = {
            'todos': todos,
            'todo_id': id,
            'items': items,
        }
        return render(request, 'home/todo.html', context)
        
def create_new_todo_view(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id') 
        todo_name = request.POST.get('todo_name')
        if(todo_name != '' and todo_name != None and ToDoList.objects.filter(title=todo_name,user_id=user_id).count() == 0):
            todo = ToDoList(title=todo_name, user_id=user_id)
            todo.save()
            return redirect('todo_detail', id=todo.id)
        else:
            todos = ToDoList.objects.filter(user_id=user_id)
            items = ToDoItem.objects.filter(todo_list_id=0)
            context = { 
                'error': 'This list already exists',
                'todos': todos,
                'items': items,
            }
            return render(request, 'home/todo.html', context)
    return todo_view(request)

def delete_todo_view(request, id):
    user_id = request.session.get('user_id')
    if user_id is None:
        return redirect('login')
    else:
        todos = ToDoList.objects.filter(user_id=user_id)
        todo = get_object_or_404(ToDoList, id=id)
        items = ToDoItem.objects.filter(todo_list_id=id)
        for item in items:
            item.delete()
        todo.delete()
        if len(todos) == 0:
            return redirect('todo')
        return redirect('todo_detail', id=todos[0].id)

def create_item_view(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id') 
        item_name = request.POST.get('item_name')
        todo_id = request.POST.get('todo_id')
        if todo_id != '' and todo_id != None:
            if(item_name != '' and item_name != None and ToDoItem.objects.filter(title=item_name,todo_list_id=todo_id).count() == 0):
                todo = ToDoList.objects.filter(id=todo_id)
                if todo:
                    item = ToDoItem(title=item_name, todo_list_id=todo_id)
                    item.save()
                return redirect('todo_detail', id=todo_id)
        else:
            todos = ToDoList.objects.filter(user_id=user_id)
            return redirect('todo_detail', id=todos[0].id)
    return todo_view(request)

def delete_item_view(request, id):
    item = get_object_or_404(ToDoItem, id=id)
    item.delete()
    return redirect('todo_detail', id=item.todo_list.id)

def delete_all_item_view(request, id):
    todo = get_object_or_404(ToDoList, id=id)
    items = ToDoItem.objects.filter(todo_list_id=id)
    for item in items:
        item.delete()
    return redirect('todo_detail', id=todo.id)

def sort_item_view(request, id):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id is None:
            return redirect('login')
        else:
            todos = ToDoList.objects.filter(user_id=user_id)
            items = ToDoItem.objects.filter(todo_list_id=id).order_by('title')
            context = {
                'todos': todos,
                'todo_id': id,
                'items': items
            }
            return render(request, 'home/todo.html', context)

def search_item_view(request):
    if request.method == 'GET':
        todo_id = request.GET.get('search_todo_id')
        text = request.GET.get('text_search')
        if(text != '' and text != None):
            items = ToDoItem.objects.filter(todo_list_id=todo_id, title__contains=text)
        else:
            items = ToDoItem.objects.filter(todo_list_id=todo_id)
        user_id = request.session.get('user_id')
        if user_id is None:
            return redirect('login')
        else:
            todos = ToDoList.objects.filter(user_id=user_id)
        context = {
            'todos': todos,
            'todo_id': todo_id,
            'items': items
        }
        return render(request, 'home/todo.html', context)
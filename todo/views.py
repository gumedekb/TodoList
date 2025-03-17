from  django . shortcuts  import  render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from . import models
from todo.models import TODOO
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/login')
def home(request):
    return render(request, 'signup.html')


def signup(request):
    if request.method == 'POST':
        userName=request.POST.get('userName')
        userEmail=request.POST.get('userEmail')
        password=request.POST.get('password')
        # print(userName,userEmail,password)
        my_user=User.objects.create_user(userName,userEmail,password)
        my_user.save()
        return redirect('/login')
    
    return render(request, 'signup.html')
        
     
def user_login(request):
    if request.method == 'POST':
        userName=request.POST.get('userName')
        password=request.POST.get('password')
        # print(userName,password)  # No need to print
        userr=authenticate(request,username=userName,password=password)
        if userr is not None:
            auth_login(request,userr)
            return redirect('/todopage')
        else:
            return redirect('/login')
               
    return render(request, 'login.html')


@login_required(login_url='/login')
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        todo_id = request.POST.get('srno')  
        status = request.POST.get('status')  

        if todo_id:  # If there is a task ID, update the existing task
            try:
                todo_item = models.TODOO.objects.get(srno=todo_id) 
                if title:
                    todo_item.title = title  
                if status is not None:
                    todo_item.status = True  
                else:
                    todo_item.status = False  
                todo_item.save()  
            except models.TODOO.DoesNotExist:
                # Handle the case where the task does not exist, if necessary
                pass
        else:  # If there is no todo_id, it's a new task, create a new one
            if title:  
                obj = models.TODOO(title=title, user=request.user)
                obj.save()  

        # Get the updated list of todos for the user
        user = request.user
        res = models.TODOO.objects.filter(user=user).order_by('-date')

        # Redirect to the todopage with the updated list
        return redirect('/todopage', {'res': res})

    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html', {'res': res})


# @csrf_exempt
def update_task_status(request):
    if request.method == "POST":
        todo_id=request.POST.get('srno')
        status=request.POST.get('status') == 'on'  # Check if status is 'on' (checked)

        try:
            todo_item = TODOO.objects.get(srno=todo_id)
            todo_item.status = status
            todo_item.save()
            return JsonResponse({'status': 'success', 'new_status': status})
        except TODOO.DoesNotExist:
            return JsonResponse({'status': 'success', 'new_status': status})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def delete_todo(request,srno):
    print(srno)
    obj=models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')


@login_required(login_url='/login')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODOO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')

    obj = models.TODOO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})


def signout(request):
    logout(request)
    return redirect('/login')


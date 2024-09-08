
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Job

# Create your views here.
def home(request):
    return render(request,'home.html')

@login_required(login_url='/user_login')
def jobs(request):
    page_num=request.GET.get('page',1)
    data=Job.objects.all()
    pagination=Paginator(data,7)
    jobs=pagination.get_page(page_num)

    return render(request,'jobs.html',{'jobs':jobs})

def details(request,k):
    jobs = Job.objects.get(id=k)
    print(id)
    return render(request,'details.html',{'job':jobs})

def search(request):
    page_num=request.GET.get('page',1)
    query = request.GET.get('q')
    t_c = request.GET.get('t_c')
    loc = request.GET.get('loc')
    data = Job.objects.all()
    k=''
    if t_c:
      
        data = data.filter(Q(title__icontains=t_c) | Q(company__icontains=t_c))
        k=t_c
    if loc:
       
        data = data.filter(location__icontains=loc)
        k=loc
    data = data.order_by('id')
    pagination = Paginator(data,7)
    jobs =pagination.get_page(page_num)

    prop = {
        'jobs': jobs,
        't_c': t_c,
        'loc': loc,
        'k': k
    }
    
    return render(request, 'jobs.html', prop)

# User Signup View
def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        # Create new user
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('jobs') 
    else:
        form = SignupForm()
    
    return render(request, 'user_signup.html')

# User Login View
def user_login(request):
    if request.method=='POST':
        usr=request.POST.get('username')
        pwd=request.POST.get('password')
        user=fetch_user_by_username(usr)
        if user:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            if user.password==pwd:
                login(request,user)
                return redirect('jobs')
            else:
                messages.add_message(request,messages.ERROR,'Invalid Credentials')
                return redirect('user_login')
        else:
            messages.add_message(request,messages.ERROR,'User Does Not Exist')
            return redirect('user_login')
    else:
        form=AuthenticationForm()
    return render(request, 'user_login.html')

def fetch_user_by_username(usr):
    User=get_user_model()
    try:
        user=User.objects.get(email=usr)
        return user
    except User.DoesNotExist:
        return None

def user_logout(request):
    logout(request)
    return render(request,'user_login.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contactUs.html')
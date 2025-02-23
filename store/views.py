from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,UserUpdateForm,ChangePasswordForm,UserInfoForm
from .models import Product, Category, Profile
from django.db.models import Q



def search(request):
   
	# Determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        # Query The Products DB Model
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.success(request, ("Sorry That Product Not Exist, Please Try Again ..!"))
            return render(request,"search.html",{})
            
        
        else:
            return render(request,"search.html",{"searched":searched})
        
   
    else:
        return render(request,"search.html",{})
        

    
    

    

def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html',{'categories':categories})

def category(request,foo):
    # repplace hyphens with spaces
    foo =foo.replace("-",' ')

    #grab category from the  url
    try:
        #llok up the category
        category = Category.objects.get(name=foo)

        products = Product.objects.filter(category=category)

        return render(request,'category.html',{'products':products,'category':category})


        
    except:

        messages.success(request, ("That category Doesn't Exist sorry ..!"))
        return redirect('home')



def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,"product.html",{'product':product})


def home(request):
    products = Product.objects.all()
    return render(request,"home.html",{'products':products})

def about(request):
    return render(request,"about.html")

def login_user(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate (request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You Have Been Succesfully Logged In ..!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an Error, Please Try Again..!"))
            return redirect('login')
    else:
           
        return render(request,"login.html")

def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Succesfully Logged Out ..!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # log in user
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, ("UserName Created Successfully  - Please Fill Out Your User Info Below !"))
            return redirect('update_info')
        else:
            messages.success(request, ("Whoops ! There was a Problem in Registering, Please Try Again..!"))
            return redirect('register')
    
    else:
        return render(request,"register.html",{ 'form':form })
    
def update_user(request):
    if request.user.is_authenticated:
        current_user= User.objects.get(id=request.user.id)
        user_form=UserUpdateForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()

            login(request,current_user)

            messages.success(request,"User Has Been Updated Successfully !!!..")

            return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form})
    else:
        messages.success(request,"You Need To Be Logged In To Access This Page")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        # did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)

            if form.is_valid():
                form.save()
                messages.success(request,"Your Password Has Been Updated!!..")
                login(request,current_user)

                return redirect("update_user")
            else:
                for error in form.errors.values():
                    messages.error(request,error)
                    return redirect('update_password')
           
            

        else:

            form = ChangePasswordForm(current_user)
            return render(request,"update_password.html",{'form':form})
    else:
        messages.success(request,"You Need To Be Logged In To Access This Page")
        return redirect('home')
    

def update_info(request):
    if request.user.is_authenticated:
        current_user= Profile.objects.get(user__id=request.user.id)
        form=UserInfoForm(request.POST or None, instance=current_user)
        
        if form.is_valid():
            form.save()

            messages.success(request,"User Info Has Been Updated Successfully !!!..")

            return redirect('home')
        return render(request,"update_info.html",{'form':form})
    else:
        messages.success(request,"You Need To Be Logged In To Access This Page")
        return redirect('home')
    




        

        

    
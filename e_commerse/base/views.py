from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'register/loginpage.html')
def signup(request):
    return render(request,'register/signuppage.html')
def user_account(request):
    return render(request,'try/user_account.html')

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from .models import UserProfile, Project, ProjectView
import os


def home_page(request):
    if request.user.is_authenticated:
        projects = Project.objects.all()
        context = {
            'projects': projects
        }
        return render(request, 'home.html', context=context)
    else:
        return redirect('login')
    
def modal_hided(request):
    request.session["infoHidden"] = True
    return redirect('home')

def account_page(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get_or_create(user=request.user)[0]
        if request.method == 'POST':
            avatar_file  = request.FILES.get('avatar')
            if avatar_file:
                if user.avatar:
                    if user.avatar != "avatars/default.png":
                        old_avatar_path = user.avatar.path
                        if os.path.exists(old_avatar_path):
                            os.remove(old_avatar_path)
                user.avatar = avatar_file
                user.save()
                user = UserProfile.objects.get(user=request.user)
        context = {
            'user': user
        }
        return render(request, 'account.html', context=context)
    else:
        return redirect('login')

def project_detail_page(request, project_id):
    if request.user.is_authenticated:
        project = Project.objects.get(id=project_id)
        context = {
            'project': project
        }
        if not ProjectView.objects.filter(project=project, user=request.user).exists():
            ProjectView.objects.create(project=project, user=request.user)
            project.views = ProjectView.objects.filter(project=project).count()
            project.save()
            project = Project.objects.get(id=project_id)
        return render(request, 'project_detail.html', context=context)
    else:
        return redirect('login')

def delete_avatar(request):
    if request.user.is_authenticated:
        user = UserProfile.objects.get(user=request.user)
        if user.avatar:
            if user.avatar != "avatars/default.png":
                old_avatar_path = user.avatar.path
                if os.path.exists(old_avatar_path):
                    os.remove(old_avatar_path)
        user.avatar = 'avatars/default.png'
        user.save()
        return redirect('account')
    else:
        return redirect('login')

def delete_project(request, project_id):
    if request.user.is_authenticated:
        Project.objects.get(id=project_id).delete()
        return redirect('home')
    else:
        return redirect('login')
    
def add_project_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            description = request.POST.get('description')
            Project.objects.create(user=request.user, name=name, description=description)
        return render(request, 'add_project.html')
    else:
        return redirect('login')

def forgot_password(request):
    if not request.user.is_authenticated:
        context = {
            'code': False,
            'password': False
        }
        if request.method == 'POST':
            receiver_email = request.POST.get('email')
            context['email'] = receiver_email
            code = request.POST.get('code')
            new_password = request.POST.get('password')
            if User.objects.filter(email=receiver_email).exists():
                if code == None:
                    verification_code = randint(100000, 999999)
                    user = User.objects.get(email=receiver_email)
                    user_profile = UserProfile.objects.get_or_create(user=user)[0]
                    user_profile.verification_code = verification_code
                    user_profile.save()
                    my_email = "shoprbexruzroot@gmail.com"
                    password = "gzdb jszm porl qnwy"
                    message = f"Ваш код для подтверждения: {verification_code}"
                    msg = MIMEMultipart()
                    msg['From'] = my_email
                    msg['To'] = receiver_email
                    msg['Subject'] = 'Код подтверждения'
                    msg.attach(MIMEText(message, 'plain'))
                    try:
                        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                            server.starttls()
                            server.login(my_email, password)
                            server.sendmail(my_email, receiver_email, msg.as_string())
                            context['code'] = True
                    except Exception as e:
                        print(f"Ошибка при отправке кода подтверждения: {e}")
                else:
                    if new_password == None:
                        user = User.objects.get(email=receiver_email)
                        user_profile = UserProfile.objects.get(user=user)
                        if int(user_profile.verification_code) == int(code):
                            context['password'] = True
                            context['input_code'] = int(user_profile.verification_code)
                        else:
                            context['error'] = 'Incorrect verification code'
                            context['code'] = True
                    else:
                        user = User.objects.get(email=receiver_email)
                        if len(new_password) >= 8:
                            user.set_password(new_password)
                            user.save()
                            return redirect('login')
                        else:
                            user_profile = UserProfile.objects.get(user=user)
                            context['input_code'] = int(user_profile.verification_code)
                            context['error'] = "Password must be at least 8 characters"
                            context['password'] = True
            else:
                context['error'] = 'Invalid email address'
        return render(request, 'forgot_password.html', context=context)
    else:
        return redirect('home')

def login_page(request):
    if not request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                context['error'] = "Username or password incorrect"
        return render(request, "login.html", context=context)
    else:
        return redirect("home")

def register_page(request):
    if not request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            email = request.POST.get('email')
            if len(password1) <= 8:
                if not User.objects.filter(email=email).exists():
                    if not username.isdigit():
                        if not User.objects.filter(username=username).exists():
                            if password1 == password2:
                                user = User.objects.create_user(
                                    username=username, password=password1, email=email
                                )
                                login(request, user)
                                return redirect("home")
                            else:
                                context['error'] = "Passwords don't match"
                        else:
                            context['error'] = "Username already taken"
                    else:
                        context['error'] = "Username mustn't contain only numbers"
                else:
                    context['error'] = "Email already taken"
            else:
                context['error'] = "Password must be at least 8 characters"
        return render(request, "register.html", context=context)
    else:
        return redirect('home')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("login")
    else:
        return redirect('home')
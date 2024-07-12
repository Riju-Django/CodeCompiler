from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import *
from .models import *
from .helper import *

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # You may log in the user immediately after signup if needed
            login(request, user)
            return redirect('dashboard')  # Replace 'dashboard' with your desired URL name
    else:
        form = SignupForm()
    return render(request, 'side/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Replace 'dashboard' with your desired URL name
    else:
        form = LoginForm()
    return render(request, 'side/login.html', {'form': form})


@login_required
def dashboard_view(request):
    code = None
    response = []
    language = None
    result_title = "Accepted"
    languages = get_language()
    error_str = ""
    testcases = [
        {
            "test_case": 1,
            "status": True,
            "input_list": [2, 3],
            "expected_output": 5,
            "actual_output": 5
        },
        {
            "test_case": 2,
            "status": True,
            "input_list": [1, 3],
            "expected_output": 4,
            "actual_output": 4
        },
        {
            "test_case": 3,
            "status": False,
            "input_list": [5, 3],
            "expected_output": 8,
            "actual_output": 5
        }
    ]
    data = Question.objects.all()
    question_details = None
    selected_id = None
    if request.method == "POST":
        selected_id = request.POST.get("selected_q")
        post_select_q_id = request.POST.get("sel_q_id")
        action = request.POST.get("action")
        code = request.POST.get("source_code")
        language = request.POST.get("language")
        if language != "null":
            language = int(language)
        if action == "Run" or action == "Submit":
            testcase = Question.objects.filter(id=int(post_select_q_id)).first().testcase
            if testcase:
                testcase = testcase.get("testcase")
            response = code_compiler(code, language, testcase)
    if not selected_id:
        selected_id = data.first().id
    else:
        selected_id = int(selected_id)
    question_details = Question.objects.filter(id=int(selected_id)).first()   
    return render(request, 'side/dashboard.html', {
        "items": data,
        "question_details": question_details,
        "result_title": result_title,
        "error_str": error_str,
        "testcases": testcases,
        "code": code,
        "selected_language": language,
        "languages": languages,
        "response": response,
    })


@login_required
def code_Compiler_view(request, qus_id):
    data = get_list_or_404(Question, id=qus_id)
    return render(request, 'side/code_compiler.html', {"item":data})

def logout_view(request):
    logout(request)
    return redirect('login')


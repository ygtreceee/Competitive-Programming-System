from django.shortcuts import render, HttpResponse, redirect
from app import models
from django import forms
from app.utils.pagination import Pagination
from django.utils.safestring import mark_safe
from app.utils.form import ProblemForm, UserForm, LoginForm
# Create your views here.


def index(request):
    info = request.session.get('info')
    if info is None:
        cf_queryset = models.CodeforcesContestInfo.objects.all()
        atc_queryset = models.AtcoderContestInfo.objects.all()
    else:
        dataUser = models.ContestUser.objects.filter(user_id=info['id']).values('contest_id')
        codeforcesUser = models.CodeforcesUser.objects.filter(user_id=info['id']).values('contest_id')
        cf_queryset = models.CodeforcesContestInfo.objects.exclude(id__in=codeforcesUser)
        atc_queryset = models.AtcoderContestInfo.objects.exclude(id__in=dataUser)

    context = {
        'title': 'Home',
        'cf_queryset': cf_queryset,
        'atc_queryset': atc_queryset,
    }
    return render(request, 'index.html', context)

def mylist(request):
    info = request.session.get('info')
    if info is None:
        cf_queryset = []
        atc_queryset = []
    else:
        dataUser = models.ContestUser.objects.filter(user_id=info['id']).values('contest_id')
        codeforcesUser = models.CodeforcesUser.objects.filter(user_id=info['id']).values('contest_id')
        cf_queryset = models.CodeforcesContestInfo.objects.filter(id__in=codeforcesUser)
        atc_queryset = models.AtcoderContestInfo.objects.filter(id__in=dataUser)

    context = {
        'title': 'Home',
        'cf_queryset': cf_queryset,
        'atc_queryset': atc_queryset,
    }
    return render(request, 'myindex.html', context)

def attend(request, id,type):
    info = request.session.get('info')
    if type == '2':
        contestUser = models.ContestUser()
        contestUser.contest_id=id
        contestUser.user_id=info['id']
        contestUser.save()
    else:
        print(type)
        codeforcesUser = models.CodeforcesUser()
        codeforcesUser.contest_id=id
        codeforcesUser.user_id=info['id']
        codeforcesUser.save()  
    context = {
        'title': 'SUCCESS'
    }
    return redirect("http://127.0.0.1:8000/index")

def attendDelete(request, id,type):
    info = request.session.get('info')
    if type == '2':
        models.ContestUser.objects.filter(user_id=info['id'],contest_id=id).delete()
    else:
        models.CodeforcesUser.objects.filter(user_id=info['id'],contest_id=id).delete()
    context = {
        'title': 'SUCCESS'
    }
    return redirect("http://127.0.0.1:8000/mylist")

def Problem_list(request):
    if request.method == 'GET':
        info = request.session.get('info')
        if info is None:
            return redirect('/login')
        else:
            page_object = Pagination(request, per_page=5, table_name='FavoriteProblem')
            context = {
                'queryset': page_object.page_range(),
                'search_value': page_object.search_value,
                'page_index_string': mark_safe(page_object.page_index_string()),
                'title': 'ProblemSet',
            }
            return render(request, 'ProblemManagement.html', context)
    else:
        form = ProblemForm(data=request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user_id = 1
            problem.save()
            return redirect('http://localhost:8000/ProblemManagement/list')
        else:
            render(request, 'ProblemManagement.html', {'form': form})

def Problem_add(request):
    if request.method == 'GET':
        problem_title = request.GET.get('title', "")
        link = request.GET.get('link', "")
        # print(problem_title, link)
        form = ProblemForm(initial={'title': problem_title, 'link': link})
        context = {
            'form': form,
            'title': 'Add Problem',
        }
        return render(request, 'FavorProAdd.html', context)
    else:
        form = ProblemForm(data=request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user_id = 1
            problem.save()
            return redirect('http://localhost:8000/ProblemManagement/list')
        else:
            render(request, 'ProblemManagement.html', {'form': form})

def Problem_delete(request, nid):
    models.FavoriteProblem.objects.filter(id=nid).delete()
    return redirect('http://localhost:8000/ProblemManagement/list')


def Problem_edit(request, nid):
    if request.method == 'GET':
        form = ProblemForm(instance=models.FavoriteProblem.objects.get(id=nid))
        context = {
            'form': form,
            'title': 'Edit Problem',
        }
        return render(request, 'FavorProEdit.html', context)
    else:
        form = ProblemForm(instance=models.FavoriteProblem.objects.get(id=nid), data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/ProblemManagement/list')
        else:
            render(request, 'FavorProEdit.html', {'form': form})


def loginPage(request):
    if request.method == 'GET':
        form = LoginForm()
        context = {
            'form': form,
            'title': 'Login Page',
        }
        return render(request, 'loginPage.html', context)
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            # user_object = models.UserInfo.objects.get(**form.cleaned_data)
            user_object = models.UserInfo.objects.filter(**form.cleaned_data).first()
            if user_object is not None:
                request.session['info'] = {'id': user_object.id, 'username': user_object.username}
                return redirect('/index')
            else:
                form.add_error('username', "Wrong user name or password!")
                # print(form.errors)
                # print(form.cleaned_data['username'], form.cleaned_data['password'])
                return render(request, 'loginPage.html', {'form': form})


def registerPage(request):
    if request.method == 'GET':
        form = UserForm()
        context = {
            'form': form,
            'title': 'Register Page',
        }
        return render(request, 'registerPage.html', context)
    else:
        form = UserForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/index')


def logoutPage(request):
    request.session.pop('info', None)
    return redirect('http://localhost:8000/index')


def profilePage(request, nid):
    if request.method == 'GET':
        form = UserForm(instance=models.UserInfo.objects.get(id=nid))
        context = {
            'form': form,
            'title': 'Profile',
        }
        return render(request, 'profilePage.html', context)
    else:
        form = UserForm(instance=models.UserInfo.objects.get(id=nid), data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://localhost:8000/logout')
        else:
            render(request, 'profilePage.html', {'form': form})


def layoutPage(request):
    return render(request, 'layout.html')


def ProblemSetPage(request):
    if request.method == 'GET':
        page_object = Pagination(request, per_page=10, page_index_range=3, private=False, table_name='ProblemSet')
        context = {
            'queryset': page_object.page_range(),
            'search_value': page_object.search_value,
            'page_index_string': mark_safe(page_object.page_index_string()),
            'title': 'ProblemSet',
        }
        return render(request, 'ProblemSetPage.html', context)
    # else:
    #     form = ProblemForm(data=request.POST)
    #     if form.is_valid():
    #         problem = form.save(commit=False)
    #         problem.user_id = 1
    #         problem.save()
    #         return redirect('http://localhost:8000/ProblemManagement/list')
    #     else:
    #         render(request, 'ProblemManagement.html', {'form': form})






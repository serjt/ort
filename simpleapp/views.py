# coding=utf-8
import os

import numpy as np
import xlsxwriter
import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse, Http404
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from simpleapp.models import Faculty, Tour, Alumni, AlumniLesson, Lesson, Lgotnik


def sign_in(request):
    c = {}
    c.update(csrf(request))
    return render(request, 'sign_in.html', c)


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    print(username, password)
    if user is not None:
        auth.login(request, user)
        return redirect('/tour/')
    else:
        return redirect('/sign_in/')


@login_required
def all_tables(request):
    user = request.user
    now = datetime.datetime.now()
    tours = Tour.objects.filter(initial__lte=now, final__gte=now)
    if tours.count() > 0:
        context = {
            'subject': Faculty.objects.filter(manager=user, filled_quota__gt=0).first(),
            'subjects': Faculty.objects.filter(manager=user, filled_quota__gt=0)[1:],
            'abis': Alumni.objects.filter(tour=tours[0], faculty__manager=user)
        }
        return render_to_response('all_tables.html', context)
    else:
        args = {
            'tours': Tour.objects.all(),
        }
        return render_to_response('not_found.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def add(request):
    c = {}
    c.update(csrf(request))
    c['lessons'] = Faculty.objects.filter(manager=request.user, filled_quota__gt=0)
    c['lgotniki'] = Lgotnik.objects.all()
    return render(request, 'add.html', c)


def add_abiturient(request):
    phone = request.POST.get('phone')
    code = request.POST.get('code')
    now = datetime.datetime.now()
    tour = Tour.objects.filter(initial__lte=now, final__gte=now)[0]
    f = 0
    if code[28] == "K":
        return render_to_response("error.html")
    elif code[28] == 1 and tour.name == '1 тур':
        f = 1
    elif code[28] == 2 and tour.name == '2 тур':
        f = 1
    else:
        f = 1
    if f == 0:
        return render_to_response("error.html")

    department_id = request.POST.get('department')
    # atestat = request.POST.get('a')
    lgotnik = request.POST.get('lgotnik')
    olimpiadnik = request.POST.get('o')
    abi = Alumni.objects.create()
    if lgotnik != "no":
        l = Lgotnik.objects.get(id=lgotnik)
        abi.lgotnik = l

    abi.phone = phone
    abi.tour = tour
    abi.barcode = code
    if olimpiadnik is not None:
        abi.olimpiadnik = True
    abi.ortId = code[0:6]
    faculty = Faculty.objects.get(id=department_id)
    abi.faculty = faculty
    if Alumni.objects.filter(faculty=faculty, tour=tour, ortId=code[0:6]).count() > 0:
        return render_to_response("error1.html")
    place = code[27]
    if place == 'R':
        abi.place = 'Шаар'
    elif place == 'B':
        abi.place = 'Борбор'
    elif place == 'Y':
        abi.place = 'Айыл'
    else:
        abi.place = 'Тоо'
    abi.save()
    extra = 0
    mini = 0
    main = 0
    for i in Lesson.objects.all():
        alumnilesson = AlumniLesson.objects.create()
        alumnilesson.alumni = abi
        alumnilesson.lesson = i
        if i.name == u'Основной':
            main = int(code[6:9])
            abi.main = main
        elif i.name == u'Биология':
            main = int(code[9:12])
        elif i.name == u'История':
            main = int(code[12:15])
        elif i.name == u'Химия':
            main = int(code[15:18])
        elif i.name == u'Физика':
            main = int(code[18:21])
        elif i.name == u'Английский язык':
            main = int(code[21:24])
        elif i.name == u'Математика':
            main = int(code[24:27])
            alumnilesson.grade = main
        if i in faculty.lessons.all() and i.name != u'Основной':
            if main > mini:
                extra = main
                mini = extra
        if main > 0:
            alumnilesson.grade = main
            alumnilesson.save()
    abi.extra_num = extra
    abi.summa = abi.main + extra
    # if atestat is not None:
    #     abi.atestat = True
    #     abi.summa += 20
    abi.save()
    return redirect('/tour/')


@login_required
def delete(request, p1):
    alumni = Alumni.objects.get(id=p1)
    alumni.delete()
    return redirect('/tour/')


def home(request):
    now = datetime.datetime.now()
    tours = Tour.objects.filter(initial__lte=now, final__gte=now)
    if tours.count() != 0:
        args = {
            'tours': Tour.objects.all(),
            'departments': Faculty.objects.filter(filled_quota__gt=0)
        }
        return render_to_response('home.html', args)
    else:
        args = {
            'tours': Tour.objects.all(),
        }
        return render_to_response('not_found.html', args)


def tour(request, p1):
    tour = Tour.objects.get(id=p1)
    user = request.user
    args = {
        'tours': Tour.objects.all(),
        'subject': Faculty.objects.filter(filled_quota__gt=0).first(),
        'subjects': Faculty.objects.filter(filled_quota__gt=0)[1:],
        'abis': Alumni.objects.filter(tour=tour, passed=True).order_by('place', '-summa'),
        'user': user
    }
    return render_to_response('tour.html', args)


def card(request, p1):
    t = Tour.objects.get(id=p1)
    user = request.user
    args = {
        't': t,
        'tours': Tour.objects.all(),
        'user': user
    }
    return render_to_response('card.html', args)


def rating(request, p1):
    tour = Tour.objects.get(id=p1)
    user = request.user
    args = {
        'tours': Tour.objects.all(),
        'subject': Faculty.objects.filter(filled_quota__gt=0).first(),
        'subjects': Faculty.objects.filter(filled_quota__gt=0)[1:],
        'abis': Alumni.objects.filter(tour=tour).order_by('place', '-summa'),
        'user': user
    }
    return render_to_response('rating.html', args)
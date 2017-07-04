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

from simpleapp.models import Faculty, Tour, Alumni, AlumniLesson, Lesson


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
            'subject': Faculty.objects.filter(manager=user).first(),
            'subjects': Faculty.objects.filter(manager=user)[1:],
            'abis': Alumni.objects.filter(tour=tours[0], faculty__manager=user)
        }
        return render_to_response('all_tables.html', context)
    else:
        return render_to_response('not_found.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def add(request):
    c = {}
    c.update(csrf(request))
    c['lessons'] = Faculty.objects.filter(manager=request.user)
    return render(request, 'add.html', c)


def add_abiturient(request):
    phone = request.POST.get('phone')
    code = request.POST.get('code')
    department_id = request.POST.get('department')
    atestat = request.POST.get('a')
    lgotnik = request.POST.get('l')
    olimpiadnik = request.POST.get('o')
    now = datetime.datetime.now()
    tour = Tour.objects.filter(initial__lte=now, final__gte=now)[0]
    abi = Alumni.objects.create()
    abi.phone = phone
    abi.tour = tour
    abi.barcode = code
    if atestat is not None:
        abi.atestat = True
    if lgotnik is not None:
        abi.lgotnik = True
    if olimpiadnik is not None:
        abi.olimpiadnik = True
    abi.ortId = code[0:6]
    faculty = Faculty.objects.get(id=department_id)
    abi.faculty = faculty
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
            'departments': Faculty.objects.all()
        }
        return render_to_response('home.html', args)
    else:
        return render_to_response('not_found.html')

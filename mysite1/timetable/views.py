from hashlib import md5
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader  
import psycopg2
from datetime import datetime
import os 

context = {}
def index(request):
    global context
    conn = psycopg2.connect(dbname='DefaultTimeTable', user=os.environ.get('PG_USER'), 
                        password=os.environ.get('PG_PASS'), host='localhost')
    cursor = conn.cursor()
    week = []
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    indexes = [0, 1, 2, 3, 4]
    for day in days:
        cursor.execute(f"SELECT * FROM {day}")
        week.append(cursor.fetchall())
    
    weekday = datetime.now().weekday()
    isChyselnyk = datetime.now().isocalendar()[1]%2 #returns 0 if chyselnyk, 1 if znamennyk 
    
    context.update( { 'week': week, 
                'weekday': weekday,
                'days': days,
                'indexes': indexes,
                'isChyselnyk': isChyselnyk,
                'session': request.session})
    return render(request, 'timetable/index.html', context)
def login(request):
    return render(request, 'timetable/login.html')
def send_login(request):
    username = request.POST['username']
    pass_md5 = md5(request.POST['password'].encode())
    conn = psycopg2.connect(dbname='Userdata', user='postgres', 
                        password='megawizard228', host='localhost')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE login='{username}'")
    user = cursor.fetchone()
    if user is None:
        return HttpResponse("User not found " + pass_md5.hexdigest())
    elif user[2] == pass_md5.hexdigest():
        request.session['username'] = username
        request.session['user_id'] = user[0]
        return HttpResponse("Login successful " + str(request.session['user_id']))
    #return HttpResponse(f"Username: {request.session['username']} Password: {request.session['password']}")
# Create your views here.

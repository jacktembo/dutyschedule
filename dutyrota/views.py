from django.http import HttpResponse
from django.shortcuts import render, Http404, HttpResponseRedirect
from datetime import datetime

def index(request):
    current_date_time = datetime.now()
    current_hour = current_date_time.hour
    if current_hour < 12:
        message = "Good Morning"
    elif current_hour >= 12 and current_hour < 18:
        message = "Good Afternoon"
    elif current_hour >= 18:
        message = "Good Evening"
    else:
        message = "Hello,"
    context = {"message": message}
    return render(request, 'dutyrota/index.html', context)





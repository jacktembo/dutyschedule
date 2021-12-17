from django.shortcuts import render, reverse, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from datetime import date, datetime, time, timedelta
import math
from .models import DutyRota, Announcement
from django.contrib.auth.decorators import login_required


today = datetime.today()
current_year = today.year
tomorrow = today + timedelta(days=1, minutes=1)  # Tomorrows's date
opening_date = datetime(2021, 11, 23)
week = timedelta(days=7)
days_passed = today - opening_date
result = days_passed / week

if type(result == float):
    week_number = math.ceil(result)
else:
    week_number = result

tomorrow_days_passed = tomorrow - opening_date
tomorrow_result = tomorrow_days_passed / week

if type(tomorrow_result == float):
    tomorrow_week_number = math.ceil(tomorrow_result)
elif type(tomorrow_result == int):
    tomorrow_week_number = tomorrow_result


@login_required
def index(request):
    context = {}
    return render(request, 'routine/dashboard.html', context)


@login_required
def today_rota(request):
    # Duty rota that has today's date
    today_duty_rota = get_object_or_404(
        DutyRota, week_number__week_number=week_number)
    teachers_on_duty = today_duty_rota.teachers.all()
    supervisors_on_duty = today_duty_rota.supervisors.all()
    tomorrow_duty_rota = get_object_or_404(
        DutyRota, week_number__week_number=tomorrow_week_number)
    teachers_on_duty_tomorrow = tomorrow_duty_rota.teachers.all()
    supervisors_on_duty_tomorrow = tomorrow_duty_rota.supervisors.all()
    context = {
        'tomorrow_rota': tomorrow_duty_rota, 'tomorrow_teachers': teachers_on_duty_tomorrow,
        'tomorrow_supervisors': supervisors_on_duty_tomorrow,
        'rota': today_duty_rota, 'teachers': teachers_on_duty,
        'supervisors': supervisors_on_duty,
    }
    return render(request, 'routine/today_rota.html', context)


@login_required
def annoucements(request):
    # Announcements to either pupils or staff
    announcements = Announcement.objects.order_by('-published_date_time')[:25]
    context = {
        'announcements': announcements
    }
    return render(request, 'routine/announcements.html', context)


@login_required
def announcement_detail(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    context = {
        'announcement': announcement
    }
    return render(request, 'routine/announcement_detail.html', context)


@login_required
def leave_permission(request):
    return HttpResponse('Hello LeavePermission')


def check_who(request):
    """This view checks who will be on duty on a selected date"""
    if request.method != 'POST':
        return render(request, 'check_who.html')
    else:
        selected_date = datetime.fromisoformat(request.POST['date'])
        duty_rota = get_object_or_404(DutyRota, date=selected_date)
        teachers_on_duty = duty_rota.teachers.all()
        supervisors_on_duty = duty_rota.supervisors.all()
        context = {
            'date': selected_date, 'rota': duty_rota,
            'teachers': teachers_on_duty,
            'supervisors': supervisors_on_duty
        }

        return render(request, 'check_who_results.html', context)



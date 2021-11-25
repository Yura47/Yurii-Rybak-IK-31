from django.shortcuts import render
from django.http import JsonResponse
import os
from datetime import datetime

def main(request):
    return render(request, 'main.html', {'parameter': "test"})

def health(request):
    response = {
    'date': datetime.now().strftime("Time: %H:%M:%S   Data: %Y/%M/%D"),
    'current_page': request.get_host() + request.get_full_path(),
    'server_info': "Name_OS: " + os.uname().sysname + ";   " +
                   "Name_Node: " + os.uname().nodename + ";   " +
                   "Release: " + os.uname().release + ";   " +
                   "Version: " + os.uname().version + ";   " +
                   "Indentificator:" + os.uname().machine,
    'client_info': "Browser: " + request.META['HTTP_USER_AGENT'] + ";   " + "IP: " + request.META['REMOTE_ADDR']
    }
    return JsonResponse(response)


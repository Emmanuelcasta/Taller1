from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # return HttpResponse("Welcome to the Movie Reviews Home Page") 
    #return render(request, 'home.html') 
    return render(request, 'home.html', {'name': 'Emmanuel Castañeda Cano'})

def about(request):
    return render(request, 'about.html')


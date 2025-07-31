from django.shortcuts import render
from .models import Movie

def home(request):
    # return HttpResponse("Welcome to the Movie Reviews Home Page") 
    #return render(request, 'home.html') 
    # return render(request, 'home.html', {'name': 'Emmanuel Castañeda Cano'})
    searchTerm = request.GET.get('searchMovie')
    
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    
    return render(request, 'home.html', {
        'name': 'Emmanuel Castañeda Cano',
        'searchTerm': searchTerm,
        'movies': movies
    })

def about(request):
    return render(request, 'about.html')

from urllib import request
from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt 
import matplotlib 
import io 
import urllib, base64 

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

def statistics_view(request): 
    matplotlib.use('Agg') 
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')  # Obtener todos los años de 
    movie_counts_by_year = {}  # Crear un diccionario para almacenar la cantidad de películas por año  
    for year in years: # Contar la cantidad de películas por año 
        if year: 
            movies_in_year = Movie.objects.filter(year=year) 
        else: 
            movies_in_year = Movie.objects.filter(year__isnull=True) 
        year_label = year if year else "None"
        count = movies_in_year.count() 
        movie_counts_by_year[year_label] = count 

    bar_width = 0.5 # Ancho de las barras 
    bar_spacing = 0.5 # Separación entre las barras  
    bar_positions = range(len(movie_counts_by_year)) # Posiciones de las barras  

    # Crear la gráfica de barras 
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center') 
    # Personalizar la gráfica 
    plt.title('Movies per year') 
    plt.xlabel('Year') 
    plt.ylabel('Number of movies') 
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90) 
    # Ajustar el espaciado entre las barras 
    plt.subplots_adjust(bottom=0.3) 
    # Guardar la gráfica en un objeto BytesIO 

# Vista para la suscripción
def signup(request):
    email = request.GET.get('email', '')
    return render(request, 'signup.html', {'email': email})
    buffer = io.BytesIO() 
    plt.savefig(buffer, format='png') 
    buffer.seek(0) 
    plt.close() 
     
    # Convertir la gráfica a base64 
    image_png = buffer.getvalue() 
    buffer.close() 
    graphic = base64.b64encode(image_png) 
    graphic = graphic.decode('utf-8') 
 
    # Renderizar la plantilla statistics.html con la gráfica 
    return render(request, 'statistics.html', {'graphic': graphic})
import matplotlib
import io
import urllib, base64

def genre_chart(request):
    matplotlib.use('Agg')
    # Get all movies and their first genre
    movies = Movie.objects.all()
    genre_counts = {}
    for movie in movies:
        first_genre = movie.genre.split(',')[0].strip() if movie.genre else 'Sin género'
        genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    genres = list(genre_counts.keys())
    counts = list(genre_counts.values())

    plt.figure(figsize=(8,5))
    plt.bar(genres, counts, color='skyblue')
    plt.xlabel('Género')
    plt.ylabel('Cantidad de películas')
    plt.title('Cantidad de películas por género (primer género)')
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()

    return render(request, 'genre_chart.html', {'chart': image_base64})

from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json
import csv

class Command(BaseCommand):
    help = 'Convert movies_initial.csv to movies.json and load movies into the Movie model'

    def handle(self, *args, **kwargs):
        import csv
        csv_file_path = 'movies_initial.csv'
        json_file_path = 'movie/management/commands/movies.json'

        # Convert CSV to JSON
        movies = []
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                movies.append(row)

        with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(movies, jsonfile, ensure_ascii=False, indent=4)

        # Load data from the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)

        # Add products to the database
        for movie in movies:
            exist = Movie.objects.filter(title=movie.get('title')).first()
            if not exist:
                try:
                    Movie.objects.create(
                        title=movie.get('title', ''),
                        image='movie/images/default.jpg',
                        genre=movie.get('genre', ''),
                        year=movie.get('year', ''),
                        description=movie.get('plot', '')
                    )
                except Exception as e:
                    print(f"Error creating movie: {e}")
            else:
                try:
                    exist.title = movie.get('title', '')
                    exist.image = 'movie/images/default.jpg'
                    exist.genre = movie.get('genre', '')
                    exist.year = movie.get('year', '')
                    exist.description = movie.get('plot', '')
                    exist.save()
                except Exception as e:
                    print(f"Error updating movie: {e}")
        #self.stdout.write(self.style.SUCCESS(f'Successfully added {cont} products to the database'))
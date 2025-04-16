from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Director, Actor, Genre, Movie, MovieActor, Rating
import datetime

# Create your tests here.
class MovieModelTest(TestCase):
    """Test cases for the Movie model"""
    
    def setUp(self):
        """Set up test data"""
        # Create director
        self.director = Director.objects.create(
            name="Christopher Nolan",
            birth_date=datetime.date(1970, 7, 30)
        )
        
        # Create genres
        self.genre1 = Genre.objects.create(name="Sci-Fi")
        self.genre2 = Genre.objects.create(name="Thriller")
        
        # Create movie
        self.movie = Movie.objects.create(
            title="Inception",
            release_date=datetime.date(2010, 7, 16),
            director=self.director,
            runtime=148,
            plot="A thief who steals corporate secrets through the use of dream-sharing technology."
        )
        self.movie.genres.add(self.genre1, self.genre2)
        
        # Create actor
        self.actor = Actor.objects.create(
            name="Leonardo DiCaprio",
            birth_date=datetime.date(1974, 11, 11)
        )
        
        # Create movie-actor relationship
        self.movie_actor = MovieActor.objects.create(
            movie=self.movie,
            actor=self.actor,
            character_name="Dom Cobb",
            is_lead=True
        )
    
    def test_movie_creation(self):
        """Test movie creation and relationships"""
        self.assertEqual(self.movie.title, "Inception")
        self.assertEqual(self.movie.director.name, "Christopher Nolan")
        self.assertEqual(self.movie.genres.count(), 2)
        self.assertTrue(self.genre1 in self.movie.genres.all())
        self.assertTrue(self.genre2 in self.movie.genres.all())
        self.assertEqual(self.movie.runtime, 148)
    
    def test_actor_relationship(self):
        """Test movie-actor relationship"""
        self.assertEqual(self.movie.actors.count(), 1)
        self.assertEqual(self.movie.actors.first().name, "Leonardo DiCaprio")
        self.assertEqual(self.movie_actor.character_name, "Dom Cobb")
        self.assertTrue(self.movie_actor.is_lead)


class RatingTest(TestCase):
    """Test cases for the Rating model"""
    
    def setUp(self):
        """Set up test data"""
        # Create movie
        self.movie = Movie.objects.create(
            title="The Shawshank Redemption",
            release_date=datetime.date(1994, 9, 23),
            runtime=142
        )
        
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")
        self.user3 = User.objects.create_user(username="user3", password="testpass123")
        
        # Create ratings
        self.rating1 = Rating.objects.create(movie=self.movie, user=self.user1, value=9)
        self.rating2 = Rating.objects.create(movie=self.movie, user=self.user2, value=10)
    
    def test_average_rating_calculation(self):
        """Test automatic average rating calculation"""
        # Check initial average rating with 2 ratings
        self.assertEqual(float(self.movie.avg_rating), 9.5)
        
        # Add a new rating
        Rating.objects.create(movie=self.movie, user=self.user3, value=8)
        self.movie.refresh_from_db()
        
        # Check updated average rating with 3 ratings
        self.assertEqual(float(self.movie.avg_rating), 9.0)


class AdminAccessTest(TestCase):
    """Test cases for admin access"""
    
    def setUp(self):
        """Create admin user"""
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.client.login(username='admin', password='adminpassword')
    
    def test_admin_access(self):
        """Test admin site accessibility"""
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_model_admin_access(self):
        """Test access to model admin pages"""
        models = ['director', 'actor', 'genre', 'movie', 'movieactor', 'userprofile', 'rating']
        
        for model in models:
            response = self.client.get(reverse(f'admin:movies_{model}_changelist'))
            self.assertEqual(response.status_code, 200)

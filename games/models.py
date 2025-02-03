from django.db import models
from django.contrib.auth.models import User

# Category Model: Represents the game category (e.g., Action, Puzzle, etc.)
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique category names
    slug = models.SlugField(unique=True, help_text="Unique identifier for the category (used in URLs).")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"  # Display "Categories" instead of "Categorys" in the admin panel


# Game Model: Represents an individual game
class Game(models.Model):
    title = models.CharField(max_length=200, unique=True, help_text="Title of the game.")  # Enforce unique titles
    description = models.TextField(help_text="A brief description of the game.")
    thumbnail_url = models.URLField(help_text="URL of the game's thumbnail image.")
    embed_code = models.TextField(help_text="Embed code for the game iframe (e.g., CrazyGames).")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='games', help_text="Category of the game.")
    rating = models.FloatField(default=0.0, help_text="Average user rating (out of 5).")
    total_reviews = models.PositiveIntegerField(default=0, help_text="Total number of reviews for the game.")

    def __str__(self):
        return self.title

    def update_rating(self):
        """
        Updates the game's rating based on associated reviews.
        """
        reviews = self.reviews.all()  # Access all related reviews
        if reviews.exists():
            self.rating = sum(review.rating for review in reviews) / reviews.count()
            self.total_reviews = reviews.count()
            self.save()

    class Meta:
        ordering = ['title']  # Order games alphabetically by title


# Review Model: Represents a review for a specific game by a user
class Review(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews', help_text="Game being reviewed.")
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="User who submitted the review.")
    rating = models.PositiveIntegerField(help_text="Rating for the game (e.g., 1-5 stars).")  # Limit to 1-5
    comment = models.TextField(help_text="User's comment for the game.")

    def __str__(self):
        return f"Review by {self.user.username} for {self.game.title}"

    class Meta:
        unique_together = ('game', 'user')  # Ensure a user can only review a game once
        ordering = ['-id']  # Show newest reviews first

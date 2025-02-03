from django.shortcuts import render, get_object_or_404
from .models import Category, Game

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

def game_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    games = category.games.all()
    return render(request, 'game_list.html', {'category': category, 'games': games})


def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'game_detail.html', {'game': game})

def play_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'play_game.html', {'game': game})
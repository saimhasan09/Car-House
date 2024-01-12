from django.shortcuts import render
from posts.models import Post
from categories.models import Category

def home(request, category_slug=None):
    categories = Category.objects.all()

    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        data = Post.objects.filter(category=category)
    else:
        data = Post.objects.all()

    return render(request, "home.html", {"data": data, "category": categories})

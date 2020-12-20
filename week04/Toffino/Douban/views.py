from django.shortcuts import render
from .models import Review

# Create your views here.

def movie_review(request):
    # 所有的评论
    reviews = Review.objects.all()
    # 评论数量
    counter = Review.objects.all().count()

    # 评分大于3分的评论
    return render(request, 'index.html', locals())

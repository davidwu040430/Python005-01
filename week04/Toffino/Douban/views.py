from django.shortcuts import render
from .models import Review

# Create your views here.

def movie_review(request):
    query = request.GET.get('q')
    if not query:
        # 所有的评论
        reviews_all = Review.objects.all()
        # 评分大于3分的评论
        condition = {'rate__gte': 3.0}
        reviews = reviews_all.filter(**condition)
        count = reviews.count()
    else:
        reviews = Review.objects.filter(content__icontains=query)
        count = reviews.count()

    return render(request, 'index.html', locals())

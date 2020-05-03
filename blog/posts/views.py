from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, PostView
from marketing.models import Signup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Q
from .forms import CommentForm



def search(request):
    query_set = Post.objects.all()
    query = request.GET.get('q')
    if query:
        query_set = query_set.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

        context = {
            'queryset': query_set
        }
        return render(request, 'search_results.html', context)

def get_category_count():
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def index(request):
    featured = Post.objects.filter(featured=True)
    latest_posts = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        su = Signup()
        su.email = email
        su.save()

    context = {
        'posts_list': featured,
        'latest_posts': latest_posts,
    }

    return render(request, 'index.html', context)

def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'post_list': paginated_queryset,
        'most_recent': most_recent,
        'category_count': category_count,
        'page_request_var': page_request_var
    }
    return render(request, 'blog.html', context)

def post(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form,
    }

    return render(request, 'post.html', context)

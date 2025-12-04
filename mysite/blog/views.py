from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404
from .models import Post


def post_list(request):
    post_list = Post.Published.all()
    # Show 3 contacts per page.
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get("page")
    try:
        posts = paginator.get_page(page_number)
    # Raises if the number cannot be converted to an integer
    except PageNotAnInteger:
        posts = paginator.get_page(1)
    # Raises EmptyPage if the given page number doesn’t exist
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})

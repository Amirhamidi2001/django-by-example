from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.list import ListView
from django.core.mail import send_mail

from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    """Display list of published posts."""

    queryset = Post.Published.all()
    context_object_name = "posts"
    template_name = "blog/post/list.html"
    paginate_by = 3


def post_list(request):
    post_list = Post.Published.all()
    # Show 3 contacts per page.
    paginator = Paginator(post_list, 3)
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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = (
                f"{cd['name']} ({cd['email']})" f"recommends reading '{post.title}'"
            )
            message = (
                f"Read '{post.title}' at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )

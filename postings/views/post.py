from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone

from postings.forms.PostForm import PostForm

from postings.models import Post


@login_required(login_url="/webauthn/login")
def create_post(request):
    qs = (
        Post.objects.select_related("author")
        .filter(status=Post.PostStatus.OPEN, deadline__gt=timezone.now())
        .order_by("-created_at")
    )
    paginator = Paginator(qs, 10)
    page_num = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, "posts/index.html", {"page_obj": page_obj})


@login_required(login_url="/webauthn/login")
def post_detail(request, uuid):

    post = get_object_or_404(
        Post,
        uuid=uuid,
        status=Post.PostStatus.OPEN,
        deadline__gt=timezone.now(),
    )
    return render(request, "posts/post_detail.html", {"post": post})


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone

from postings.models import Post

@login_required(login_url='/webauthn/login')
def post_list(request):
    qs = (
        Post.objects.select_related("author")
        .filter(
            status=Post.PostStatus.OPEN,
            deadline__gt=timezone.now(),
        )
        .order_by("-created_at")
    )

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "posts/index.html", {"page_obj": page_obj})
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from postings.models import Post, PostApplication
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from postings.forms.PostForm import ApplicationForm, PostForm
import uuid


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

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def _auto_expire(post: Post) -> None:
    """If the deadline has passed, flip status → EXPIRED."""
    if (
        post.deadline
        and post.deadline <= timezone.now()
        and post.status in (Post.PostStatus.OPEN, Post.PostStatus.LOCKED)
    ):
        post.status = Post.PostStatus.EXPIRED
        post.save(update_fields=["status"])


# --------------------------------------------------------------------------- #
# Views
# --------------------------------------------------------------------------- #

@login_required(login_url="/webauthn/login")
def post_detail(request, uuid: uuid.UUID):
    """Single‑post detail page with full role/ state matrix logic."""

    post: Post = get_object_or_404(Post, uuid=uuid)
    _auto_expire(post)  # deadline‑driven transition

    is_author = request.user == post.author

    # ------------------------------------------------------------------ #
    # Role‑specific querysets
    # ------------------------------------------------------------------ #
    user_application = None
    approved_qs = pending_qs = None

    if is_author:
        pending_qs = post.applications.filter(
            status=PostApplication.ApplicationStatus.PENDING
        ).order_by("-created_at")
        approved_qs = post.applications.filter(
            status=PostApplication.ApplicationStatus.APPROVED
        ).order_by("created_at")
    else:
        user_application = PostApplication.objects.filter(
            post=post, applicant=request.user
        ).first()

    # ------------------------------------------------------------------ #
    # Handle POST actions
    # ------------------------------------------------------------------ #
    if request.method == "POST":
        action = request.POST.get("action")

        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        # 1. Apply
        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        if action == "apply" and not is_author and post.status == Post.PostStatus.OPEN:
            form = ApplicationForm(request.POST)
            if form.is_valid() and not user_application:
                app = form.save(commit=False)
                app.post = post
                app.applicant = request.user
                app.save()
                messages.success(request, "Your application has been submitted.")
            else:
                messages.warning(request, "You have already applied to this post.")
            return redirect("postings:post_detail", uuid=post.uuid)

        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        # 2. Withdraw (pending only)
        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        elif action == "withdraw_application" and user_application:
            if user_application.status == PostApplication.ApplicationStatus.PENDING:
                user_application.delete()
                messages.success(request, "Your application has been withdrawn.")
            else:
                messages.warning(request, "Processed applications cannot be withdrawn.")
            return redirect("postings:post_detail", uuid=post.uuid)

        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        # 3. Approve (author only)
        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        elif action == "approve_application" and is_author:
            aid = request.POST.get("application_id")
            target = get_object_or_404(PostApplication, id=aid, post=post)
            if not post.is_full():
                target.status = PostApplication.ApplicationStatus.APPROVED
                target.save()
                messages.success(request, f"{target.applicant.username} approved.")
            else:
                messages.error(request, "Task is full – cannot approve more applicants.")
            return redirect("postings:post_detail", uuid=post.uuid)

        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        # 4. Lock / Re‑open (author only)
        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        elif action == "toggle_lock" and is_author:
            if post.status == Post.PostStatus.OPEN:
                post.status = Post.PostStatus.LOCKED
                post.save(update_fields=["status"])
                messages.success(request, "Post locked – no further applications.")
            elif post.status == Post.PostStatus.LOCKED:
                if post.is_full():
                    messages.warning(request, "Cannot reopen – task already full.")
                else:
                    post.status = Post.PostStatus.OPEN
                    post.save(update_fields=["status"])
                    messages.success(request, "Post reopened for applications.")
            else:
                messages.error(request, "This status cannot be toggled.")
            return redirect("postings:post_detail", uuid=post.uuid)

        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        # 5. Mark completed (author only)
        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        elif action == "mark_completed" and is_author and post.status != Post.PostStatus.COMPLETED:
            post.status = Post.PostStatus.COMPLETED
            post.save(update_fields=["status"])
            messages.success(request, "Task marked as completed.")
            return redirect("postings:post_detail", uuid=post.uuid)

        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        # 6. Re‑open EXPIRED (author only)
        # ――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
        elif action == "reopen_post" and is_author and post.status == Post.PostStatus.EXPIRED:
            post.status = Post.PostStatus.OPEN
            post.save(update_fields=["status"])
            messages.success(request, "Post reopened – remember to extend the deadline!")
            return redirect("postings:post_detail", uuid=post.uuid)

    # ------------------------------------------------------------------ #
    # Render
    # ------------------------------------------------------------------ #
    application_form = ApplicationForm()

    context = {
        "post": post,
        "is_author": is_author,
        "user_application": user_application,
        "pending_applications": pending_qs,
        "approved_applications": approved_qs,
        "application_form": application_form,
        "is_open_for_application": (
            post.status == Post.PostStatus.OPEN
            and (post.deadline is None or post.deadline > timezone.now())
        ),
    }
    return render(request, "posts/post_detail.html", context)


@login_required(login_url="/webauthn/login")
def post_update(request, uuid):
    post = get_object_or_404(Post, uuid=uuid)
    if post.author != request.user:
        raise PermissionDenied("You do not have permission to edit this post.")
    messages.info(request, "Edit functionality is not yet implemented.")
    return redirect('postings:post_detail', uuid=post.uuid)


@login_required(login_url="/webauthn/login")
def post_delete(request, uuid):
    post = get_object_or_404(Post, uuid=uuid)
    if post.author != request.user:
        raise PermissionDenied("You do not have permission to delete this post.")

    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f"The post '{post_title}' has been deleted successfully.")
        return redirect('postings:index')

    return redirect('postings:post_detail', uuid=post.uuid)

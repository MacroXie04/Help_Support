from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from postings.models import Post, PostApplication
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from postings.forms.PostForm import ApplicationForm, PostForm


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
    post = get_object_or_404(Post, uuid=uuid)
    is_author = (request.user == post.author)

    user_application = None
    pending_applications = None
    approved_applications = None

    if is_author:
        pending_applications = post.applications.filter(status=PostApplication.ApplicationStatus.PENDING).order_by('-created_at')
        approved_applications = post.applications.filter(status=PostApplication.ApplicationStatus.APPROVED).order_by('created_at')
    else:
        user_application = PostApplication.objects.filter(post=post, applicant=request.user).first()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'apply' and not is_author and post.status == Post.PostStatus.OPEN:
            form = ApplicationForm(request.POST)
            if form.is_valid() and not user_application:
                application = form.save(commit=False)
                application.post = post
                application.applicant = request.user
                application.save()
                messages.success(request, 'Your application has been submitted successfully.')
            else:
                messages.warning(request, 'You have already applied to this post.')
            return redirect('postings:post_detail', uuid=post.uuid)

        elif action == 'approve_application' and is_author:
            application_id = request.POST.get('application_id')
            application_to_approve = get_object_or_404(PostApplication, id=application_id, post=post)
            if not post.is_full():
                application_to_approve.status = PostApplication.ApplicationStatus.APPROVED
                application_to_approve.save()
                messages.success(request, f'{application_to_approve.applicant.username} has been approved.')
            else:
                messages.error(request, 'The task is full. No more applications can be approved.')
            return redirect('postings:post_detail', uuid=post.uuid)

        elif action == 'withdraw_application' and user_application:
            if user_application.status == PostApplication.ApplicationStatus.PENDING:
                user_application.delete()
                messages.success(request, 'Your application has been withdrawn.')
            else:
                messages.warning(request, 'Your application has already been processed and cannot be withdrawn.')
            return redirect('postings:post_detail', uuid=post.uuid)

        elif action == 'toggle_lock' and is_author:
            if post.status == Post.PostStatus.OPEN:
                post.status = Post.PostStatus.LOCKED
                post.save(update_fields=['status'])
                messages.success(request, 'The post has been locked. No more applications will be accepted.')
            elif post.status == Post.PostStatus.LOCKED:
                if post.is_full():
                    messages.warning(request, 'Cannot reopen the post because the task is already full.')
                else:
                    post.status = Post.PostStatus.OPEN
                    post.save(update_fields=['status'])
                    messages.success(request, 'The post has been reopened for applications.')
            else:
                messages.error(request, f'The post status "{post.get_status_display()}" cannot be changed.')
            return redirect('postings:post_detail', uuid=post.uuid)

    application_form = ApplicationForm()
    context = {
        'post': post,
        'is_author': is_author,
        'user_application': user_application,
        'pending_applications': pending_applications,
        'approved_applications': approved_applications,
        'application_form': application_form,
        'is_open_for_application': (
            post.status == Post.PostStatus.OPEN and
            (post.deadline is None or post.deadline > timezone.now())
        )
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

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from postings.models import Post, PostApplication
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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
    user_application = PostApplication.objects.filter(post=post,
                                                      applicant=request.user).first() if not is_author else None

    # Author sees all applications; others see none
    applications = post.applications.all().order_by('-created_at') if is_author else None

    if request.method == 'POST':
        action = request.POST.get('action')

        # Action: A user applies to the post
        if action == 'apply' and not is_author and post.status == Post.PostStatus.OPEN:
            form = ApplicationForm(request.POST)
            if form.is_valid() and not user_application:
                application = form.save(commit=False)
                application.post = post
                application.applicant = request.user
                application.save()
                messages.success(request, '你的申请已成功提交！')
            else:
                messages.warning(request, '你已经申请过这个任务了。')
            return redirect('post_detail', uuid=post.uuid)

        # Action: The author approves an application
        elif action == 'approve_application' and is_author:
            application_id = request.POST.get('application_id')
            application_to_approve = get_object_or_404(PostApplication, id=application_id, post=post)
            if not post.is_full():
                application_to_approve.status = PostApplication.ApplicationStatus.APPROVED
                application_to_approve.save()
                messages.success(request, f'已批准 {application_to_approve.applicant.username} 的申请。')
            else:
                messages.error(request, '任务人数已满，无法批准更多申请。')
            return redirect('post_detail', uuid=post.uuid)

        # Action: A user withdraws their own application
        elif action == 'withdraw_application' and user_application:
            if user_application.status == PostApplication.ApplicationStatus.PENDING:
                user_application.delete()
                messages.success(request, '你的申请已成功撤回。')
            else:
                messages.warning(request, '你的申请已被处理，无法撤回。')
            return redirect('post_detail', uuid=post.uuid)

    # For GET requests, prepare the context
    application_form = ApplicationForm()
    context = {
        'post': post,
        'is_author': is_author,
        'user_application': user_application,
        'applications': applications,
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
        raise PermissionDenied("你没有权限编辑这个帖子。")
    # You should build a proper form and template for editing
    # For now, this is a placeholder
    messages.info(request, "编辑功能尚未实现。")
    return redirect('post_detail', uuid=post.uuid)


@login_required(login_url="/webauthn/login")
def post_delete(request, uuid):
    post = get_object_or_404(Post, uuid=uuid)
    if post.author != request.user:
        raise PermissionDenied("你没有权限删除这个帖子。")

    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f"帖子 '{post_title}' 已成功删除。")
        # Redirect to a list page or homepage, assuming 'home' is its name
        return redirect('home')

        # You would normally render a confirmation page on GET
    # but the form in the template submits directly via POST
    return redirect('post_detail', uuid=post.uuid)

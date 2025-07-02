from django.contrib.auth.decorators import login_required

from django.shortcuts import (
    render,
    redirect,
)

from postings.forms.PostForm import PostForm


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", uuid=post.uuid)
    else:
        form = PostForm()

    return render(request, "posts/post_form.html", {"form": form})

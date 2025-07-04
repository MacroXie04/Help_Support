import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from postings.models import Post
from chat.models import ChatRoom, ChatMessage

@login_required(login_url="/webauthn/login")
def room(request, uuid: uuid.UUID):
    # 1. Fetch the post & chat room (create if missing)
    post = get_object_or_404(Post, uuid=uuid)
    room, _ = ChatRoom.objects.get_or_create(post=post)
    room.sync_participants()  # make sure membership is current

    # 2. Guard: only author or approved applicant may enter
    if request.user not in room.participants.all():
        return HttpResponseForbidden("You’re not a participant in this task’s chat.")

    # 3. Handle message submit
    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            ChatMessage.objects.create(room=room, sender=request.user, text=text)
        return redirect("chat:room", uuid=uuid)

    # 4. Render
    context = {
        "post": post,
        "room": room,
        "messages": room.messages.select_related("sender"),
    }
    return render(request, "chatroom.html", context)
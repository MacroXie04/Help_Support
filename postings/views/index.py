from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required(login_url='/login')
def index_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")
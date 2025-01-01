from django.shortcuts import render

def layout(request):
    return render(request, 'index_layout.html')
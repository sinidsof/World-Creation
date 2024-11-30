from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')
def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def gallery(request):
    return render(request, 'core/gallery.html')

def feedback(request):
    return render(request, 'core/feedback.html')



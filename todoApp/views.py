from django.shortcuts import redirect

def index(request):
    # Just redirect to the todos view from the main page
    return redirect('/todos')
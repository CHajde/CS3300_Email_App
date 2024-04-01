from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'emrem_app/index.html')


def create_reminder(request):
    return render(request, 'emrem_app/create_reminder.html')


def view_reminders(request):
    # Here you would typically get the reminders from the database.
    # For example, if you have a Reminder model you could do something like this:
    # reminders = Reminder.objects.filter(user=request.user)

    # But for now, we'll just pass an empty context or some dummy data
    context = {'reminders': []}  # Replace with actual data retrieval logic
    return render(request, 'emrem_app/view_reminders.html', context)


def login_view(request):
    # Placeholder view for login. Eventually, you'll use Django's auth views here.
    # return redirect('name_of_your_login_template')
    return render(request, 'emrem_app/login.html')


def logout_view(request):
    # Placeholder view for logout. Eventually, you'll use Django's auth views here.
    # Logout the user and redirect to home page for example
    # return redirect('index')
    return render(request, 'emrem_app/logout.html')
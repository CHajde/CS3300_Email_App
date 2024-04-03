from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Reminder
from .forms import ReminderForm

# Create your views here.
def index(request):
    return render(request, 'emrem_app/index.html')


def create_reminder(request):
    return render(request, 'emrem_app/create_reminder.html')


from django.shortcuts import render
from .models import Reminder

def view_reminders(request):
    reminders = Reminder.objects.all()  # This queries all reminders
    return render(request, 'emrem_app/view_reminders.html', {'reminders': reminders})



def login_view(request):
    # Placeholder view for login. Eventually, you'll use Django's auth views here.
    # return redirect('name_of_your_login_template')
    return render(request, 'emrem_app/login.html')


def logout_view(request):
    # Placeholder view for logout. Eventually, you'll use Django's auth views here.
    # Logout the user and redirect to home page for example
    # return redirect('index')
    return render(request, 'emrem_app/logout.html')


class ReminderDetailView(DetailView):
    model = Reminder
    template_name = 'emrem_app/reminder_detail.html'
    context_object_name = 'reminder'
    
    
def index(request):
    reminders = Reminder.objects.all()  # Later change to filter by user
    return render(request, 'emrem_app/index.html', {'reminders': reminders})


def edit_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            return redirect('view_reminders')
    else:
        form = ReminderForm(instance=reminder)
    return render(request, 'emrem_app/edit_reminder.html', {'form': form})


def delete_reminder(request, pk):
    reminder = get_object_or_404(Reminder, pk=pk)
    reminder.delete()
    return redirect('view_reminders')


def create_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_reminders')
    else:
        form = ReminderForm()
    return render(request, 'emrem_app/create_reminder.html', {'form': form})
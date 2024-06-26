from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Reminder
from .forms import ReminderForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        
        return render(request, 'emrem_app/index.html', {'reminders': None})
    
    sort = request.GET.get('sort', None)
    
    if sort == 'urgency':
        reminders = Reminder.objects.filter(user=request.user).order_by('-urgency')
    elif sort == 'date':
        reminders = Reminder.objects.filter(user=request.user).order_by('reminder_date')
    else:
        reminders = Reminder.objects.filter(user=request.user)

    return render(request, 'emrem_app/index.html', {'reminders': reminders})



@login_required
def create_reminder(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            print("Form is valid. User:", request.user)  # Debug print
            reminder.user = request.user
            reminder.save()
            print("Reminder saved with user_id:", reminder.user_id)  # Confirm user_id is set
            return redirect('view_reminders')
        else:
            print("Form errors:", form.errors)  # Print form errors
    else:
        form = ReminderForm()
    return render(request, 'emrem_app/create_reminder.html', {'form': form})




@login_required
def view_reminders(request):
    if request.user.is_authenticated:
        reminders = Reminder.objects.filter(user=request.user)
    else:
        reminders = []  # Or redirect to login page

    return render(request, 'emrem_app/view_reminders.html', {'reminders': reminders})



def login_view(request):
    return render(request, 'emrem_app/login.html')


def logout_view(request):
    return render(request, 'emrem_app/logout.html')


class ReminderDetailView(DetailView):
    model = Reminder
    template_name = 'emrem_app/reminder_detail.html'
    context_object_name = 'reminder'


@login_required
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


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})
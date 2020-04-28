from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from recipeSite.models import Post

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Sua conta foi criada!")
            return redirect('signin')
        else:
            messages.info(request, f"ERROR")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profileEdit(request):
    user = get_object_or_404(User, username=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': Profile.objects.get(user=user)
    }
    return render(request, 'users/profileEdit.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def discardPic(request):
    request.user.profile.defaultImage()
    return redirect('profile')
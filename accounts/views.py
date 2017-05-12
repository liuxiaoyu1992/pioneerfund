from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from home.models import Projects, Pledges
from .models import UserProfile
from .forms import UserLoginForm, UserRegisterForm, EditProfileForm, UserProfileForm
from django.views.generic import DetailView
from django.views import View
from django.urls import reverse
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q


User = get_user_model()
# Create your views here.
def index(request):
    return render(request, 'accounts/index.html')

def login_view(request):
    print(request.user.is_authenticated())
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/tohome")
    return render(request, "accounts/form.html", {"form": form, "title": title})

def register_view(request):
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/tohome")
    context = {"form": form, "title": title}
    return render(request, "accounts/form.html", context)

def log_out_view(request):
    logout(request)
    return render(request, "accounts/logout.html")


def edit_profile(request):
    title = 'Edit profile'
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('profiles:tohome'))
    else:
        form = EditProfileForm(instance=request.user)
        context = {"form": form, "title": title}
        return render(request, 'accounts/edit_profile.html', context)

def edit_personal_profile(request):
    title = 'Edit personal profile'
    user_profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST or None, request.FILES or None,instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect(reverse('profiles:tohome'))
    else:
        form = UserProfileForm(instance=user_profile)
        context = {"form": form, "title": title}
        return render(request, 'accounts/edit_profile.html', context)

def change_password(request):
    title = 'Change password'
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('profiles:tohome'))
        else:
            return redirect(reverse('profiles:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        context = {"form": form, "title": title}
        return render(request, 'accounts/change_password.html', context)


class UserDetailView(DetailView):
    template_name = 'accounts/user_detail.html'
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(
            User,
            username__iexact=self.kwargs.get("username")
        )

    # def get_projects(self):
    #     projects = Projects.objects.filter(uid__username=self.kwargs.get("username"))
    #     return projects


    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        following = UserProfile.objects.is_following(self.request.user, self.get_object())

        my_pledges = Pledges.objects.filter(uid__username=self.kwargs.get("username")).values()
        project_ids = set()
        if my_pledges:
            for pled in my_pledges:
                project_ids.add(pled['pid_id'])
                print("uid")
                print(pled['uid_id'])
            my_filter_qs = Q()
            for project_id in project_ids:
                my_filter_qs = my_filter_qs | Q(id=project_id)
            backed_projects = Projects.objects.filter(my_filter_qs)
        else:
            backed_projects = None

        context['following'] = following
        context['created_projects'] = Projects.objects.filter(uid__username=self.kwargs.get("username"))
        context['backed_projects'] = backed_projects
        context['profiles'] = UserProfile.objects.get(user__username=self.kwargs.get("username"))


        print(context)
        return context

class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated():
            is_following = UserProfile.objects.toggle_follow(request.user, toggle_user)
        return redirect("profiles:detail", username=username)
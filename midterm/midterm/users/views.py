from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View
from posts.models import UserPurchase, Post



# Create your views here.
def register(request):
    if request.method == "POST":
        author_form = forms.RegistrationForm(request.POST)
        if author_form.is_valid():
            author_form.save()
            messages.success(request, "Registered successfully")
            return redirect("user_login")
    else:
        author_form = forms.RegistrationForm()
    return render(request, "register.html", {"form": author_form, "type": "Register"})



# user login class based view
class UserLoginView(LoginView):
    template_name = "register.html"

    #
    def get_success_url(self):
        return reverse_lazy("profile")

    def form_valid(self, form):
        messages.success(self.request, "Login successful")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, "Invalid login information")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "login"
        return context


# profile page

@login_required
def profile(request):
    # Get the user's authored posts
    user_authored_posts = Post.objects.filter(author=request.user)

    # Get the user's purchase history
    user_purchases = UserPurchase.objects.filter(user=request.user)

    # Get the IDs of the posts the user has purchased
    purchased_post_ids = user_purchases.values_list('post_id', flat=True)

    # Filter the posts based on the purchased IDs
    purchased_posts = Post.objects.filter(id__in=purchased_post_ids)

    return render(request, "profile.html", {"user_authored_posts": user_authored_posts, "user_purchases": user_purchases, "purchased_posts": purchased_posts})



class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("user_login")

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from . import forms
from . import models
from django.contrib import messages
from django.shortcuts import redirect
from .models import UserPurchase, Post



# Create your views here.

# add post using class based view
@method_decorator(login_required, name="dispatch")
class AddPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = "add_post.html"
    success_url = reverse_lazy("add_post")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# update post class based view
@method_decorator(login_required, name="dispatch")
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = "add_post.html"
    pk_url_kwarg = "id"  # if we change the url parameter
    success_url = reverse_lazy("profile")



# delete post class based view
@method_decorator(login_required, name="dispatch")
class DeletePostView(DeleteView):
    model = models.Post
    template_name = "delete_post.html"
    success_url = reverse_lazy("profile")
    pk_url_kwarg = "id"


# detail post view
class DetailPostView(DetailView):
    model = models.Post
    pk_url_kwarg = "id"
    template_name = "post_details.html"

    # comment section
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # inherited
        post = self.object  # store the post model object
        comments = post.comments.all()
        comment_form = forms.CommentForm()
        context["comments"] = comments
        context["comment_form"] = comment_form
        return context



def buy_now(request, post_id):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        post = Post.objects.get(pk=post_id)

        # Check if there are available posts
        if post.available_posts > 0:
            # Decrement the count and save the post
            post.available_posts -= 1
            post.save()

            # Create a record in UserPurchase
            UserPurchase.objects.create(user=request.user, post=post)

            # Add a message for the user
            messages.success(request, f"You have successfully bought '{post.title}'!")

        else:
            # Add a message if no more posts are available
            messages.error(request, f"Sorry, '{post.title}' is out of stock.")

    return redirect('detail_post', id=post_id)

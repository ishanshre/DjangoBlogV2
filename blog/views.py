from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
)
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from .models import Post, Comment, Profile
from django.urls import reverse_lazy, reverse
from .forms import CommentForm, PostForm

# Create your views here.


class IndexListView(ListView):
    model = Post
    paginate_by = 6
    context_object_name = 'post_list'
    template_name = 'blog/index.html'

    def get_queryset(self):
        return self.model.published.all()


class TagPostListView(ListView):
    model = Post
    paginate_by = 8
    context_object_name = 'post_list'
    template_name = 'blog/tag_post_list_view.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['tags_slugs'] = self.kwargs['tag_slug']
        return context

    def get_queryset(self):
        return self.model.published.filter(tags__slug=self.kwargs['tag_slug'])


class GetComment(DetailView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def get_queryset(self):
        return Post.published.filter(publish__year=self.kwargs['year'], publish__month=self.kwargs['month'], publish__day=self.kwargs['day'], slug=self.kwargs['slug'])


class PostComment(SingleObjectMixin, LoginRequiredMixin, FormView):
    model = Post
    form_class = CommentForm
    context_object_name = 'posts'
    template_name = 'blog/post_detail.html'
    
    def get_queryset(self):
        return Post.published.filter(publish__year=self.kwargs['year'], publish__month=self.kwargs['month'], publish__day=self.kwargs['day'], slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()#from singleObjectMixin returns current posts year, month, day and slug
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        comment = form.save(commit=False)#store the comment from user temporary in comment variable 
        comment.post = self.object#Link this comment to current blog post
        comment.author = self.request.user#Link the logged in user as the comment author
        comment.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        posts = self.get_object()
        return reverse('blog:post_detail', kwargs={
            'year':posts.publish.year,
            'month':posts.publish.month,
            'day':posts.publish.day,
            'slug': posts.slug
        })


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        view = GetComment.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)



class SearchBlogView(ListView):
    model = Post
    context_object_name = 'post_list'
    paginate_by = 10
    template_name = 'blog/post_search.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.published.filter(
            Q(title__icontains=query)|Q(author__username = query)
        )


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    message = "Post Created Successfully"
    success_url = reverse_lazy('blog:index')

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form,*args,**kwargs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'
    message = "Update Successful"

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super(PostUpdateView, self).form_valid(form, *args, **kwargs)
    
    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('blog:index')
    message = "Post Deleted Successfully"

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    
    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        return super(PostDeleteView, self).form_valid(form,*args, **kwargs)
    
    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user


class CommentUpdateView(LoginRequiredMixin,UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'blog/comment_update.html'
    message = "Comment Edited"

    #alternative method to update comment using method overiding
    # def get_object(self):
    #     return Comment.objects.get(id=self.kwargs['comment_id'])

    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CommentUpdateView,self).form_valid(form)
    
    def test_func(self):
        self.object = self.get_object()
        return self.object == self.request.user


class CommentUpdateView(LoginRequiredMixin,UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    fields = ['comment']
    template_name = 'blog/comment_update.html'
    message = "Comment Edited"
    
    #alternative method to update comment using method overiding
    def get_object(self):
        return Comment.objects.get(id=self.kwargs['comment_id'])

    def get_queryset(self):
        return Post.published.filter(id=self.kwargs['comment_id'])


    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CommentUpdateView,self).form_valid(form)
    
    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user

    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('blog:post_detail', args=[self.object.post.publish.year, self.object.post.publish.month,self.object.post.publish.day, self.object.post.slug])


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'
    message = 'Comment Deleted'

    def get_object(self):
        return Comment.objects.get(id=self.kwargs['comment_id'])
    
    def get_success_message(self, cleaned_data):
        print(cleaned_data)
        return self.message
    
    def form_vald(self,form):
        form.instance.author = self.request.user
        return super(CommentDeleteView, self).form_valid(form)
    
    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user
    
    def get_success_url(self):
        self.object = self.get_object()
        return reverse_lazy('blog:post_detail', args=[self.object.post.publish.year, self.object.post.publish.month,self.object.post.publish.day, self.object.post.slug])


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'blog/profile.html'

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
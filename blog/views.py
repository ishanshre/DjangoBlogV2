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
from .models import Post
from django.urls import reverse_lazy, reverse
from .forms import CommentForm

# Create your views here.


class IndexListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'post_list'
    template_name = 'blog/index.html'

    def get_queryset(self):
        return self.model.published.all()


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
    fields = ['title','slug','body','status']
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
    fields = ['title','slug','body','status']
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
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
)
from .models import Post
# Create your views here.


class IndexListView(ListView):
    model = Post
    paginate_by = 10
    context_object_name = 'post_list'
    template_name = 'blog/index.html'

    def get_queryset(self):
        return self.model.published.all()


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post_detail.html'


    def get_queryset(self):
        #post = Post.published.get(publish__year=self.kwargs['year'], publish__month=self.kwargs['month'], publish__day=self.kwargs['day'], slug=self.kwargs['slug'])
        return Post.published.filter(publish__year=self.kwargs['year'], publish__month=self.kwargs['month'], publish__day=self.kwargs['day'], slug=self.kwargs['slug'])

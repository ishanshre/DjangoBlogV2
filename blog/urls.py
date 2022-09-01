from django.urls import path
from .views import IndexListView, PostDetailView, SearchBlogView, PostCreateView, PostUpdateView, PostDeleteView


app_name = 'blog'
urlpatterns = [
    path('', IndexListView.as_view(), name = 'index'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchBlogView.as_view(), name='post_search'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
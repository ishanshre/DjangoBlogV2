from django.urls import path
from .views import IndexListView, PostDetailView


app_name = 'blog'
urlpatterns = [
    path('', IndexListView.as_view(), name = 'index'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
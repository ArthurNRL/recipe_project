from . import views
from django.urls import path

urlpatterns = [
    path('', views.postListView.as_view(), name='recipeHome'),
    path('user/<str:username>', views.userListView.as_view(), name='userPosts'),
    path('post/<int:pk>/', views.postDetail.as_view(), name='postDetail'),
    path('post/<int:pk>/update', views.postUpdateView.as_view(), name='postUpdate'),
    path('post/<int:pk>/delete', views.postDeleteView.as_view(), name='postDelete'),
    path('post/new/', views.postCreateView.as_view(), name='postCreate'),
    path('favorites/', views.userFavoritesListView.as_view(), name='userFavorites'),
	path('about/', views.about, name='recipeAbout'),
]

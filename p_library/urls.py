from django.contrib import admin  
from django.urls import path, reverse_lazy 
from .views import AuthorEdit, AuthorList, authors_create_many, books_authors_create_many, FriendList, FriendFormEdit, books_friends_create, index
from allauth.account.views import login, logout
from .views import RegisterView, CreateUserProfile
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'p_library'  
urlpatterns = [  
	path('', index, name='index'), 
    path('author/create', AuthorEdit.as_view(), name='author_create'),  
    path('authors', AuthorList.as_view(), name='author_list'),
    path('author/create_many', authors_create_many, name='author_create_many'),
    path('author_book/create_many', books_authors_create_many, name='author_book_create_many'),
    path('friend/create', FriendFormEdit.as_view(), name='friend_create'),
    path('friends', FriendList.as_view(), name='friend_form'),
    path('book_friend/create', books_friends_create, name='book_friend_create'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('pub_house/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('friend_list/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(template_name='register.html', success_url=reverse_lazy('p_library:profile-create')), name='register'),
    path('profile-create/', CreateUserProfile.as_view(), name='profile-create'),
    ] 
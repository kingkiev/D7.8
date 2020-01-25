from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from p_library.models import Book, Publish, Author, Friend, UserProfile
from p_library.forms import AuthorForm, BookForm, FriendForm, BookFormForFriend, ProfileCreationForm
from django.views.generic import CreateView, ListView, FormView
from django.urls import reverse_lazy
from django.forms import formset_factory
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import auth
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import login, authenticate 
 

def index(request):
	context = {}
	template = loader.get_template('index.html')
	books = Book.objects.all()
	biblio_data = {
		"title": "мою библиотеку",
		"books": books,
		}
	if request.user.is_authenticated:
		biblio_data['username'] = request.user.username
	return HttpResponse(template.render(biblio_data, request))

class RegisterView(FormView):

	form_class = UserCreationForm

	def form_valid(self, form):
		form.save()
		username = form.cleaned_data.get('username')
		raw_password = form.cleaned_data.get('password1')
		login(self.request, authenticate(username=username, password=raw_password))
		return super(RegisterView, self).form_valid(form)

class CreateUserProfile(FormView):

	form_class = ProfileCreationForm
	template_name = 'profile-create.html'
	success_url = reverse_lazy('p_library:index')

	def dispath(self, request, *args, **kwargs):
		if self.request.user.is_anonymous:
			return HttpResponseRedirect(reverse_lazy('p_library:login'))
		return super(CreateUserProfile, self).dispath(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.user = self.request.user
		instance.save()	
		return super(CreateUserProfile, self).form_valid(form)


def book_increment(request):
	if request.method == 'POST':
		book_id = request.POST['id']
		if not book_id:
			return redirect('/index/')
		else:
			book = Book.objects.filter(id=book_id).first()
			if not book:
				return redirect('/index/')
			book.copy_count += 1
			book.save()
		return redirect('/index/')
	else:
		return redirect('/index/')

def book_decrement(request):
	if request.method == 'POST':
		book_id = request.POST['id']
		if not book_id:
			return redirect('/index/')
		else:
			book = Book.objects.filter(id=book_id).first()
			if not book:
				return redirect('/index/')
			if book.copy_count < 1:
				book.copy_count = 0
			else:
				book.copy_count -= 1
			book.save()
		return redirect('/index/')
	else:
		return redirect('/index/')

def pub_house(request):
	template = loader.get_template('pub_house.html')
	houses = Publish.objects.all()
	houses_data = {
		"title": "Книги по изданиям",
		"houses": houses,
		}
	return HttpResponse(template.render(houses_data, request))

class AuthorEdit(CreateView):
	model = Author
	form_class = AuthorForm
	success_url = reverse_lazy('p_library:authors_list')
	template_name = 'authors_edit.html'

class AuthorList(ListView):
	model = Author
	template_name = 'authors_list.html'

class FriendFormEdit(CreateView):
	model = Friend
	form_class = FriendForm
	success_url = reverse_lazy('p_library:friend_form')
	template_name = 'friend_form_edit.html'

class FriendList(ListView):
	model = Friend
	template_name = 'friend_form.html'

def authors_create_many(request):
	AuthorFormSet = formset_factory(AuthorForm, extra=2)
	if request.method == 'POST':
		author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
		if author_formset.is_valid() and book_formset.is_valid():
			for author_form in author_formset:
				author_form.save()
			return HttpResponseRedirect(reverse_lazy('p_library:authors_list'))
	else:
		author_formset = AuthorFormSet(prefix='authors')
	return render(request, 'manage_books_authors.html', {'author_formset': author_formset})

def books_authors_create_many(request):
	AuthorFormSet = formset_factory(AuthorForm, extra=2)
	BookFormSet = formset_factory(BookForm, extra=2)
	if request.method == 'POST':
		author_formset = AuthorFormSet(request.POST, request.FILES, prefix='authors')
		book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
		if author_formset.is_valid() and book_formset.is_valid():
			for author_form in author_formset:
				author_form.save()
			for book_form in book_formset:
				book_form.save()
			return HttpResponseRedirect(reverse_lazy('p_library:authors_list'))
	else:
		author_formset = AuthorFormSet(prefix='authors')
		book_formset = BookFormSet(prefix='books')
	return render(request, 'manage_books_authors.html', {'author_formset': author_formset, 'book_formset': book_formset})

def books_friends_create(request):
	FriendFormSet = formset_factory(FriendForm, extra=1)
	BookFormSet = formset_factory(BookFormForFriend, extra=1)
	if request.method == 'POST':
		friend_formset = FriendFormSet(request.POST, request.FILES, prefix='friends')
		book_formset = BookFormSet(request.POST, request.FILES, prefix='books')
		if friend_formset.is_valid() and book_formset.is_valid():
			for friend_form in friend_formset:  
				friend_form.save()  
			for book_form in book_formset:  
				book_form.save()  
			return HttpResponseRedirect(reverse_lazy('p_library:friend_form'))
	else:
		friend_formset = FriendFormSet(prefix='friends')  
		book_formset = BookFormSet(prefix='books')
	return render(
		request, 'manage_books_friends.html',  
		{  
			'friend_formset': friend_formset,  
			'book_formset': book_formset,  
		}  
	)

def friend_list(request):
	template = loader.get_template('friend_list.html')
	friends = Friend.objects.all()
	data = {"friends": friends,}
	return HttpResponse(template.render(data, request))
		
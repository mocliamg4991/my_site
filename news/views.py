from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from .utils import MyMixin
from django.contrib import messages
from django.contrib.auth import login, logout

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form" : form})

def user_logout(request):
    logout(request)
    return redirect ('login')
def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect ('login')
        else:
            messages.error (request, 'ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})



def test(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4','john5', 'paul6', 'george7', 'ringo8']
    paginator = Paginator(objects, 2)
    page_numb = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_numb)
    return render(request, 'news/test.html', {'page_obj':page_obj})

class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    queryset = News.objects.select_related('category')
    mixin_prop = 'hello world'
    paginate_by = 2
    #extra_context = {'title':'Главная страница'}
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {
#             'news': news,
#             'title':'Список новостей',
#     }
#     return render(request, template_name = 'news/index.html', context = context)

class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk = self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter( category_id = self.kwargs['category_id'], is_published=True).select_related('category')

# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news':news, 'category':category})

class ViewNews(DetailView):
    model = News
    #pk_url_kwarg = 'news_id'
    #template_name = 'news/news_detail.html'
    context_object_name = 'news_item'


# def view_news(request, news_id):
#     #news_item = News.objects.get(pk=news_id)
#
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item" : news_item})

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    succes_url = reverse_lazy ('home')
    login_url = '/home/'


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             #print(form.cleaned_data)
#             #news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form })

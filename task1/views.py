from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Buyer, Game, News, OtherModel, Article
from .forms import RegistrationForm, LoginForm, NewsForm
from .serializers import (
    BuyerSerializer, GameSerializer, NewsSerializer, OtherSerializer, ArticleSerializer
)

# Главная страница
def home(request):
    buyers = Buyer.objects.all()
    return render(request, 'home.html', {'buyers': buyers})

# Регистрация пользователя
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if password != repeat_password:
                messages.error(request, 'Пароли не совпадают')
                return render(request, 'registration.html', {'form': form})

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь уже существует')
                return render(request, 'registration.html', {'form': form})

            if Buyer.objects.filter(name=username).exists():
                messages.error(request, 'Пользователь уже существует в таблице Buyer')
                return render(request, 'registration.html', {'form': form})

            User.objects.create_user(username=username, password=password)
            Buyer.objects.create(name=username, age=age)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

# Вход в систему
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему')
                return redirect('home')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'login_page.html', {'form': form})

# Выход из системы
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('home')

# Список продуктов
def product_list(request):
    games = Game.objects.all()
    return render(request, 'product_list.html', {'games': games})

# Магазин
def shop(request):
    return render(request, 'shop.html')

# Контакты
def contact(request):
    return render(request, 'contact.html')

# О нас
def about(request):
    return render(request, 'about.html')

# Корзина
def cart(request):
    return render(request, 'cart.html')

# Страница выбора
def choice_page(request):
    return render(request, 'choice_page.html')

# Регистрация через Django
def sign_up_by_django(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            if password != repeat_password:
                messages.error(request, 'Пароли не совпадают')
                return render(request, 'fifth_task/registration_page.html', {'form': form})

            if age < 18:
                messages.error(request, 'Вы должны быть старше 18')
                return render(request, 'fifth_task/registration_page.html', {'form': form})

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь уже существует')
                return render(request, 'fifth_task/registration_page.html', {'form': form})

            if Buyer.objects.filter(name=username).exists():
                messages.error(request, 'Пользователь уже существует в таблице Buyer')
                return render(request, 'fifth_task/registration_page.html', {'form': form})

            User.objects.create_user(username=username, password=password)
            Buyer.objects.create(name=username, age=age)
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'fifth_task/registration_page.html', {'form': form})

# ViewSets для API
class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        Buyer.objects.all().delete()
        return Response({'status': 'all buyers deleted'})

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    permission_classes = [IsAuthenticated]

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    permission_classes = [IsAuthenticated]

class OtherViewSet(viewsets.ModelViewSet):
    queryset = OtherModel.objects.all()
    serializer_class = OtherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['field1']
    permission_classes = [IsAuthenticated]

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    permission_classes = [IsAuthenticated]

# Новости
def news_list(request):
    news_items = News.objects.all().order_by('-date')
    paginator = Paginator(news_items, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'news_list.html', {'news_items': page_obj})

# Добавление новости
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'add_news.html', {'form': form})

def news(request):
    news_list = News.objects.all().order_by('-date')
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'news.html', {'page_obj': page_obj})

def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm(instance=news_item)
    return render(request, 'news_detail.html', {'news_item': news_item, 'form': form})
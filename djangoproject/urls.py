"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py
from django.contrib import admin
from django.urls import path, include
from task1.views import (
    home, registration, product_list, shop, contact, about, cart, choice_page, news_detail,
    sign_up_by_django, login_view, logout_view, add_news, news_list,
    BuyerViewSet, GameViewSet, NewsViewSet, OtherViewSet, ArticleViewSet
)
from rest_framework.routers import DefaultRouter

# Создаем маршруты для API
router = DefaultRouter()
router.register(r'buyers', BuyerViewSet)
router.register(r'games', GameViewSet)
router.register(r'news', NewsViewSet)
router.register(r'other', OtherViewSet)
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # URL-адреса аутентификации
    path('', home, name='home'),  # Домашняя страница
    path('registration/', registration, name='registration'),  # Регистрация
    path('product_list/', product_list, name='product_list'),  # Список товаров
    path('shop/', shop, name='shop'),  # Магазин
    path('contact/', contact, name='contact'),  # Контакты
    path('about/', about, name='about'),  # О нас
    path('cart/', cart, name='cart'),  # Корзина
    path('choice_page/', choice_page, name='choice_page'),  # Выбор регистрации
    path('sign_up_by_django/', sign_up_by_django, name='sign_up_by_django'),  # Регистрация через Django
    path('login/', login_view, name='login'),  # Вход
    path('logout/', logout_view, name='logout'),  # Выход
    path('api/', include(router.urls)),  # API
    # Маршрут для списка новостей
    path('news/', news_list, name='news'),
    path('news/add/', add_news, name='add_news'),  # Страница для добавления новости
    path('news/list/', news_list, name='news_list'),  # Страница со списком новостей
    # Перенаправление с /news/ на /news/list/
    # Если у вас есть маршрут с аргументом news_id, убедитесь, что он правильно настроен
    path('news/<int:news_id>/', news_detail, name='news_detail'),
]
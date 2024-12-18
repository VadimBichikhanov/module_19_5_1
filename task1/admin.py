from django.contrib import admin
from .models import Game, Buyer, News
from django.utils.html import format_html
from django.db.models import F

# Админ-класс для модели Game
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_filter = ('size', 'cost')  # Фильтрация по полям size и cost
    list_display = ('title', 'cost', 'size', 'buyer_list')  # Отображение полей title, cost, size и покупатели
    search_fields = ('title',)  # Поиск по полю title
    list_per_page = 20  # Ограничение количества записей до 20
    list_editable = ('cost', 'size')  # Поля, доступные для редактирования в списке

    def buyer_list(self, obj):
        return ", ".join([buyer.name for buyer in obj.buyer.all()])
    buyer_list.short_description = "Покупатели"

    actions = ['set_discount']

    def set_discount(self, request, queryset):
        queryset.update(cost=F('cost') * 0.9)  # Установка скидки 10%
    set_discount.short_description = "Установить скидку 10%"

# Админ-класс для модели Buyer
@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_filter = ('balance', 'age')  # Фильтрация по полям balance и age
    list_display = ('name', 'balance_with_icon', 'age', 'games_count')  # Отображение полей name, balance, age и количество игр
    search_fields = ('name',)  # Поиск по полю name
    list_per_page = 30  # Ограничение количества записей до 30
    readonly_fields = ('balance',)  # Поле balance доступно только для чтения
    list_editable = ('age',)  # Поле age доступно для редактирования в списке

    @admin.display(description='Баланс')
    def balance_with_icon(self, obj):
        return format_html(f'<span style="color: {"green" if obj.balance > 0 else "red"};">{obj.balance}</span>')

    def games_count(self, obj):
        return obj.games.count()
    games_count.short_description = "Количество игр"

# Админ-класс для модели News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_content', 'date')  # Убираем 'content'
    list_filter = (('date', admin.DateFieldListFilter),)
    search_fields = ('title', 'content')
    list_per_page = 20
    list_display_links = ('title',)

    @admin.display(description='Содержание')
    def short_content(self, obj):
        return format_html(f'<a href="#" onclick="alert(\'{obj.content}\'); return false;">{obj.content[:50]}...</a>')
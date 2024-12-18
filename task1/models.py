from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Buyer(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    age = models.IntegerField()
    registration_date = models.DateTimeField(default=timezone.now)

    def clean(self):
        if self.age < 18:
            raise ValidationError("Возраст должен быть не менее 18 лет.")
        if self.age > 120:
            raise ValidationError("Возраст должен быть не более 120 лет.")
        if self.balance < 0:
            raise ValidationError("Баланс не может быть отрицательным.")

    def __str__(self):
        return f"{self.name} (Баланс: {self.balance})"

    def games_count(self):
        return self.games.count()

class Game(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    age_limited = models.BooleanField(default=False)
    buyer = models.ManyToManyField(Buyer, related_name='games', through='Purchase')

    def clean(self):
        if self.cost < 0:
            raise ValidationError("Стоимость не может быть отрицательной.")
        if self.size < 0:
            raise ValidationError("Размер не может быть отрицательным.")

    def __str__(self):
        return self.title

    def buyer_list(self):
        return ", ".join([buyer.name for buyer in self.buyer.all()])

class Purchase(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.buyer.name} купил {self.game.title}"

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

class OtherModel(models.Model):
    field1 = models.CharField(max_length=200)
    field2 = models.TextField()

    class Meta:
        ordering = ['field1']

    def __str__(self):
        return self.field1

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True, db_index=True)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
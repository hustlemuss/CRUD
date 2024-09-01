from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=60, unique=True, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Наименование товара'
        verbose_name_plural = 'Наименование товаров'

    def __str__(self):
        return self.title


class Stock(models.Model):
    address = models.CharField(max_length=200, unique=True, verbose_name='Адрес')
    products = models.ManyToManyField(
        Product,
        through='StockProduct',
        related_name='stocks',
    )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.address


class StockProduct(models.Model):
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        blank=True,
        related_name='positions',
        verbose_name='Склад',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name='Название товара',
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Стоимость',

    )

    class Meta:
        verbose_name = 'Наличие товара на сладе'
        verbose_name_plural = 'Наличие товаров на сладе'



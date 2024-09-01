from rest_framework import serializers
from rest_framework.response import Response

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class StockProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['stock', 'product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = StockProductSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(stock=stock,
                                        product=position['product'],
                                        quantity=position['quantity'],
                                        price=position['price'],
                                        )
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position in positions:
            if not StockProduct.objects.filter(product=position['product'], stock=instance):
                StockProduct.objects.create(product=position['product'],
                                            stock=instance,
                                            quantity=position['quantity'],
                                            price=position['price'],
                                            )
            else:
                StockProduct.objects.filter(product=position['product'], stock=instance) \
                    .update(quantity=position['quantity'],
                            price=position['price'],
                            )

        return stock

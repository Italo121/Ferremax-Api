from rest_framework import serializers
from .models import Sucursal, Producto, StockSucursal, Pedido, DetallePedido

class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class StockSucursalSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockSucursal
        fields = '__all__'

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

    def validate(self, data):
        producto = data['producto']
        cantidad = data['cantidad']
        pedido = data['pedido']

        try:
            stock = StockSucursal.objects.get(producto=producto, sucursal=pedido.sucursal)
        except StockSucursal.DoesNotExist:
            raise serializers.ValidationError("No hay stock registrado para este producto en esta sucursal.")

        if stock.cantidad < cantidad:
            raise serializers.ValidationError(f"No hay suficiente stock disponible. Solo quedan {stock.cantidad} unidades.")

        return data

    def create(self, validated_data):
        producto = validated_data['producto']
        cantidad = validated_data['cantidad']
        pedido = validated_data['pedido']

        stock = StockSucursal.objects.get(producto=producto, sucursal=pedido.sucursal)

        stock.cantidad -= cantidad
        stock.save()

        return DetallePedido.objects.create(**validated_data)
    
class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'sucursal', 'cliente', 'fecha', 'estado', 'detalles']

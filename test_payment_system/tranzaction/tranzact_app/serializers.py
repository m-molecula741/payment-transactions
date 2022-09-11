from rest_framework import serializers

def positive_integer_valid(value):
    if value < 0:
        raise serializers.ValidationError('отрицательный id')

def positive_float_valid(value):
    if value < 0:
        raise serializers.ValidationError('отрицательная сумма перевода')

class Serializers_data(serializers.Serializer):
    id = serializers.IntegerField(validators=[positive_integer_valid])
    amount = serializers.FloatField(validators=[positive_float_valid])
    id_to = serializers.IntegerField(validators=[positive_integer_valid])

class Serializers_history(serializers.Serializer):
    id = serializers.IntegerField(validators=[positive_integer_valid])
    id_from = serializers.IntegerField(validators=[positive_integer_valid])
    id_to = serializers.IntegerField(validators=[positive_integer_valid])
    amount = serializers.FloatField(validators=[positive_float_valid])
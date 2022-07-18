from rest_framework import serializers

from check.models import Check, PositionCheck

class PositionCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionCheck
        fields = ['name', 'count', 'price','position_amount']

class CheckSerializer(serializers.ModelSerializer):
    positions = PositionCheckSerializer(many=True)

    class Meta:
        model = Check
        fields = ['buyer', 'number', 'store','issue_date','check_amount','positions']

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        check = Check.objects.create(**validated_data)
        for position_data in positions_data:
            PositionCheck.objects.create(parent_check=check, **position_data)
        return check
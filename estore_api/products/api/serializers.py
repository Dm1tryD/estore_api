from rest_framework import serializers
from .. import models


class NotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notebook
        fields = '__all__'


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phone
        fields = '__all__'

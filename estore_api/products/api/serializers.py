from rest_framework import serializers
from .. import models


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Series
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unit
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = 'image.url'


class OsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OS
        fields = '__all__'


class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CPU
        fields = '__all__'


class GPUSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()

    class Meta:
        model = models.GPU
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Storage
        fields = '__all__'


class DisplayTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DisplayType
        fields = '__all__'


class DisplayResolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DisplayResolution
        fields = '__all__'


class DisplaySerializer(serializers.ModelSerializer):
    display_type = DisplayTypeSerializer()
    display_resolution = DisplayResolutionSerializer()

    class Meta:
        model = models.Display
        fields = '__all__'


class LaptopSerializer(serializers.ModelSerializer):
    os = OsSerializer()
    cpu = CPUSerializer()
    gpu = GPUSerializer()
    storage = StorageSerializer()
    display = DisplaySerializer()
    category = CategorySerializer()
    series = SeriesSerializer()
    color = ColorSerializer()
    brand = BrandSerializer()

    class Meta:
        model = models.ProductTypeLaptop
        fields = '__all__'


class PhoneSerializer(serializers.ModelSerializer):
    os = OsSerializer()
    cpu = CPUSerializer()
    gpu = GPUSerializer()
    storage = StorageSerializer()
    display = DisplaySerializer()
    category = CategorySerializer()
    series = SeriesSerializer()
    color = ColorSerializer()
    brand = BrandSerializer()
    image = ImageSerializer()

    class Meta:
        model = models.ProductTypePhone
        fields = '__all__'

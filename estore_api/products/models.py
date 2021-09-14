from django.db import models

LOW = 1
NORMAL = 2
HIGH = 3
STATUS_CHOICES = (
    (LOW, 'Low'),
    (NORMAL, 'Normal'),
    (HIGH, 'High'),
)

STORAGE_CHOICES = (
    ('HDD', 'HDD'),
    ('SSD', 'SSD'),
)


class BaseCharacters(models.Model):
    name = models.CharField(max_length=255)
    priority = models.IntegerField(choices=STATUS_CHOICES, default=NORMAL)

    class Meta:
        abstract = True


class Series(models.Model):
    name = models.CharField(max_length=255)
    year = models.DateField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField()

    def __str__(self):
        return self.image.name


class Product(BaseCharacters):
    """
    The basic abstract model for all products
    """
    description = models.CharField(max_length=1000)
    image = models.ManyToManyField(Image, related_name='%(class)s_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='%(class)s_brand')

    class Meta:
        abstract = True

    def get_price_with_discount(self):
        if self.discount:
            return self.price-((self.price/100)*self.discount)
        return self.price


class OS(models.Model):
    brand = models.ForeignKey(Brand, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} {self.version}"


class CPU(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class GPU(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Storage(models.Model):
    size = models.PositiveIntegerField()
    type = models.CharField(choices=STORAGE_CHOICES, max_length=3)

    def __str__(self):
        return f"{self.type} - {self.size} GB"


class DisplayType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DisplayResolution(models.Model):
    resolution = models.CharField(max_length=255)

    def __str__(self):
        return self.resolution


class Display(models.Model):
    display_type = models.ForeignKey(DisplayType, on_delete=models.CASCADE)
    display_size = models.DecimalField(max_digits=5, decimal_places=2)
    display_resolution = models.ForeignKey(DisplayResolution, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.display_type} {self.display_size} {self.display_resolution}"


class ElectronicTech(Product):
    """
    Abstract model for electronics products with a display, cpu, gpu, storage
    """
    os = models.ForeignKey(OS, on_delete=models.CASCADE)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, related_name='%(class)s_cpu')
    gpu = models.ForeignKey(GPU, on_delete=models.CASCADE, related_name='%(class)s_gpu')
    storage = models.ForeignKey(Storage, on_delete=models.DO_NOTHING)
    display = models.ForeignKey(Display, on_delete=models.DO_NOTHING)
    front_camera = models.CharField(max_length=50, blank=True)

    class Meta:
        abstract = True


class Notebook(ElectronicTech):

    def __str__(self):
        return self.name


class Phone(ElectronicTech):
    sim_amount = models.PositiveIntegerField()
    main_camera = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Component(models.Model):
    COMPONENT_TYPES = [
        ("CPU", "CPU"),
        ("GPU", "GPU"),
        ("RAM", "RAM"),
        ("Storage", "Storage"),
        ("Motherboard", "Motherboard"),
        ("PSU", "Power Supply"),
        ("Case", "Case"),
    ]

    name = models.CharField(max_length=255)
    component_type = models.CharField(max_length=50, choices=COMPONENT_TYPES)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class StoreItem(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.FloatField()


class Build(models.Model):
    name = models.CharField(max_length=100)


class BuildItem(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
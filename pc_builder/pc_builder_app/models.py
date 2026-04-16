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
        ("cpu", "CPU"),
        ("gpu", "GPU"),
        ("ram", "RAM"),
        ("storage", "Storage"),
        ("motherboard", "Motherboard"),
        ("psu", "Power Supply"),
        ("case", "Case"),
        ("cooler", "Cooler"),
    ]

    name = models.CharField(max_length=255)
    component_type = models.CharField(max_length=50, choices=COMPONENT_TYPES)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.component_type})"


class StoreItem(models.Model):
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return f"{self.component.name} - {self.supplier.name}"


class Build(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BuildItem(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
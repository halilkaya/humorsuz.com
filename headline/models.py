from django.utils.translation import ugettext_lazy as _
from django.db import models


class Category(models.Model):
    """
    Object categories
    """
    name = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Object(models.Model):
    """
    Objects
    """
    ImagePositions = (
        (0, 'centered'),
        (1, 'cover'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)
    image_position = models.IntegerField(choices=ImagePositions, default=0, blank=True, null=True)

    def __str__(self):
        return self.name


class Headline(models.Model):
    """
    Headline templates
    """
    text = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.text

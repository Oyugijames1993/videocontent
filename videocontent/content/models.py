from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse
from django.conf import settings
from django import forms
from django.forms import ImageField, FileInput



# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="thumbnails/")
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("content:course-detail", kwargs={"slug": self.slug})




class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    vimeo_id = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    order = models.IntegerField(default=1)
    # file = models.FileField(upload_to="uploads/")

    class Meta:
        ordering = ["order"]    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("content:video-detail", kwargs={
            "video_slug": self.slug,
            "slug": self.course.slug
        })
    
    
def pre_save_course(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
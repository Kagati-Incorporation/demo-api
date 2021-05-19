from django.contrib import admin

from .models import FileUpload


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'file')
    list_filter = ('user',)

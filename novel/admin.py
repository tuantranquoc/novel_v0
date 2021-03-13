from django.contrib import admin
from .models import User, Novel, Category, Chapter, Driver
from django_ace import AceWidget
from django import forms

# Register your models here.


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'
        widgets = {
            'content': AceWidget(
                mode='html', theme='twilight', wordwrap=True,
                width='100%', height='300px'
            )
        }


class NovelForm(forms.ModelForm):
    class Meta:
        model = Novel
        fields = '__all__'
        widgets = {
            'content': AceWidget(
                mode='html', theme='twilight', wordwrap=True,
                width='100%', height='300px'
            )
        }


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )

    class Meta:
        model = User


class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'public', 'removed',)
    search_fields = ('title',)
    list_filter = ('status', )
    form = NovelForm

    class Meta:
        model = Novel


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('title',)

    class Meta:
        model = Category
        

class DriverAdmin(admin.ModelAdmin):
    list_display = ('path', )
    search_fields = ('path',)

    class Meta:
        model = Driver


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter_number', 'novel',
                    'created_at', 'updated_at',)
    search_fields = ('title',)
    raw_id_fields = ('novel',)
    form = ChapterForm

    class Meta:
        model = Chapter


admin.site.register(Novel, NovelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Driver, DriverAdmin)

from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'brief', 'full_text', 'date', 'user')


admin.site.register(Review, ReviewAdmin)

from django.contrib import admin

from story.models import Journal, JournalImages


# Admin Configuration
class JournalImagesInline(admin.TabularInline):
    model = JournalImages
    extra = 1

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'updated_on', 'created_on')
    list_filter = ('user', 'date', 'updated_on', 'created_on')
    search_fields = ('user__username', 'journal')
    inlines = [JournalImagesInline]

@admin.register(JournalImages)
class JournalImagesAdmin(admin.ModelAdmin):
    list_display = ('journal', 'file')
    list_filter = ('journal__user',)
    search_fields = ('journal__user__username',)
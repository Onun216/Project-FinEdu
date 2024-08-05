from django.contrib import admin
from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from finedu_pedia.models import GlossaryItem, GlossaryPage


@admin.register(GlossaryPage)
class GlossaryPageAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'content',
    list_per_page = 50
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    prepopulated_fields = {
        "slug": ('title',),
    }


@admin.register(GlossaryItem)
class GlossaryItemAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = 'id', 'title', 'is_published',  'created_by',
    list_display_links = 'title',
    search_fields = 'id', 'slug', 'title', 'content',
    list_per_page = 50
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    readonly_fields = (
        'created_at', 'updated_at', 'created_by', 'updated_by',
        'link',
    )
    prepopulated_fields = {
        "slug": ('title',),
    }

    def link(self, obj):
        if not obj.pk:
            return '-'

        glossary_item_url = obj.get_absolute_url()
        safe_link = mark_safe(
            f'<a target="_blank" href="{glossary_item_url}">Ver item</a>'
        )

        return safe_link

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user  # type: ignore
        else:
            obj.created_by = request.user  # type: ignore

        obj.save()

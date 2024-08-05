from django.contrib import admin
from site_setup.models import MenuLink, SiteSetup


class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1


@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    list_display = 'title', 'description',
    inlines = MenuLinkInline,

    # Método verifica se já existe algum setup na base de dados.
    # Se sim, a permissão é retirada.
    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()

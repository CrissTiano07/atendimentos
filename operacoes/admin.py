from django.contrib import admin
from django.db.models import Count

from .models import Colaborador, Demanda, Participacao


class ParticipacaoInline(admin.TabularInline):
    model = Participacao
    extra = 1
    autocomplete_fields = ["colaborador"]


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ("nome", "ativo", "total_atendimentos")
    list_filter = ("ativo",)
    search_fields = ("nome",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_total=Count("participacoes"))

    @admin.display(description="Atendimentos", ordering="_total")
    def total_atendimentos(self, obj):
        return obj._total


@admin.register(Demanda)
class DemandaAdmin(admin.ModelAdmin):
    list_display = ("tipo", "data", "participantes")
    list_filter = ("tipo",)
    date_hierarchy = "data"
    search_fields = ("tipo", "colaboradores__nome")
    inlines = [ParticipacaoInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("colaboradores")

    @admin.display(description="Participantes")
    def participantes(self, obj):
        return ", ".join(c.nome for c in obj.colaboradores.all())

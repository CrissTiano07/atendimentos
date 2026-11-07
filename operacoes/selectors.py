from django.db.models import Count

from .models import Participacao


def participacoes(ano=None, mes=None, data_ini=None, data_fim=None,
                  tipo=None, colaborador_id=None):
    """Base de todas as consultas: participações com filtros opcionais."""
    qs = Participacao.objects.select_related("colaborador", "demanda")
    if ano:
        qs = qs.filter(demanda__data__year=ano)
    if mes:
        qs = qs.filter(demanda__data__month=mes)
    if data_ini:
        qs = qs.filter(demanda__data__gte=data_ini)
    if data_fim:
        qs = qs.filter(demanda__data__lte=data_fim)
    if tipo:
        qs = qs.filter(demanda__tipo__icontains=tipo)
    if colaborador_id:
        qs = qs.filter(colaborador_id=colaborador_id)
    return qs


def total_por_colaborador(**filtros):
    return (participacoes(**filtros)
            .values("colaborador__id", "colaborador__nome")
            .annotate(total=Count("demanda", distinct=True))
            .order_by("-total", "colaborador__nome"))


def historico(colaborador_id, **filtros):
    return (participacoes(colaborador_id=colaborador_id, **filtros)
            .order_by("demanda__data", "demanda__tipo")
            .values_list("demanda__data", "demanda__tipo"))


def por_tipo(colaborador_id, **filtros):
    return (participacoes(colaborador_id=colaborador_id, **filtros)
            .values("demanda__tipo")
            .annotate(total=Count("demanda", distinct=True))
            .order_by("-total"))


def comparar(nomes, **filtros):
    return total_por_colaborador(**filtros).filter(colaborador__nome__in=nomes)

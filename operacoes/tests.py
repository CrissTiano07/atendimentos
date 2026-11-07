from datetime import date

from django.db import IntegrityError, transaction
from django.test import TestCase

from . import selectors as sel
from .models import Colaborador, Demanda, Participacao


class ParticipacaoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.joao, cls.maria, cls.pedro = [
            Colaborador.objects.create(nome=n) for n in ("João", "Maria", "Pedro")
        ]
        dados = [
            ("Fiscalização de trânsito", date(2026, 11, 6), [cls.joao, cls.maria]),
            ("Apoio operacional", date(2026, 11, 6), [cls.joao]),
            ("Organização de equipe", date(2026, 10, 5), [cls.maria, cls.pedro]),
        ]
        for tipo, data, pessoas in dados:
            d = Demanda.objects.create(tipo=tipo, data=data)
            for c in pessoas:
                Participacao.objects.create(demanda=d, colaborador=c)

    def test_demanda_compartilhada_conta_uma_vez_para_cada_pessoa(self):
        totais = {r["colaborador__nome"]: r["total"] for r in sel.total_por_colaborador()}
        self.assertEqual(totais, {"João": 2, "Maria": 2, "Pedro": 1})

    def test_nao_permite_mesma_pessoa_duas_vezes_na_mesma_demanda(self):
        demanda = Demanda.objects.get(tipo="Apoio operacional")
        with self.assertRaises(IntegrityError), transaction.atomic():
            Participacao.objects.create(demanda=demanda, colaborador=self.joao)

    def test_filtro_por_ano_mes_e_tipo(self):
        totais = {
            r["colaborador__nome"]: r["total"]
            for r in sel.total_por_colaborador(ano=2026, mes=11, tipo="trânsito")
        }
        self.assertEqual(totais, {"João": 1, "Maria": 1})

    def test_filtro_por_periodo(self):
        totais = {
            r["colaborador__nome"]: r["total"]
            for r in sel.total_por_colaborador(data_ini=date(2026, 10, 1), data_fim=date(2026, 10, 31))
        }
        self.assertEqual(totais, {"Maria": 1, "Pedro": 1})

    def test_historico_ordenado_por_data_e_tipo(self):
        self.assertEqual(
            list(sel.historico(self.joao.id)),
            [(date(2026, 11, 6), "Apoio operacional"),
             (date(2026, 11, 6), "Fiscalização de trânsito")],
        )

    def test_por_tipo(self):
        tipos = {r["demanda__tipo"]: r["total"] for r in sel.por_tipo(self.maria.id)}
        self.assertEqual(tipos, {"Fiscalização de trânsito": 1, "Organização de equipe": 1})

    def test_comparar(self):
        nomes = [r["colaborador__nome"] for r in sel.comparar(["João", "Pedro"])]
        self.assertEqual(nomes, ["João", "Pedro"])

    def test_atalho_reverso_participacoes(self):
        self.assertEqual(self.joao.participacoes.count(), 2)
        self.assertEqual(self.joao.demandas.count(), 2)

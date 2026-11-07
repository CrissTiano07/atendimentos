from django.db import models


class Colaborador(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Demanda(models.Model):
    tipo = models.CharField(max_length=120)
    data = models.DateField()
    colaboradores = models.ManyToManyField(
        Colaborador, through="Participacao", related_name="demandas"
    )

    class Meta:
        ordering = ["-data"]

    def __str__(self):
        return f"{self.tipo} ({self.data:%d/%m/%Y})"


class Participacao(models.Model):
    demanda = models.ForeignKey(
        Demanda, on_delete=models.CASCADE, related_name="participacoes"
    )
    colaborador = models.ForeignKey(
        Colaborador, on_delete=models.CASCADE, related_name="participacoes"
    )

    class Meta:
        verbose_name_plural = "participações"
        constraints = [
            models.UniqueConstraint(
                fields=["demanda", "colaborador"], name="uniq_demanda_colaborador"
            )
        ]

    def __str__(self):
        return f"{self.colaborador} → {self.demanda}"

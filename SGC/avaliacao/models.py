from django.db import models
from abc import ABC, abstractmethod

# Create your models here.

"""
===============================================
PADRÃO STRATEGY – Estratégias de Avaliação
===============================================
"""

class EstrategiaAvaliacao(ABC):
    @abstractmethod
    def calcular(self, notas: list[float]) -> float:
        pass


class AvaliacaoMedia(EstrategiaAvaliacao):
    def calcular(self, notas: list[float]) -> float:
        return sum(notas) / len(notas) if notas else 0.0


class AvaliacaoPonderada(EstrategiaAvaliacao):
    def calcular(self, notas: list[float], pesos: list[float] = None) -> float:
        if not notas:
            return 0.0
        if not pesos or len(pesos) != len(notas):
            return sum(notas) / len(notas)
        total_peso = sum(pesos)
        return sum(n * p for n, p in zip(notas, pesos)) / total_peso


class AvaliacaoFinal(EstrategiaAvaliacao):
    def calcular(self, notas: list[float]) -> float:
        return max(notas) if notas else 0.0

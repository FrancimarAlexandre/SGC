from django.db import models
from django.utils import timezone

"""
===============================================
PADRÃO OBSERVER – Sistema de Notificações
===============================================
"""

class SistemaNotificacao:
    observadores = []

    @classmethod
    def adicionarObserver(cls, observer):
        if observer not in cls.observadores:
            cls.observadores.append(observer)

    @classmethod
    def removerObserver(cls, observer):
        if observer in cls.observadores:
            cls.observadores.remove(observer)

    @classmethod
    def notificarTodos(cls, mensagem):
        for observer in cls.observadores:
            observer.receberNotificacao(mensagem)



from django.db import models
from professor.models import Professor
from django.utils import timezone
from core.models import SistemaNotificacao
from avaliacao.models import AvaliacaoPonderada,AvaliacaoMedia,AvaliacaoFinal
from alunos.models import Aluno
# Create your models here.

class Curso(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="cursos")
    criado_em = models.DateTimeField(default=timezone.now)
    imagem = models.ImageField(
        upload_to='cursos/',
        blank=True,
        null=True,
        default='default/curso.png'
    )

    def __str__(self):
        return self.nome

    # ==========================
    # Métodos de domínio
    # ==========================
    def cadastrar(self):
        self.save()

    def matricularAluno(self, aluno):
        self.alunos.add(aluno)
        SistemaNotificacao.notificarTodos(f"{aluno.nome} foi matriculado no curso {self.nome}.")

    def removerAluno(self, aluno):
        self.alunos.remove(aluno)
        SistemaNotificacao.notificarTodos(f"{aluno.nome} foi removido do curso {self.nome}.")

    def calcularAvaliacao(self, notas: list[float]):
        if hasattr(self, "estrategia_avaliacao"):
            estrategia = self.estrategia_avaliacao
            return estrategia.calcular(notas)
        return sum(notas) / len(notas) if notas else 0.0

"""
===============================================
PADRÃO FACTORY – Criação de Cursos
===============================================
"""

class CursoFactory:
    @staticmethod
    def criarCurso(tipo: str, dados: dict) -> Curso:
        nome = dados.get("nome")
        descricao = dados.get("descricao")
        professor = dados.get("professor")
        imagem = dados.get("imagem", None)

        curso = Curso(nome=nome, descricao=descricao, professor=professor, imagem=imagem)
        curso.save()

        # Estratégia de avaliação baseada no tipo
        if tipo == "media":
            curso.estrategia_avaliacao = AvaliacaoMedia()
        elif tipo == "ponderada":
            curso.estrategia_avaliacao = AvaliacaoPonderada()
        else:
            curso.estrategia_avaliacao = AvaliacaoFinal()

        return curso

"""
===============================================
PADRÃO FACADE – Facade do Sistema
===============================================
"""

class SistemaFacade:
    def __init__(self):
        self.factory = CursoFactory()
        self.notificacao = SistemaNotificacao()

    def cadastrarCurso(self, tipo, dados):
        return self.factory.criarCurso(tipo, dados)

    def matricularAluno(self, alunoId, cursoId):
        aluno = Aluno.objects.get(id=alunoId)
        curso = Curso.objects.get(id=cursoId)
        curso.matricularAluno(aluno)

    def removerAluno(self, alunoId, cursoId):
        aluno = Aluno.objects.get(id=alunoId)
        curso = Curso.objects.get(id=cursoId)
        curso.removerAluno(aluno)

    def notificarAlunos(self, cursoId, mensagem):
        curso = Curso.objects.get(id=cursoId)
        for aluno in curso.alunos.all():
            aluno.receberNotificacao(mensagem)

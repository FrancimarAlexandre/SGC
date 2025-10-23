from django.db import models
from django.utils import timezone
from abc import ABC, abstractmethod

"""
===============================================
MODELOS PRINCIPAIS DO DOMÍNIO
===============================================
"""

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    especialidade = models.CharField(max_length=100)
    foto = models.ImageField(
        upload_to='professores/',
        blank=True,
        null=True,
        default='default/professor.png'
    )

    def __str__(self):
        return f"{self.nome} ({self.especialidade})"

    def cadastrar(self):
        """Cadastra o professor."""
        self.save()

    def ministrarCurso(self, curso):
        """Associa o professor a um curso."""
        curso.professor = self
        curso.save()


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, unique=True)
    cursos = models.ManyToManyField("Curso", related_name="alunos", blank=True)
    foto = models.ImageField(
        upload_to='alunos/',
        blank=True,
        null=True,
        default='default/aluno.png'
    )

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    def cadastrar(self):
        self.save()

    def matricular(self, curso):
        self.cursos.add(curso)
        curso.matricularAluno(self)

    def cancelarMatricula(self, curso):
        self.cursos.remove(curso)
        curso.removerAluno(self)

    def receberNotificacao(self, mensagem):
        """Recebe notificações do sistema."""
        print(f"📢 Notificação para {self.nome}: {mensagem}")


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

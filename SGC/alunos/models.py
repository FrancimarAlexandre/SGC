from django.db import models

# Create your models here.


class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=20, unique=True)
    cursos = models.ManyToManyField("cursos.Curso", related_name="alunos", blank=True)
    foto = models.ImageField(
        upload_to="alunos/", blank=True, null=True, default="default/aluno.png"
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

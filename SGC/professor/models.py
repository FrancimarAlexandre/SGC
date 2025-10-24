from django.db import models

# Create your models here.

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

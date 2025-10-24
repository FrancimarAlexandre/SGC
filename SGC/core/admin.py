from django.contrib import admin

from cursos.models import Curso
from professor.models import Professor
from alunos.models import Aluno

# Register your models here.
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome','descricao')
    list_display_links = ('nome',)
    list_filter = ('nome','professor')

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome','especialidade')
    list_filter = ('especialidade','nome')

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome','matricula')
    list_filter = ('nome','cursos',)
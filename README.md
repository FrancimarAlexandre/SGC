# 🧩 SGC - Sistema de Gerenciamento de Cursos (POO2)

## 📘 Diagrama de Classe UML

```mermaid
classDiagram
    %% ================================
    %% CLASSES PRINCIPAIS (MODELS)
    %% ================================
    class Curso {
        - id: int
        - nome: str
        - descricao: str
        - professor: Professor
        - alunos: list~Aluno~
        + adicionar_aluno(a: Aluno)
        + remover_aluno(a: Aluno)
        + notificar_observadores()
    }

    class Aluno {
        - id: int
        - nome: str
        - email: str
        + atualizar(mensagem: str)
    }

    class Professor {
        - id: int
        - nome: str
        - especialidade: str
    }

    %% ================================
    %% FACTORY
    %% ================================
    class CursoFactory {
        + criar_curso(nome: str, descricao: str, professor: Professor): Curso
    }

    %% ================================
    %% STRATEGY
    %% ================================
    class EstrategiaAvaliacao {
        <<interface>>
        + calcular_resultado(notas: list~float~): float
    }

    class MediaStrategy {
        + calcular_resultado(notas: list~float~): float
    }

    class PesoStrategy {
        + calcular_resultado(notas: list~float~): float
    }

    EstrategiaAvaliacao <|.. MediaStrategy
    EstrategiaAvaliacao <|.. PesoStrategy

    %% ================================
    %% OBSERVER
    %% ================================
    class Observador {
        <<interface>>
        + atualizar(mensagem: str)
    }

    class AlunoObservador {
        - aluno: Aluno
        + atualizar(mensagem: str)
    }

    Observador <|.. AlunoObservador
    Curso --> Observador : notifica

    %% ================================
    %% FACADE
    %% ================================
    class SistemaFacade {
        - cursos: list~Curso~
        + criar_novo_curso(nome, descricao, professor): Curso
        + matricular_aluno(curso: Curso, aluno: Aluno)
        + gerar_relatorio_curso(curso: Curso): str
    }

    %% ================================
    %% RELACIONAMENTOS
    %% ================================
    Professor "1" --> "many" Curso : leciona
    Curso "1" --> "many" Aluno : contem
    SistemaFacade --> CursoFactory : usa
    SistemaFacade --> Curso : gerencia

# ===========================
# Makefile - Djngo Project SGC
# ===========================

# Variáveis
PYTHON = python3
MANAGE=${PYTHON} manage.py

# Ambiente virtual (opcional)
VENV = venv
ACTIVATE = ${VENV}/bin/activate

# ============================
# Comandos principais do Django
# ============================

# Inicia o servidor local
run:
	${MANAGE} runserver

# Cria migrações
migrate:
	${MANAGE} makemigrations
	${MANAGE} migrate

# Cria superusuário
superuser:
	${MANAGE} createsuperuser

# Abre o shell interativo do Django
shell:
	${MANAGE} shell

# Limpa cache e migrações antigas (útil em desenvolvimeneto)
clean:
	find. -path "*/migrations/*.py" -not -nme "__init__.py" -delete
	find. -path "*/__pycache__/*" -delete
	tm -rf db.sqlite3

# ==================================
# Ambiente Virtual
# ==================================

# cria e ativa o ambiente virtual
venv:
	${PYTHON} -m venv ${VENV}

install:
	. ${ACTIVATE} $$ pip install -r requirements.txt

# ========================================
# Testes
# ========================================

test:
	${MANAGE} test

# =============================
# Auxílio
# =============================

help:
	@echo "Comandos disponíveis:"
	@echo "  make run           -> Inicia o servidor Django"
	@echo "  make migrate       -> Executa makemigrations e migrate"
	@echo "  make superuser     -> cria um super usuário"
	@echo "  make shell         -> Abre o shell do Django"
	@echo "  make clean         -> Remove migrações e cache"
	@echo "  make venv          -> Cria ambiente virtual"
	@echo "  make install       -> Instala dependências do requirements.txt"
	@echo "  make test          -> Executa os testes"
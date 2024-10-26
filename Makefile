# =================================================
# Arquivo MAKEFILE para auxiliar o desenvolvedor.
# =================================================

# Diretório raiz de minha aplicação.
APP_DIR=app
TESTS_DIR=tests

# Limpa arquivos temporários
clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -rf .mypy_cache
	@rm -f .coverage
	@rm -f .coverage.NB-SBDEV*
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f report.xml
	@rm -f *.log

# Monta o ambiente virtual
build-venv:
	python3 -m venv .venv

# Instala o ambiente
requirements-dev:
	@pip install --upgrade pip
	@pip install -r requirements/develop.txt

# Instala o ambiente
requirements-prod:
	@pip install --upgrade pip
	@pip install -r requirements/base.txt

requirements-check:
	@pip list -o
	@pip check

install: requirements-dev
	@echo ":-D Pacotes instalados"

env-dev:
	cp devtools/dotenv.dev .env
	@echo "Alterado para ambiente de dev."

env-test:
	cp devtools/dotenv.test .env
	@echo "Alterado para ambiente de teste."

bandit:
	@echo "=> Análise bandit"
	@bandit -r -f custom ${APP_DIR}
	@echo "=> bandit OK"

flake8:
	@echo "=> Análise flake8"
	@flake8 --show-source ${APP_DIR} ${TESTS_DIR}
	@echo "=> flake8 OK"

fix-python-import:
	@isort ${APP_DIR} ${TESTS_DIR} --profile=black --line-length=79

check-python-import:
	@echo "=> Análise isort"
	@isort ${APP_DIR} ${TESTS_DIR} --profile=black --line-length=79 --check-only
	@echo "=> isort OK"

black:
	@black ${APP_DIR} ${TESTS_DIR} --target-version=py38 --line-length=79

black-check:
	@echo "=> Análise black"
	@black ${APP_DIR} ${TESTS_DIR} --target-version=py38 --line-length=79 --check
	@echo "=> black OK"

dead-fixtures:
	@echo "=> Análise dead-fixtures"
	@pytest --dead-fixtures
	@echo "=> dead-fixtures OK"

check-types:
	@echo "=> Análise mypy"
	@mypy ${APP_DIR} --ignore-missing-imports --install-types --non-interactive
	@echo "=> mypy OK"

lint: clean fix-python-import black flake8 check-types dead-fixtures

check-lint: check-python-import black-check flake8 bandit check-types dead-fixtures

safety:
	cat requirements/base.txt | safety check --stdin

coverage: clean
	@py.test --cov=${APP_DIR} --cov-report=term-missing --cov-report=xml --junitxml=report.xml --cov-fail-under=90 \
	--durations=5 ${TEST_DIR}

coverage-html: clean
	@py.test --cov=${APP_DIR} --cov-report=term-missing --cov-report=html --cov-fail-under=90 ${TEST_DIR}

test: clean
	@py.test --durations=5
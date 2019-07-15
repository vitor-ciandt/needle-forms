#!/usr/bin/make -f
# -*- makefile -*-

PYTHONPATH := ${CURDIR}
export PYTHONPATH

export env $(cat .env)

all: help
help:
	@echo ""
	@echo "-- Help Menu"
	@echo ""
	@echo "   1. make clean 		- Clean all pyc and caches"
	@echo "   2. make test 			- Run tests"
	@echo "   3. make cov    		- Run tests with coverage"
	@echo "   4. make lint 		    - Run pylint"
	@echo "   5. make lint_report   - Run pylint and generate report"
	@echo "   6. make black 		- Run black"
	@echo ""
	@echo ""

.PHONY: clean
clean:
	@echo "Clean files pyc and caches..."
	rm -rf build/ dist/ docs/_build *.egg-info
	find $(CURDIR) -name "*.py[co]" -delete
	find $(CURDIR) -name "*.orig" -delete
	find $(CURDIR)/$(MODULE) -name "__pycache__" | xargs rm -rf
	find $(CURDIR)/$(MODULE) -name ".pytest_cache" | xargs rm -rf
	rm -f pylint-report.txt
	rm -f coverage.xml

.PHONY: test
test:
	@echo $(PYTHONPATH)
	    pipenv run pytest ./tests

.PHONY: cov
cov:
	pipenv run pytest --cov=./ --cov-report term --cov-report=xml:coverage.xml

.PHONY: lint
lint:
	pipenv run isort ./abstractions/*.py
	pipenv run pylint --rcfile=standard.rc ./abstractions/*.py

.PHONY: lint_report
lint_report:
	pipenv run pylint ./abstractions/*.py --reports=n --msg-template "{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint-report.txt || exit 0;

.PHONY: black
black:
	pipenv run black -l 79 .

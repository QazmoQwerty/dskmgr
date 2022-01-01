.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[1m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: lint
lint: ## Run mypy
	mypy -m libdskmgr.scripts.main

.PHONY: build
build: ## Build the .whl file
	python3 -m build

.PHONY: install
install: ## Install the .whl file
	python3 -m pip install --force-reinstall dist/dskmgr*.whl

.PHONY: upload
upload: ## Upload to pypi
	python3 -m twine upload dist/*

.PHONY: test
test: ## Install documentation
	python3 -m libdskmgr.scripts.main --wm bspwm-mock

.PHONY: install-docs
install-docs: ## Generate and install manpage
	pandoc -s -t man docs/manpage.md -o docs/dskmgr.1
	sudo bash -c "cat docs/dskmgr.1 | gzip > /usr/local/man/man1/dskmgr.1"
	sudo bash -c "ln -f /usr/local/man/man1/dskmgr.1 /usr/local/man/man1/dskmgrd.1"

.PHONY: clean
clean: ## Clean generated files
	-rm -rf dist dskmgr.egg-info/ .mypy_cache/ dist/ __pycache__/
.PHONY: git-hooks
git-hooks: .git/hooks/pre-commit

.git/hooks/%: git-hooks/%.sh
	install --mode=700 $< $@

.PHONY: lint
lint: lint-python lint-shell lint-svg

.PHONY: lint-python lint-shell lint-svg
lint-python lint-shell lint-svg:
	./$@.sh

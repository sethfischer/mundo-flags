.PHONY: git-hooks
git-hooks: .git/hooks/pre-commit

.git/hooks/%: git-hooks/%.sh
	install --mode=700 $< $@

.PHONY: lint
lint: lint-shell lint-svg

.PHONY: lint-shell lint-svg
lint-shell lint-svg:
	./$@.sh

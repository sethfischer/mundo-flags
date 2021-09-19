.PHONY: git-hooks
git-hooks: .git/hooks/pre-commit

.git/hooks/%: git-hooks/%.sh
	install --mode=700 $< $@

.PHONY: install-ide-config
install-ide-config:
	rsync --recursive ide-config/ .

.PHONY: lint
lint: lint-python lint-shell lint-svg

.PHONY: lint-python lint-shell lint-svg
lint-python lint-shell lint-svg:
	./$@.sh

.PHONY: convert
convert: rsvg-convert

.PHONY: rsvg-convert
rsvg-convert:
	mkdir -p _build/rsvg-convert-x54
	timeout 120 make -f examples/$@.makefile

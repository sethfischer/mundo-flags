.PHONY: install-git-hooks
install-git-hooks:
	git config --local core.hooksPath 'git-hooks'

.PHONY: install-ide-config
install-ide-config:
	rsync --recursive ide-config/ .

.PHONY: lint
lint: lint-python lint-shell lint-svg

.PHONY: lint-svg
lint-svg:
	./lint-svg.py --warn-on-error

.PHONY: lint-python lint-shell
lint-python lint-shell:
	./$@.sh

.PHONY: convert
convert: rsvg-convert imagemagick

.PHONY: rsvg-convert
rsvg-convert:
	mkdir -p _build/rsvg-convert-x54
	timeout 120 make -f examples/$@.makefile

.PHONY: imagemagick
imagemagick:
	mkdir -p _build/imagemagick/16x16 _build/imagemagick/x54
	timeout 600 make -f examples/$@.makefile

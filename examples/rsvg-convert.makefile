# Example makefile for converting svg to png using rsvg-convert
#
# Before running make the appropriate output directories must be manually
# created:
#
# mkdir -p _build/rsvg-convert-x54


SRC_DIR := ./flags/iso3166-1/
BUILD_DIR := ./_build/


# flag dependencies
FLAGS_SRC := $(wildcard $(SRC_DIR)*.svg)

# targets for flags 54 high
FLAGS_x54 := ${FLAGS_SRC:$(SRC_DIR)%.svg=$(BUILD_DIR)rsvg-convert-x54/%.png}

.PHONY: all
all: $(FLAGS_x54)

# flags 54 high png
$(BUILD_DIR)rsvg-convert-x54/%.png: $(SRC_DIR)%.svg
	rsvg-convert --height 54 --format png --output $@ $^

.PHONY: clean
clean:
	$(RM) $(BUILD_DIR)rsvg-convert-x54/*.png

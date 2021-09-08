# Example makefile for converting svg to raster formats using ImageMagick
#
# Before running make the appropriate output directories must be manually
# created:
#
# mkdir -p _build/imagemagick/16x16 _build/imagemagick/x54


SRC_DIR := ./svg/
BUILD_DIR := ./_build/


# flag dependencies
FLAGS_SRC := $(wildcard $(SRC_DIR)*.svg)

# targets for flags 16x16 png padded with transparent background
FLAGS_16x16 := ${FLAGS_SRC:$(SRC_DIR)%.svg=$(BUILD_DIR)imagemagick/16x16/%.png}
# targets for flags 54 high
FLAGS_x54 := ${FLAGS_SRC:$(SRC_DIR)%.svg=$(BUILD_DIR)imagemagick/x54/%.png}

.PHONY: all
all: $(FLAGS_16x16) $(FLAGS_x54)

# flags 16x16 png padded with transparent background
$(BUILD_DIR)imagemagick/16x16/%.png: $(SRC_DIR)%.svg
	convert SVG:$^ -resize 16x16 -background transparent -gravity center -extent 16x16 $@

# flags 54 high png
$(BUILD_DIR)imagemagick/x54/%.png: $(SRC_DIR)%.svg
	convert SVG:$^ -resize x54 $@

.PHONY: clean
clean:
	rm -r $(BUILD_DIR)imagemagick/16x16/*.png
	rm -r $(BUILD_DIR)imagemagick/x54/*.png

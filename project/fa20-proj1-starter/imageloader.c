/************************************************************************
**
** NAME:        imageloader.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**              Justin Yokota - Starter Code
**				Fuyukiri
**
**
** DATE:        2020-08-15
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "imageloader.h"

// Opens a .ppm P3 image file, and constructs an Image object.
// You may find the function fscanf useful.
// Make sure that you close the file with fclose before returning.
Image *readData(char *filename)
{
	// YOUR CODE HERE
	char format[10];
	uint32_t cols, rows, scale;
	Image *img = (Image *)malloc(sizeof(Image));

	FILE *fp;
	fp = fopen(filename, "r");

	fscanf(fp, "%s %u %u %u", format, &cols, &rows, &scale);

	img->rows = rows;
	img->cols = cols;
	Color **image = (Color **)malloc(rows * sizeof(Color *));
	img->image = image;

	for (int i = 0; i < rows; i++)
	{
		image[i] = (Color *)malloc(cols * sizeof(Color));
		for (int j = 0; j < cols; j++)
		{
			fscanf(fp, "%hhu %hhu %hhu", &image[i][j].R, &image[i][j].G, &image[i][j].B);
		}
	}
	fclose(fp);
	return img;
}

// Given an image, prints to stdout (e.g. with printf) a .ppm P3 file with the image's data.
void writeData(Image *image)
{
	// YOUR CODE HERE
	uint32_t cols = image->cols;
	uint32_t rows = image->rows;
	Color **img = image->image;
	printf("P3\n%u %u\n255\n", cols, rows);
	for (int i = 0; i < rows; i++)
	{
		for (int j = 0; j < cols - 1; j++)
		{
			printf("%3hhu %3hhu %3hhu   ", img[i][j].R, img[i][j].G, img[i][j].B);
		}
		printf("%3hhu %3hhu %3hhu", img[i][cols - 1].R, img[i][cols - 1].G, img[i][cols - 1].B);
		printf("\n");
	}
}

// Frees an image
void freeImage(Image *image)
{
	// uint32_t cols = image->cols;
	uint32_t rows = image->rows;
	Color **img = image->image;
	for (int i = 0; i < rows; i++)
	{
		free(img[i]);
	}
	free(img);
	free(image);
}

// void main() {
// 	Image *i = readData("./testInputs/JohnConway.ppm");
// 	writeData(i);
// 	freeImage(i);
// }
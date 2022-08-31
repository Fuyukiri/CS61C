/************************************************************************
**
** NAME:        steganography.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**				Justin Yokota - Starter Code
**				Fuyukiri
**
** DATE:        2020-08-23
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

// Determines what color the cell at the given row/col should be. This should not affect Image, and should allocate space for a new Color.
Color *evaluateOnePixel(Image *image, int row, int col)
{
	// YOUR CODE HERE
	Color *color = (Color *)malloc(sizeof(Color));
	uint32_t digit = image->image[row][col].B;
	digit &= 1;
	if (digit == 1)
	{
		color->R = 255;
		color->G = 255;
		color->B = 255;
	}
	else
	{
		color->R = 0;
		color->G = 0;
		color->B = 0;
	}
	return color;
}

// Given an image, creates a new image extracting the LSB of the B channel.
Image *steganography(Image *image)
{
	// YOUR CODE HERE
	Image *new_img = (Image *)malloc(sizeof(Image));

	uint32_t rows = image->rows;
	uint32_t cols = image->cols;

	Color **colors = (Color **)malloc(rows * sizeof(Color *));

	new_img->image = colors;
	new_img->cols = cols;
	new_img->rows = rows;
	for (uint32_t i = 0; i < rows; i++)
	{
		colors[i] = (Color *)malloc(cols * sizeof(Color));
		for (uint32_t j = 0; j < cols; j++)
		{
			Color *c = evaluateOnePixel(image, i, j);
			colors[i][j] = *c;
			free(c);
		}
	}
	return new_img;
}

/*
Loads a file of ppm P3 format from a file, and prints to stdout (e.g. with printf) a new image,
where each pixel is black if the LSB of the B channel is 0,
and white if the LSB of the B channel is 1.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a file of ppm P3 format (not necessarily with .ppm file extension).
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!
*/
int main(int argc, char **argv)
{
	// YOUR CODE HERE
	Image *img = readData(argv[1]);
	Image *new_img = steganography(img);

	writeData(new_img);

	freeImage(new_img);
	freeImage(img);
	return 0;
}

/************************************************************************
**
** NAME:        gameoflife.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Justin Yokota - Starter Code
**              Fuyukiri
**
**
** DATE:        2020-08-23
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

// Determines what color the cell at the given row/col should be. This function allocates space for a new Color.
// Note that you will need to read the eight neighbors of the cell in question. The grid "wraps", so we treat the top row as adjacent to the bottom row
// and the left column as adjacent to the right column.
int directions[8][2] = {{1, 0}, {0, 1}, {1, 1}, {-1, 1}, {-1, 0}, {0, -1}, {-1, -1}, {1, -1}};

int check_if_live(Image *image, int row, int col)
{
	if (image->image[row][col].R | image->image[row][col].G | image->image[row][col].B)
	{
		return 1;
	}
	return 0;
}

Color *evaluateOneCell(Image *image, int row, int col, uint32_t rule)
{
	// YOUR CODE HERE
	Color *color = (Color *)malloc(sizeof(Color));
	uint32_t rows = image->rows;
	uint32_t cols = image->cols;
	int live = check_if_live(image, row, col);
	int live_neighbor = 0;
	uint8_t RGB[3] = {0, 0, 0};
	int max_RGB = 0;
	for (int i = 0; i < 8; i++)
	{
		int x = (row + directions[i][0] + rows) % rows;
		int y = (col + directions[i][1] + cols) % cols;
		if (check_if_live(image, x, y))
		{
			live_neighbor++;
		}
		uint8_t R = image->image[x][y].R;
		uint8_t G = image->image[x][y].G;
		uint8_t B = image->image[x][y].B;
		int sum = R + G + B;
		if (sum > max_RGB)
		{
			RGB[0] = R;
			RGB[1] = G;
			RGB[2] = B;
		}
	}

	int check_bit = rule;

	if (live)
	{
		check_bit >>= 9;
	}

	check_bit >>= live_neighbor;
	check_bit &= 1;

	if (check_bit)
	{
		color->R = RGB[0];
		color->G = RGB[1];
		color->B = RGB[2];
	}
	else
	{
		color->R = 0;
		color->G = 0;
		color->B = 0;
	}

	return color;
}

// The main body of Life; given an image and a rule, computes one iteration of the Game of Life.
// You should be able to copy most of this from steganography.c
Image *life(Image *image, uint32_t rule)
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
			Color *c = evaluateOneCell(image, i, j, rule);
			colors[i][j] = *c;
			free(c);
		}
	}
	return new_img;
}

/*
Loads a .ppm from a file, computes the next iteration of the game of life, then prints to stdout the new image.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a .ppm.
argv[2] should contain a hexadecimal number (such as 0x1808). Note that this will be a string.
You may find the function strtol useful for this conversion.
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!

You may find it useful to copy the code from steganography.c, to start.
*/
int main(int argc, char **argv)
{
	// YOUR CODE HERE
	if (argc != 3)
	{
		return -1;
	}
	Image *image = readData(argv[1]);
	uint32_t rule = strtol(argv[2], NULL, 16);
	Image *next_image = life(image, rule);
	writeData(next_image);
	freeImage(image);
	freeImage(next_image);
	return 0;
}

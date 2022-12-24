#include "matrix.h"
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

// Include SSE intrinsics
#if defined(_MSC_VER)
#include <intrin.h>
#elif defined(__GNUC__) && (defined(__x86_64__) || defined(__i386__))
#include <immintrin.h>
#include <x86intrin.h>
#endif

/* Below are some intel intrinsics that might be useful
 * void _mm256_storeu_pd (double * mem_addr, __m256d a)
 * __m256d _mm256_set1_pd (double a)
 * __m256d _mm256_set_pd (double e3, double e2, double e1, double e0)
 * __m256d _mm256_loadu_pd (double const * mem_addr)
 * __m256d _mm256_add_pd (__m256d a, __m256d b)
 * __m256d _mm256_sub_pd (__m256d a, __m256d b)
 * __m256d _mm256_fmadd_pd (__m256d a, __m256d b, __m256d c)
 * __m256d _mm256_mul_pd (__m256d a, __m256d b)
 * __m256d _mm256_cmp_pd (__m256d a, __m256d b, const int imm8)
 * __m256d _mm256_and_pd (__m256d a, __m256d b)
 * __m256d _mm256_max_pd (__m256d a, __m256d b)
*/

/* Generates a random double between low and high */
double rand_double(double low, double high) 
{
    double range = (high - low);
    double div = RAND_MAX / range;
    return low + (rand() / div);
}

/* Generates a random matrix */
void rand_matrix(matrix *result, unsigned int seed, double low, double high) 
{
    srand(seed);
    for (int i = 0; i < result->rows; i++) 
    {
        for (int j = 0; j < result->cols; j++) {
            set(result, i, j, rand_double(low, high));
        }
    }
}

/*
 * Returns the double value of the matrix at the given row and column.
 * You may assume `row` and `col` are valid. Note that the matrix is in row-major order.
 */
double get(matrix *mat, int row, int col) 
{
    // Task 1.1 TODO
    int index = mat->cols * row + col;
    return mat->data[index];
}

/*
 * Sets the value at the given row and column to val. You may assume `row` and
 * `col` are valid. Note that the matrix is in row-major order.
 */
void set(matrix *mat, int row, int col, double val) 
{
    mat->data[row * (mat->cols) + col] = val;
}

/*
 * Allocates space for a matrix struct pointed to by the double pointer mat with
 * `rows` rows and `cols` columns. You should also allocate memory for the data array
 * and initialize all entries to be zeros. `parent` should be set to NULL to indicate that
 * this matrix is not a slice. You should also set `ref_cnt` to 1.
 * You should return -1 if either `rows` or `cols` or both have invalid values. Return -2 if any
 * call to allocate memory in this function fails.
 * Return 0 upon success.
 */
int allocate_matrix(matrix **mat, int rows, int cols) 
{
    // Task 1.2 TODO
    // HINTS: Follow these steps.
    // 1. Check if the dimensions are valid. Return -1 if either dimension is not positive.
    // 2. Allocate space for the new matrix struct. Return -2 if allocating memory failed.
    // 3. Allocate space for the matrix data, initializing all entries to be 0. Return -2 if allocating memory failed.
    // 4. Set the number of rows and columns in the matrix struct according to the arguments provided.
    // 5. Set the `parent` field to NULL, since this matrix was not created from a slice.
    // 6. Set the `ref_cnt` field to 1.
    // 7. Store the address of the allocated matrix struct at the location `mat` is pointing at.
    // 8. Return 0 upon success.
    if (rows < 1 || cols < 1) 
    {
        return -1;
    }
    matrix *new_matrix = (matrix *) malloc(sizeof(matrix));
    if (new_matrix == NULL) 
    {
        return -2;
    }

    // constructor
    new_matrix->rows = rows;
    new_matrix->cols = cols;
    new_matrix->data = (double *) calloc(rows * cols, sizeof(double));
    if (new_matrix->data == NULL) 
    {
        return -2;
    }
    new_matrix->ref_cnt = 1;
    new_matrix->parent = NULL;
    *mat = new_matrix;
    return 0;
}

/*
 * You need to make sure that you only free `mat->data` if `mat` is not a slice and has no existing slices,
 * or that you free `mat->parent->data` if `mat` is the last existing slice of its parent matrix and its parent
 * matrix has no other references (including itself).
 */
void deallocate_matrix(matrix *mat) 
{
    // Task 1.3 TODO
    // HINTS: Follow these steps.
    // 1. If the matrix pointer `mat` is NULL, return.
    // 2. If `mat` has no parent: decrement its `ref_cnt` field by 1. If the `ref_cnt` field becomes 0, then free `mat` and its `data` field.
    // 3. Otherwise, recursively call `deallocate_matrix` on `mat`'s parent, then free `mat`.
    if (mat == NULL) 
    {
        return;
    }
    if (mat->parent == NULL) 
    {
        mat->ref_cnt--;
        if (mat->ref_cnt == 0) 
        {
            free(mat->data);
            free(mat);
        }
    } else 
    {
        deallocate_matrix(mat->parent);
        free(mat);
    }
}

/*
 * Allocates space for a matrix struct pointed to by `mat` with `rows` rows and `cols` columns.
 * Its data should point to the `offset`th entry of `from`'s data (you do not need to allocate memory)
 * for the data field. `parent` should be set to `from` to indicate this matrix is a slice of `from`
 * and the reference counter for `from` should be incremented. Lastly, do not forget to set the
 * matrix's row and column values as well.
 * You should return -1 if either `rows` or `cols` or both have invalid values. Return -2 if any
 * call to allocate memory in this function fails.
 * Return 0 upon success.
 * NOTE: Here we're allocating a matrix struct that refers to already allocated data, so
 * there is no need to allocate space for matrix data.
 */
int allocate_matrix_ref(matrix **mat, matrix *from, int offset, int rows, int cols) 
{
    // Task 1.4 TODO
    // HINTS: Follow these steps.
    // 1. Check if the dimensions are valid. Return -1 if either dimension is not positive.
    // 2. Allocate space for the new matrix struct. Return -2 if allocating memory failed.
    // 3. Set the `data` field of the new struct to be the `data` field of the `from` struct plus `offset`.
    // 4. Set the number of rows and columns in the new struct according to the arguments provided.
    // 5. Set the `parent` field of the new struct to the `from` struct pointer.
    // 6. Increment the `ref_cnt` field of the `from` struct by 1.
    // 7. Store the address of the allocated matrix struct at the location `mat` is pointing at.
    // 8. Return 0 upon success.
    if (rows < 1 || cols < 1) 
    {
        return -1;
    }
    int col = offset % from->cols;
    int row = offset / from->cols;
    if ((row + rows) > from->rows || (col + cols) > from -> cols) 
    {
        return -1;
    }
    matrix *slice_matrix = (matrix *)malloc(sizeof(matrix));
    if (slice_matrix == NULL) 
    {
        return -2;
    }
    slice_matrix->data = from->data + offset;
    slice_matrix->rows = rows;
    slice_matrix->cols = cols;
    slice_matrix->parent = from;
    from->ref_cnt += 1;
    *mat = slice_matrix;
    return 0;
}

/*
 * Sets all entries in mat to val. Note that the matrix is in row-major order.
 */
void fill_matrix(matrix *mat, double val) 
{
    // Task 1.5 TODO
    __m256d register_vec;
    #pragma omp parallel for
    for (int i = 0; i < mat->rows * mat->cols / 4; i++) 
    {
        register_vec = _mm256_set_pd (val, val, val, val);
        _mm256_storeu_pd (mat->data + i * 4, register_vec);
    }
    #pragma omp parallel for
    for (int i = mat->rows * mat->cols / 4 * 4; i < mat->cols * mat->rows; i++) 
    {
        mat->data[i] = val;
    } 
}

/*
 * Store the result of taking the absolute value element-wise to `result`.
 * Return 0 upon success.
 * Note that the matrix is in row-major order.
 */
int abs_matrix(matrix *result, matrix *mat) {
    // Task 1.5 TODO
    if (result == NULL || mat == NULL || result->cols != mat ->cols || result->rows != mat->rows) 
    {
        return -1;
    }

    __m256d register_vec;
    #pragma omp parallel for
    for (int i = 0; i < mat->rows * mat-> cols / 4; i++) 
    {
        register_vec = _mm256_loadu_pd(mat->data + i * 4);
        __m256d sign_mask = _mm256_set1_pd(-0.0);
        __m256d abs_vec = _mm256_andnot_pd(sign_mask, register_vec);
        _mm256_storeu_pd (result->data + i * 4, abs_vec);
    }
    #pragma omp parallel for
    for (int i = mat->rows * mat-> cols / 4 * 4; i < mat->rows * mat-> cols; i++) 
    {
        if (mat->data[i] < 0) 
        {
            result->data[i] = -mat->data[i];
        } 
        else 
        {
            result->data[i] = mat->data[i];
        }
    }
    return 0;
}

/*
 * (OPTIONAL)
 * Store the result of element-wise negating mat's entries to `result`.
 * Return 0 upon success.
 * Note that the matrix is in row-major order.
 */
int neg_matrix(matrix *result, matrix *mat) 
{
    if (result->cols != mat ->cols || result->rows != mat->rows || result->data == NULL) 
    {
        return -1;
    }

    __m256d register_vec;
    __m256d zero = _mm256_set1_pd(0);
    #pragma omp parallel for
    for (int i = 0; i < mat->rows * mat-> cols / 4; i++) 
    {
        register_vec = _mm256_loadu_pd(mat->data + i * 4);
        __m256d negative = _mm256_sub_pd(zero, register_vec);
        _mm256_storeu_pd (result->data + i * 4, negative);
    }
    #pragma omp parallel for
    for (int i = mat->rows * mat-> cols / 4 * 4; i < mat->rows * mat-> cols; i++) 
    {
            result->data[i] = -mat->data[i];
    }
    return 0;
}

/*
 * Store the result of adding mat1 and mat2 to `result`.
 * Return 0 upon success.
 * You may assume `mat1` and `mat2` have the same dimensions.
 * Note that the matrix is in row-major order.
 */
int add_matrix(matrix *result, matrix *mat1, matrix *mat2) 
{
    // Task 1.5 TODO
    if (result->cols != mat1 ->cols || result->rows != mat1->rows || result->data == NULL) 
    {
        return -1;
    }
    if (mat1->cols != mat2->cols || mat1->rows != mat2->rows) 
    {
        return -1;
    }

    __m256d register_mat1;
    __m256d register_mat2;
    #pragma omp parallel for
    for (int i = 0; i < mat1->rows * mat1-> cols / 4; i++) 
    {
        register_mat1 = _mm256_loadu_pd(mat1->data + i * 4);
        register_mat2 = _mm256_loadu_pd(mat2->data + i * 4);
        __m256d res = _mm256_add_pd(register_mat1, register_mat2);
        _mm256_storeu_pd (result->data + i * 4, res);
    }
    #pragma omp parallel for
    for (int i = mat1->rows * mat1-> cols / 4 * 4; i < mat1->rows * mat1-> cols; i++) 
    {
        result->data[i] = mat1->data[i] + mat2->data[i];
    }
    return 0;
}

/*
 * (OPTIONAL)
 * Store the result of subtracting mat2 from mat1 to `result`.
 * Return 0 upon success.
 * You may assume `mat1` and `mat2` have the same dimensions.
 * Note that the matrix is in row-major order.
 */
int sub_matrix(matrix *result, matrix *mat1, matrix *mat2) {
    // Task 1.5 TODO
    if (result->cols != mat1 ->cols || result->rows != mat1->rows || result->data == NULL) 
    {
        return -1;
    }
    if (mat1->cols != mat2->cols || mat1->rows != mat2->rows) 
    {
        return -1;
    }
    __m256d register_mat1;
    __m256d register_mat2;
    #pragma omp parallel for
    for (int i = 0; i < mat1->rows * mat1-> cols / 4; i++) 
    {
        register_mat1 = _mm256_loadu_pd(mat1->data + i * 4);
        register_mat2 = _mm256_loadu_pd(mat2->data + i * 4);
        __m256d res = _mm256_sub_pd(register_mat1, register_mat2);
        _mm256_storeu_pd (result->data + i * 4, res);
    }
    #pragma omp parallel for
    for (int i = mat1->rows * mat1-> cols / 4 * 4; i < mat1->rows * mat1-> cols; i++) 
    {
        result->data[i] = mat1->data[i] - mat2->data[i];
    }
    return 0;
}

/*
 * Store the result of multiplying mat1 and mat2 to `result`.
 * Return 0 upon success.
 * Remember that matrix multiplication is not the same as multiplying individual elements.
 * You may assume `mat1`'s number of columns is equal to `mat2`'s number of rows.
 * Note that the matrix is in row-major order.
 */
int mul_matrix(matrix *result, matrix *mat1, matrix *mat2) 
{
    // Task 1.6 TODO
    if (mat1 == NULL || mat2 == NULL || result == NULL || mat1->rows != result->rows || mat2->cols != result->cols 
    || mat1->cols != mat2->rows) 
    {
        return -1;
    }
    
    // Small matrix just use naive algorithm
    if(mat1->cols * mat1->rows < 500) {
        for (int i = 0; i < mat1->rows ; i++) 
        {
            for (int j = 0; j < mat2->cols; j++) 
            {
                for (int k = 0; k < mat1->cols; k++) 
                {
                    result->data[i * mat2->cols + j] += mat1->data[i * mat1->cols + k] * mat2->data[k * mat2->cols + j];
                }
            }
        }
        return 0;
    }
    __m256d register_mat1, register_trans, mul_res;
    double cur_res;

    // SIMD
    matrix* trans = transpose(mat2);
    if (mat1->cols * mat1->rows < 1000) {
        for (int i = 0; i < mat1->rows; i++) 
        {
            for (int j = 0; j < trans->rows; j++) 
            {
                mul_res = _mm256_set1_pd(0);
                for (int k = 0; k < mat1->cols / 4; k++) 
                {
                    register_mat1 = _mm256_loadu_pd(mat1->data + i * mat1->cols + k * 4);
                    register_trans = _mm256_loadu_pd(trans->data + j * trans->cols + k * 4);
                    mul_res = _mm256_add_pd(mul_res, _mm256_mul_pd(register_mat1, register_trans));
                }
                result->data[i * trans->rows + j] += mul_res[0] + mul_res[1] + mul_res[2] + mul_res[3];
                for (int k = mat1->cols / 4 * 4; k < mat1->cols; k++) 
                {
                    result->data[i * trans->rows + j] += mat1->data[i * mat1->cols + k] * trans->data[j * trans->cols + k];
                }
            }
        }
        return 0;
    }
    
    // Parallel Programming
    #pragma omp parallel for private (cur_res, mul_res) collapse(2)
    for (int i = 0; i < mat1->rows; i++) 
    {
        for (int j = 0; j < trans->rows; j++) 
        {
            cur_res = 0;
            mul_res = _mm256_set1_pd(0); 
            for (int k = 0; k < mat1->cols / 4; k++) 
            {
                register_mat1 = _mm256_loadu_pd(mat1->data + i * mat1->cols + k * 4);
                register_trans = _mm256_loadu_pd(trans->data + j * trans->cols + k * 4);
                mul_res = _mm256_add_pd(mul_res, _mm256_mul_pd(register_mat1, register_trans));
            }

            cur_res += (mul_res[0] + mul_res[1] + mul_res[2] + mul_res[3]);

            for (int k = mat1->cols / 4 * 4; k < mat1->cols; k++) 
            {
                cur_res += get(mat1, i, k) * get(trans, j, k);
            }
            set(result, i, j, cur_res);
        }
    }
    
    deallocate_matrix(trans);
    return 0;
}


/* 
 * transpose the matrix
 */
matrix* transpose(matrix *mat) 
{
    matrix* result = NULL;
    allocate_matrix(&result, mat->cols, mat->rows);
    #pragma omp parallel for collapse(2)
    for(int i = 0; i < result->rows; i++)
    {
		for(int j = 0; j < result->cols; j++)
        {
			result->data[i * result->cols + j] = mat->data[j * mat->cols + i];
		}
	}
    return result;
}

/*
 * Store the result of raising mat to the (pow)th power to `result`.
 * Return 0 upon success.
 * Remember that pow is defined with matrix multiplication, not element-wise multiplication.
 * You may assume `mat` is a square matrix and `pow` is a non-negative integer.
 * Note that the matrix is in row-major order.
 */
int pow_matrix(matrix *result, matrix *mat, int pow) 
{
    // Task 1.6 TODO
    if (mat->cols != mat->rows || result->rows != result->cols || result->data == NULL || pow < 0) {
        return -1;
    }
    if (pow == 0) {
        #pragma omp parallel for
        for (int i = 0; i < mat->rows; i++) 
        {
            for (int j = 0; j < mat->cols; j++) 
            {
                if (i == j) {
                    result->data[i * mat->cols + j] = 1.0;
                } else {
                    result->data[i * mat->cols + j] = 0.0;
                }
            }
        }
    }
    else if (pow == 1) {
        add_matrix(result, result, mat);
    }
    else 
    {
        matrix *temp = NULL;
        matrix *temp_zero = NULL;
        allocate_matrix(&temp, mat->rows, mat->cols);
        allocate_matrix(&temp_zero, mat->rows, mat->cols);
        add_matrix(result, temp_zero, mat);
        for (int i = 1; i < pow; i++) 
        {
            add_matrix(temp, temp_zero, result);
            fill_matrix(result, 0);
            mul_matrix(result, temp, mat);
        }
    }

    return 0;
}

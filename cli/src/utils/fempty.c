/*H**********************************************************************
* FILENAME :
*       [main.c]
*
* DESIGN REF:
*       [0000]
*
* DESCRIPTION :
*       [describe].
*
* PUBLIC FUNCTIONS :
*       [type function(param)]
*
* NOTES :
*       [notes]
*
*       [copyright]
*
* AUTHOR :
*       [name]
*
* START DATE :
        [dd mmm yy]
*
* CHANGES :
*
*       REF NO          VERSION         DATE            WHO         DETAIL
*       [0000]          [0000]          [dd mmm yy]     [initials]  [detail]
*
*H**********************************************************************/

#include <stdio.h>
#include <stdlib.h>

FILE *fempty(const char *fpath, char *mode)
{
    FILE *fp = fopen(fpath, "w");
    if (fp == NULL)
    {
        printf("Error: opening file\n");
        exit(1);
    }
    fclose(fp);
    fp = fopen(fpath, mode);
    if (fp == NULL)
    {
        printf("Error: opening file\n");
        exit(1);
    }
    return fp;
}
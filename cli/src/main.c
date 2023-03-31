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
#include <string.h>
#include <dirent.h>
#include <limits.h>

#include "include/utils.h"

int main()
{
    struct dirent *entry;
    DIR *dir = opendir(CORPUS_DIR_PATH);
    if (dir == NULL)
    {
        printf("Error: opening directory\n");
        exit(1);
    }
    FILE *fout = fempty(CORPUS_OUTPUT_FILE_PATH, "ab");
    while ((entry = readdir(dir)) != NULL)
    {
        if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
            continue;
        char fpath[PATH_MAX + 1];
        strcpy(fpath, CORPUS_DIR_PATH);
        strcat(fpath, "/");
        strcat(fpath, entry->d_name);
        fpack(fclean(fpath), fout);
    }
    closedir(dir);
    fclose(fout);
    printf("*** all file successfully processed ***\n");
    return 0;
}

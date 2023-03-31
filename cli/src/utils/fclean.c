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

#include "../include/utils.h"

void trim_extra_spaces(char *str);
void pop_first_line(char *fbuffer, char *label, char *data);

DOC_RAW *fclean(const char *fpath)
{
    DOC_RAW *doc_raw = calloc(1, sizeof(DOC_RAW));
    doc_raw->label = calloc(1, MAX_LABEL_LENGTH);
    doc_raw->data = calloc(1, MAX_DATA_LENGTH);

    FILE *fp;
    long fsize;
    fp = fopen(fpath, "rb");
    if (fp == NULL)
    {
        printf("Error: File not found\n");
        exit(1);
    }
    fseek(fp, 0, SEEK_END);
    fsize = ftell(fp);
    if (fsize > MAX_DATA_LENGTH)
    {
        printf("Error: %s exceeds the data limit of %d\n", fpath, MAX_DATA_LENGTH);
        exit(1);
    }
    fseek(fp, 0, SEEK_SET);

    char *fbuffer = calloc(1, fsize + 1);
    fread(fbuffer, fsize, 1, fp);
    fbuffer[fsize] = '\0';

    pop_first_line(fbuffer, doc_raw->label, doc_raw->data);
    trim_extra_spaces(doc_raw->data);

    free(fbuffer);
    fclose(fp);
    return doc_raw;
}

void pop_first_line(char *fbuffer, char *label, char *data)
{
    char *rest = strchr(fbuffer, '\n');
    if (rest != NULL)
    {
        strcpy(data, rest + 1);
        strncpy(label, fbuffer, rest - fbuffer);
        label[rest - fbuffer] = '\0';
        *rest = '\0';
        memmove(fbuffer, fbuffer + strlen(fbuffer) + 1, strlen(fbuffer + 1) + 1);
    }
}

void trim_extra_spaces(char *str)
{
    int i, j;
    int str_len = strlen(str);
    int consecutive_spaces = 0;
    for (i = 0, j = 0; i < str_len; i++)
    {
        if (str[i] != ' ' && str[i] != '\t' && str[i] != '\n')
        {
            str[j++] = str[i];
            consecutive_spaces = 0;
        }
        else if (consecutive_spaces < 1)
        {
            str[j++] = ' ';
            consecutive_spaces++;
        }
    }
    if (j > 0 && str[j - 1] == ' ')
    {
        j--;
    }
    str[j] = '\0';
}

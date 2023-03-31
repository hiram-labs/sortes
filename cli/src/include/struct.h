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

#ifndef STRUCT_H
#define STRUCT_H

#include "def.h"

typedef struct
{
    char str[MAX_SEQ_LENGTH];
} SEQ;

typedef struct
{
    short seqs_len;
    char label[MAX_LABEL_LENGTH];
    SEQ seqs[MAX_NUM_OF_SEQ];
} DOC_PROCESSED;

typedef struct
{
    char *label;
    char *data;
} DOC_RAW;

#endif
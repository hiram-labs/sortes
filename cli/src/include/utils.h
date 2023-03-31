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

#ifndef UTILS_H
#define UTILS_H

#include "struct.h"

FILE *fempty(const char *fpath, char *mode);
DOC_RAW *fclean(const char *fpath);
void fpack(DOC_RAW *doc, FILE *fp);
void spush(DOC_PROCESSED *ds, SEQ *seq);

#endif

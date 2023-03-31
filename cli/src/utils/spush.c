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

void spush(DOC_PROCESSED *doc_proc, SEQ *seq)
{
    if ((size_t)(doc_proc->seqs_len * MAX_SEQ_LENGTH) > (sizeof(doc_proc->seqs)))
    {
        printf("Error: the document is bigger than allowed\n");
        exit(1);
    }
    doc_proc->seqs[doc_proc->seqs_len] = *seq;
    doc_proc->seqs_len++;
}
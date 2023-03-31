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

void fpack(DOC_RAW *doc_raw, FILE *fp)
{
    DOC_PROCESSED *doc_proc = calloc(1, sizeof(DOC_PROCESSED));
    SEQ *seq = calloc(1, sizeof(SEQ));
    doc_proc->seqs_len = 0;
    strcpy(doc_proc->label, doc_raw->label);

    short strider = 0;
    short data_len = strlen(doc_raw->data);
    while (strider < data_len)
    {
        strncpy(seq->str, doc_raw->data + strider, MAX_SEQ_LENGTH - 1);
        seq->str[MAX_SEQ_LENGTH - 1] = '\0';
        spush(doc_proc, seq);
        strider += DATA_SEQ_STRIDE;
    }

    doc_proc->seqs_len++;
    fwrite(&doc_proc->seqs_len, sizeof(short), 1, fp);
    fwrite(doc_proc->label, sizeof(doc_proc->label), 1, fp);
    fwrite(doc_proc->seqs, sizeof(seq->str), doc_proc->seqs_len, fp);

    free(seq);
    free(doc_proc);
    free(doc_raw->label);
    free(doc_raw->data);
    free(doc_raw);
}
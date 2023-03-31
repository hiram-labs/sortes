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

#ifndef DEF_H
#define DEF_H

/**
 * these are provided in the make file from environment variables.
 *the ifndef guards here are just to help with intellisense during development
**/
#ifndef MAX_LABEL_LENGTH
#define MAX_LABEL_LENGTH 0
#endif
#ifndef MAX_DATA_LENGTH
#define MAX_DATA_LENGTH 0
#endif
#ifndef MAX_SEQ_LENGTH
#define MAX_SEQ_LENGTH 0
#endif
#ifndef MAX_NUM_OF_SEQ
#define MAX_NUM_OF_SEQ 0
#endif
#ifndef DATA_SEQ_STRIDE
#define DATA_SEQ_STRIDE 0
#endif
#ifndef CORPUS_DIR_PATH
#define CORPUS_DIR_PATH ""
#endif
#ifndef CORPUS_OUTPUT_FILE_PATH
#define CORPUS_OUTPUT_FILE_PATH ""
#endif

#endif
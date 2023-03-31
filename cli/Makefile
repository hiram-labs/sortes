CC=gcc
CFLAGS=-Wall -Wextra -Werror -O2
LDFLAGS=
LIBS=

DEFINE=-DMAX_LABEL_LENGTH=$(MAX_LABEL_LENGTH)\
	-DMAX_DATA_LENGTH=$(MAX_DATA_LENGTH)\
	-DMAX_SEQ_LENGTH=$(MAX_SEQ_LENGTH)\
	-DMAX_NUM_OF_SEQ=$(MAX_NUM_OF_SEQ)\
	-DDATA_SEQ_STRIDE=$(DATA_SEQ_STRIDE)\
	-DCORPUS_DIR_PATH=\"$(CORPUS_DIR_PATH)\"\
	-DCORPUS_OUTPUT_FILE_PATH=\"$(CORPUS_OUTPUT_FILE_PATH)\"

SRC_DIR=src
INC_DIR=$(SRC_DIR)/include
UTILS_DIR=$(SRC_DIR)/utils
OBJ_DIR=obj
BIN_DIR=bin

SRCS=$(wildcard $(SRC_DIR)/*.c)
UTILS_SRCS=$(wildcard $(UTILS_DIR)/*.c)
OBJS=$(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SRCS))
UTILS_OBJS=$(patsubst $(UTILS_DIR)/%.c,$(OBJ_DIR)/%.o,$(UTILS_SRCS))
DEPS=$(OBJS:.o=.d)
BIN=$(BIN_DIR)/$(APP_NAME)

.PHONY: all clean

all: $(BIN)

$(BIN): $(OBJS) $(UTILS_OBJS) | $(BIN_DIR)
	$(CC) $(LDFLAGS) $(LIBS) $^ -o $@

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c $(INC_DIR)/def.h $(INC_DIR)/struct.h $(INC_DIR)/utils.h | $(OBJ_DIR)
	$(CC) $(CFLAGS) $(DEFINE) -MMD -MP -c $< -o $@

$(OBJ_DIR)/%.o: $(UTILS_DIR)/%.c $(INC_DIR)/def.h $(INC_DIR)/struct.h $(INC_DIR)/utils.h | $(OBJ_DIR)
	$(CC) $(CFLAGS) $(DEFINE) -MMD -MP -c $< -o $@

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

clean:
	rm -rf $(BIN_DIR) $(OBJ_DIR)

-include $(DEPS)

#!/bin/make

##### Variables #####
CC=gcc
LD=gcc
CFLAGS= -Wall -Wextra -Wunreachable-code -Wwrite-strings
CFLAGS:= -Imain/ -IkColoring/ -ImaxFlowMinCost/ -ImaxFlow/ -IshortestPath/ -ItransitiveClosure
LDFLAGS=

SRCDIR=src/
SRCS=$(wildcard $(SRCDIR)*.c)
OBJDIR=obj/
OBJS=$(addprefix $(OBJDIR), $(notdir $(SRCS:.c=.o)))
BINDIR=bin/

##### Rules #####
all: $(BINDIR)graphtoolbox

$(BINDIR)graphtoolbox: $(OBJS)
	@echo [LD] $@
	@$(LD) $^ -o $@ $(LDFLAGS)

##### Generic rules #####
$(OBJDIR)%.o: $(SRCDIR)%.c
	@echo [CC] $@
	@$(CC) -c $< -o $@ $(CFLAGS)

##### Tools #####
.PNOHY: clean mrproper

clean:
	@find . -name \*~ -exec rm -fv {} \;
	@rm -fv $(OBJDIR)*.o

mrproper: clean
	@rm -fv $(BINDIR)*


#ifndef GRAPH_H_03022011101047
#define GRAPH_H_03022011101047

typedef struct
{
    char *name;
    int color;
} Node;

typedef struct
{
    int capacity;
    int cost;
} Edge;

typedef struct
{
    Node *nodes;
    Edge **edges;
} Graph;

#endif

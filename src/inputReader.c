#include <string.h>
#include <glib-object.h>
#include <json-glib/json-glib.h>

int inputParser(char *path, JsonParser *parser) {
    GError *error;
    error = NULL;
    json_parser_load_from_file(parser, path, &error); 

    if(error) {
        g_error_free (error);
        return EXIT_FAILURE;
    }

    
    return EXIT_SUCCESS;
}

int inputTransform(JsonParser *parser, Graph *graph) {
    JsonNode *root;
    JsonReader *reader;
    int num_nodes, num_edges;
    int i;

    root = json_parser_get_root(parser);
    reader = json_reader_new(root);

    // Is the graph directed ?
    json_reader_read_member(reader, "oriented") 
    if(json_reader_get_boolean_value(reader)) {
       graph->directed = DIRECTED; 
    } else {
        graph->directed = NOT_DIRECTED;
    }
    json_reader_end_member(reader);

    // Get the nodes
    json_reader_read_member(reader, "nodes"); 
    if(json_reader_is_array(reader)) {

        // Allocate the memory for the nodes, and for the edges
        num_nodes = json_reader_count_elements(reader); 
        graph->nodes = malloc(num_nodes * sizeof(Node));
        graph->edges = malloc(num_nodes * sizeof(Edge *));

        for(i=0; i < num_nodes; i++) {
            graph->edges[i] = malloc(num_nodes * sizeof(Edge));
        }

        for(i=0; i < num_nodes; i++) {
            json_reader_read_element(reader, i);
            readNode(json_reader_get_value(reader), graph); 
            json_reader_end_element(reader);
        }
    }
    json_reader_end_member(reader);


    // Get the edges
    json_reader_read_member(reader, "edges"); 
    if(json_reader_is_array(reader)) {

        for(i=0; i < num_edges; i++) {
            json_reader_read_element(reader, i);
            reader(json_reader_get_value(reader), graph); 
            json_reader_end_element(reader);
        }
    }
    json_reader_end_member(reader);




    

    return EXIT_SUCCESS;
}

int readNode(Graph *graph, JsonNode *node) {

}

int readEdge(Graph *graph, JsonNode *node) {

}


int jsonToGraph(char *path, Graph *graph) {
    JsonParser *parser;

    g_type_init();
    parser = json_parser_new();

    if(inputReader(path, parser) == EXIT_SUCCESS) {
        if(inputTransform(parser, graph) == EXIT_FAILURE) {
            g_object_unref (parser);
            return EXIT_FAILURE;   
        }
    } else {
        g_object_unref (parser);
        return EXIT_FAILURE;
    }
   
    g_object_unref (parser);
    return EXIT_SUCCESS; 
}


/*
 * This file was generated by build_grammar.py, DO NOT MODIFY!
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "parser-generated.h"
#include "error.h"

const nterm_type_t parser_starting_nterm = NT_PROGRAM;
parser_table_t *table;

static struct {
    void *data;
    size_t size;
    size_t offset;
} mempool;

static void *alloc_tokens(size_t n_tokens)
{
    void *ret = (uint8_t *) mempool.data + mempool.offset;
    mempool.offset += n_tokens * sizeof(token_type_t);
    return ret;
}
size_t parser_get_table_index(nterm_type_t nterm, term_type_t term)
{
    return ((nterm << 6) + term) % 464;
}
const char *nterm_to_readable(nterm_type_t nterm)
{
    switch(nterm) {
    case NT_PROGRAM: return "<program>";
    case NT_RETURN_STATEMENT: return "<return-statement>";
    case NT_RET_EXPRESSION_LIST: return "<ret-expression-list>";
    case NT_FOR_LOOP: return "<for-loop>";
    case NT_EXPRESSION_LIST: return "<expression-list>";
    case NT_STATEMENT_LIST: return "<statement-list>";
    case NT_DECL_OPTIONAL_ASSIGNMENT: return "<decl-optional-assignment>";
    case NT_OPTIONAL_FUN_EXPRESSION_LIST: return "<optional-fun-expression-list>";
    case NT_EXPRESSION_LIST2: return "<expression-list2>";
    case NT_OPTIONAL_FOR_STEP: return "<optional-for-step>";
    case NT_TYPE_LIST2: return "<type-list2>";
    case NT_RET_EXPRESSION_LIST2: return "<ret-expression-list2>";
    case NT_GLOBAL_STATEMENT: return "<global-statement>";
    case NT_IDENTIFIER_LIST2: return "<identifier-list2>";
    case NT_REPEAT_UNTIL: return "<repeat-until>";
    case NT_FUNC_DEF: return "<func-def>";
    case NT_ASSIGNMENT: return "<assignment>";
    case NT_FUNC_DECL: return "<func-decl>";
    case NT_IDENTIFIER_LIST_WITH_TYPES: return "<identifier-list-with-types>";
    case NT_IDENTIFIER_LIST_WITH_TYPES2: return "<identifier-list-with-types2>";
    case NT_GLOBAL_STATEMENT_LIST: return "<global-statement-list>";
    case NT_COND_STATEMENT: return "<cond-statement>";
    case NT_IDENTIFIER_WITH_TYPE: return "<identifier-with-type>";
    case NT_STATEMENT: return "<statement>";
    case NT_FUN_EXPRESSION_LIST2: return "<fun-expression-list2>";
    case NT_FUNC_TYPE_LIST2: return "<func-type-list2>";
    case NT_IDENTIFIER_LIST: return "<identifier-list>";
    case NT_TYPE_LIST: return "<type-list>";
    case NT_FUNC_CALL: return "<func-call>";
    case NT_COND_OPT_ELSEIF: return "<cond-opt-elseif>";
    case NT_DECLARATION: return "<declaration>";
    case NT_FUNC_TYPE_LIST: return "<func-type-list>";
    case NT_WHILE_LOOP: return "<while-loop>";
    }
    return "<unknown-nterm>";
}
const char *term_to_readable(term_type_t term)
{
    switch(term) {
    case T_FUNCTION: return "function";
    case T_WHILE: return "while";
    case T_TYPE: return "<type>";
    case T_CARET: return "^";
    case T_GT: return ">";
    case T_ELSEIF: return "elseif";
    case T_EQUALS: return "=";
    case T_BOOL: return "<bool>";
    case T_THEN: return "then";
    case T_LPAREN: return "(";
    case T_END: return "end";
    case T_IDENTIFIER: return "<identifier>";
    case T_LT: return "<";
    case T_REQUIRE: return "require";
    case T_DOUBLE_EQUALS: return "==";
    case T_OPTIONAL_EXPRESSION_LIST: return "<optional-expression-list>";
    case T_GLOBAL: return "global";
    case T_ELSE: return "else";
    case T_NUMBER: return "<number>";
    case T_COLON: return ":";
    case T_MINUS: return "-";
    case T_LOCAL: return "local";
    case T_TILDE_EQUALS: return "~=";
    case T_GTE: return ">=";
    case T_HASH: return "#";
    case T_STRING: return "<string>";
    case T_RETURN: return "return";
    case T_DOUBLE_DOT: return "..";
    case T_INTEGER: return "<integer>";
    case T_COMMA: return ",";
    case T_EOF: return "$";
    case T_FOR: return "for";
    case T_ASTERISK: return "*";
    case T_DO: return "do";
    case T_IF: return "if";
    case T_REPEAT: return "repeat";
    case T_UNTIL: return "until";
    case T_EXPRESSION: return "<expression>";
    case T_BREAK: return "break";
    case T_PLUS: return "+";
    case T_SLASH: return "/";
    case T_RPAREN: return ")";
    case T_PERCENT: return "%";
    case T_NIL: return "nil";
    case T_LTE: return "<=";
    case T_DOUBLE_SLASH: return "//";
    }
    return "<unknown-term>";
}
int parser_init()
{
    mempool.data = calloc(141, sizeof(token_type_t));
    if(mempool.data == NULL) {
        return E_INT;
    }
    mempool.size = 141 * sizeof(token_type_t);

    size_t rule_count = 464;
    table = calloc(1, sizeof(parser_table_t) + rule_count * sizeof(exp_list_t));
    if(table == NULL) {
        return E_INT;
    }

    table->bucket_count = rule_count;
    table->data[13] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[13].data[0].term = T_REQUIRE;
    table->data[13].data[1].term = T_STRING;
    table->data[13].data[2].is_nterm = true;
    table->data[13].data[2].nterm = NT_GLOBAL_STATEMENT_LIST;
    table->data[368] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[368].data[0].is_nterm = true;
    table->data[368].data[0].nterm = NT_GLOBAL_STATEMENT;
    table->data[368].data[1].is_nterm = true;
    table->data[368].data[1].nterm = NT_GLOBAL_STATEMENT_LIST;
    table->data[363] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[363].data[0].is_nterm = true;
    table->data[363].data[0].nterm = NT_GLOBAL_STATEMENT;
    table->data[363].data[1].is_nterm = true;
    table->data[363].data[1].nterm = NT_GLOBAL_STATEMENT_LIST;
    table->data[352] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[352].data[0].is_nterm = true;
    table->data[352].data[0].nterm = NT_GLOBAL_STATEMENT;
    table->data[352].data[1].is_nterm = true;
    table->data[352].data[1].nterm = NT_GLOBAL_STATEMENT_LIST;
    table->data[382] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[320] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[320].data[0].is_nterm = true;
    table->data[320].data[0].nterm = NT_FUNC_DECL;
    table->data[304] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[304].data[0].is_nterm = true;
    table->data[304].data[0].nterm = NT_FUNC_DEF;
    table->data[315] = (exp_list_t){ .valid = true, .size = 4, .data = alloc_tokens(4) };
    table->data[315].data[0].term = T_IDENTIFIER;
    table->data[315].data[1].term = T_LPAREN;
    table->data[315].data[2].term = T_OPTIONAL_EXPRESSION_LIST;
    table->data[315].data[3].term = T_RPAREN;
    table->data[176] = (exp_list_t){ .valid = true, .size = 8, .data = alloc_tokens(8) };
    table->data[176].data[0].term = T_GLOBAL;
    table->data[176].data[1].term = T_IDENTIFIER;
    table->data[176].data[2].term = T_COLON;
    table->data[176].data[3].term = T_FUNCTION;
    table->data[176].data[4].term = T_LPAREN;
    table->data[176].data[5].is_nterm = true;
    table->data[176].data[5].nterm = NT_TYPE_LIST;
    table->data[176].data[6].term = T_RPAREN;
    table->data[176].data[7].is_nterm = true;
    table->data[176].data[7].nterm = NT_FUNC_TYPE_LIST;
    table->data[338] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[338].data[0].term = T_TYPE;
    table->data[338].data[1].is_nterm = true;
    table->data[338].data[1].nterm = NT_TYPE_LIST2;
    table->data[377] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[366] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[205] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[205].data[0].term = T_COMMA;
    table->data[205].data[1].is_nterm = true;
    table->data[205].data[1].nterm = NT_TYPE_LIST2;
    table->data[217] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[206] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[32] = (exp_list_t){ .valid = true, .size = 8, .data = alloc_tokens(8) };
    table->data[32].data[0].term = T_FUNCTION;
    table->data[32].data[1].term = T_IDENTIFIER;
    table->data[32].data[2].term = T_LPAREN;
    table->data[32].data[3].is_nterm = true;
    table->data[32].data[3].nterm = NT_IDENTIFIER_LIST_WITH_TYPES;
    table->data[32].data[4].term = T_RPAREN;
    table->data[32].data[5].is_nterm = true;
    table->data[32].data[5].nterm = NT_FUNC_TYPE_LIST;
    table->data[32].data[6].is_nterm = true;
    table->data[32].data[6].nterm = NT_STATEMENT_LIST;
    table->data[32].data[7].term = T_END;
    table->data[235] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[235].data[0].is_nterm = true;
    table->data[235].data[0].nterm = NT_IDENTIFIER_WITH_TYPE;
    table->data[235].data[1].is_nterm = true;
    table->data[235].data[1].nterm = NT_IDENTIFIER_LIST_WITH_TYPES2;
    table->data[265] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[254] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[317] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[317].data[0].term = T_COMMA;
    table->data[317].data[1].is_nterm = true;
    table->data[317].data[1].nterm = NT_IDENTIFIER_WITH_TYPE;
    table->data[317].data[2].is_nterm = true;
    table->data[317].data[2].nterm = NT_IDENTIFIER_LIST_WITH_TYPES2;
    table->data[329] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[318] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[147] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[147].data[0].term = T_COLON;
    table->data[147].data[1].term = T_TYPE;
    table->data[147].data[2].is_nterm = true;
    table->data[147].data[2].nterm = NT_FUNC_TYPE_LIST2;
    table->data[158] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[128] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[163] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[166] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[159] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[144] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[149] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[129] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[139] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[162] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[138] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[154] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[237] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[237].data[0].term = T_COMMA;
    table->data[237].data[1].term = T_TYPE;
    table->data[237].data[2].is_nterm = true;
    table->data[237].data[2].nterm = NT_FUNC_TYPE_LIST2;
    table->data[238] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[208] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[243] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[246] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[239] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[224] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[229] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[209] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[219] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[242] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[218] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[234] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[355] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[355].data[0].is_nterm = true;
    table->data[355].data[0].nterm = NT_STATEMENT;
    table->data[355].data[1].is_nterm = true;
    table->data[355].data[1].nterm = NT_STATEMENT_LIST;
    table->data[358] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[358].data[0].is_nterm = true;
    table->data[358].data[0].nterm = NT_STATEMENT;
    table->data[358].data[1].is_nterm = true;
    table->data[358].data[1].nterm = NT_STATEMENT_LIST;
    table->data[351] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[351].data[0].is_nterm = true;
    table->data[351].data[0].nterm = NT_STATEMENT;
    table->data[351].data[1].is_nterm = true;
    table->data[351].data[1].nterm = NT_STATEMENT_LIST;
    table->data[341] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[341].data[0].is_nterm = true;
    table->data[341].data[0].nterm = NT_STATEMENT;
    table->data[341].data[1].is_nterm = true;
    table->data[341].data[1].nterm = NT_STATEMENT_LIST;
    table->data[321] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[321].data[0].is_nterm = true;
    table->data[321].data[0].nterm = NT_STATEMENT;
    table->data[321].data[1].is_nterm = true;
    table->data[321].data[1].nterm = NT_STATEMENT_LIST;
    table->data[331] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[331].data[0].is_nterm = true;
    table->data[331].data[0].nterm = NT_STATEMENT;
    table->data[331].data[1].is_nterm = true;
    table->data[331].data[1].nterm = NT_STATEMENT_LIST;
    table->data[354] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[354].data[0].is_nterm = true;
    table->data[354].data[0].nterm = NT_STATEMENT;
    table->data[354].data[1].is_nterm = true;
    table->data[354].data[1].nterm = NT_STATEMENT_LIST;
    table->data[346] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[346].data[0].is_nterm = true;
    table->data[346].data[0].nterm = NT_STATEMENT;
    table->data[346].data[1].is_nterm = true;
    table->data[346].data[1].nterm = NT_STATEMENT_LIST;
    table->data[356] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[337] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[330] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[325] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[350] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[114] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[114].data[0].is_nterm = true;
    table->data[114].data[0].nterm = NT_COND_STATEMENT;
    table->data[81] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[81].data[0].is_nterm = true;
    table->data[81].data[0].nterm = NT_WHILE_LOOP;
    table->data[111] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[111].data[0].is_nterm = true;
    table->data[111].data[0].nterm = NT_FOR_LOOP;
    table->data[115] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[115].data[0].is_nterm = true;
    table->data[115].data[0].nterm = NT_REPEAT_UNTIL;
    table->data[101] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[101].data[0].is_nterm = true;
    table->data[101].data[0].nterm = NT_DECLARATION;
    table->data[91] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[91].data[0].is_nterm = true;
    table->data[91].data[0].nterm = NT_ASSIGNMENT;
    table->data[106] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[106].data[0].is_nterm = true;
    table->data[106].data[0].nterm = NT_RETURN_STATEMENT;
    table->data[118] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[118].data[0].term = T_BREAK;
    table->data[450] = (exp_list_t){ .valid = true, .size = 5, .data = alloc_tokens(5) };
    table->data[450].data[0].term = T_IF;
    table->data[450].data[1].term = T_EXPRESSION;
    table->data[450].data[2].term = T_THEN;
    table->data[450].data[3].is_nterm = true;
    table->data[450].data[3].nterm = NT_STATEMENT_LIST;
    table->data[450].data[4].is_nterm = true;
    table->data[450].data[4].nterm = NT_COND_OPT_ELSEIF;
    table->data[5] = (exp_list_t){ .valid = true, .size = 4, .data = alloc_tokens(4) };
    table->data[5].data[0].term = T_ELSEIF;
    table->data[5].data[1].term = T_EXPRESSION;
    table->data[5].data[2].term = T_THEN;
    table->data[5].data[3].is_nterm = true;
    table->data[5].data[3].nterm = NT_COND_OPT_ELSEIF;
    table->data[17] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[17].data[0].term = T_ELSE;
    table->data[17].data[1].is_nterm = true;
    table->data[17].data[1].nterm = NT_STATEMENT_LIST;
    table->data[17].data[2].term = T_END;
    table->data[10] = (exp_list_t){ .valid = true, .size = 1, .data = alloc_tokens(1) };
    table->data[10].data[0].term = T_END;
    table->data[193] = (exp_list_t){ .valid = true, .size = 5, .data = alloc_tokens(5) };
    table->data[193].data[0].term = T_WHILE;
    table->data[193].data[1].term = T_EXPRESSION;
    table->data[193].data[2].term = T_DO;
    table->data[193].data[3].is_nterm = true;
    table->data[193].data[3].nterm = NT_STATEMENT_LIST;
    table->data[193].data[4].term = T_END;
    table->data[223] = (exp_list_t){ .valid = true, .size = 10, .data = alloc_tokens(10) };
    table->data[223].data[0].term = T_FOR;
    table->data[223].data[1].term = T_IDENTIFIER;
    table->data[223].data[2].term = T_EQUALS;
    table->data[223].data[3].term = T_EXPRESSION;
    table->data[223].data[4].term = T_COMMA;
    table->data[223].data[5].term = T_EXPRESSION;
    table->data[223].data[6].is_nterm = true;
    table->data[223].data[6].nterm = NT_OPTIONAL_FOR_STEP;
    table->data[223].data[7].term = T_DO;
    table->data[223].data[8].is_nterm = true;
    table->data[223].data[8].nterm = NT_STATEMENT_LIST;
    table->data[223].data[9].term = T_END;
    table->data[141] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[141].data[0].term = T_COMMA;
    table->data[141].data[1].term = T_EXPRESSION;
    table->data[145] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[142] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[3] = (exp_list_t){ .valid = true, .size = 4, .data = alloc_tokens(4) };
    table->data[3].data[0].term = T_REPEAT;
    table->data[3].data[1].is_nterm = true;
    table->data[3].data[1].nterm = NT_STATEMENT_LIST;
    table->data[3].data[2].term = T_UNTIL;
    table->data[3].data[3].term = T_EXPRESSION;
    table->data[85] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[85].data[0].term = T_LOCAL;
    table->data[85].data[1].is_nterm = true;
    table->data[85].data[1].nterm = NT_IDENTIFIER_WITH_TYPE;
    table->data[85].data[2].is_nterm = true;
    table->data[85].data[2].nterm = NT_DECL_OPTIONAL_ASSIGNMENT;
    table->data[390] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[390].data[0].term = T_EQUALS;
    table->data[390].data[1].term = T_EXPRESSION;
    table->data[419] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[422] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[389] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[415] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[405] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[385] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[420] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[401] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[395] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[418] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[394] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[410] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[414] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[27] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[27].data[0].term = T_IDENTIFIER;
    table->data[27].data[1].term = T_COLON;
    table->data[27].data[2].term = T_TYPE;
    table->data[107] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[107].data[0].is_nterm = true;
    table->data[107].data[0].nterm = NT_IDENTIFIER_LIST;
    table->data[107].data[1].term = T_EQUALS;
    table->data[107].data[2].is_nterm = true;
    table->data[107].data[2].nterm = NT_EXPRESSION_LIST;
    table->data[283] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[283].data[0].term = T_IDENTIFIER;
    table->data[283].data[1].is_nterm = true;
    table->data[283].data[1].nterm = NT_IDENTIFIER_LIST2;
    table->data[397] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[397].data[0].term = T_COMMA;
    table->data[397].data[1].term = T_IDENTIFIER;
    table->data[397].data[2].is_nterm = true;
    table->data[397].data[2].nterm = NT_IDENTIFIER_LIST2;
    table->data[374] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[398] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[293] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[293].data[0].term = T_EXPRESSION;
    table->data[293].data[1].is_nterm = true;
    table->data[293].data[1].nterm = NT_EXPRESSION_LIST2;
    table->data[77] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[77].data[0].term = T_COMMA;
    table->data[77].data[1].term = T_EXPRESSION;
    table->data[77].data[2].is_nterm = true;
    table->data[77].data[2].nterm = NT_EXPRESSION_LIST2;
    table->data[83] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[86] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[53] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[79] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[69] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[49] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[84] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[65] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[59] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[82] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[58] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[74] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[78] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[90] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[90].data[0].term = T_RETURN;
    table->data[90].data[1].is_nterm = true;
    table->data[90].data[1].nterm = NT_RET_EXPRESSION_LIST;
    table->data[165] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[165].data[0].term = T_EXPRESSION;
    table->data[165].data[1].is_nterm = true;
    table->data[165].data[1].nterm = NT_RET_EXPRESSION_LIST2;
    table->data[269] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[269].data[0].term = T_COMMA;
    table->data[269].data[1].term = T_EXPRESSION;
    table->data[269].data[2].is_nterm = true;
    table->data[269].data[2].nterm = NT_RET_EXPRESSION_LIST2;
    table->data[275] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[278] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[245] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[271] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[261] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[241] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[276] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[257] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[251] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[274] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[250] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[266] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[270] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[411] = (exp_list_t){ .valid = true, .size = 4, .data = alloc_tokens(4) };
    table->data[411].data[0].term = T_IDENTIFIER;
    table->data[411].data[1].term = T_LPAREN;
    table->data[411].data[2].is_nterm = true;
    table->data[411].data[2].nterm = NT_OPTIONAL_FUN_EXPRESSION_LIST;
    table->data[411].data[3].term = T_RPAREN;
    table->data[430] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[21] = (exp_list_t){ .valid = true, .size = 2, .data = alloc_tokens(2) };
    table->data[21].data[0].term = T_EXPRESSION;
    table->data[21].data[1].is_nterm = true;
    table->data[21].data[1].nterm = NT_FUN_EXPRESSION_LIST2;
    table->data[25] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[14] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[173] = (exp_list_t){ .valid = true, .size = 3, .data = alloc_tokens(3) };
    table->data[173].data[0].term = T_COMMA;
    table->data[173].data[1].term = T_EXPRESSION;
    table->data[173].data[2].is_nterm = true;
    table->data[173].data[2].nterm = NT_FUN_EXPRESSION_LIST2;
    table->data[185] = (exp_list_t){ .valid = true, .size = 0 };
    table->data[174] = (exp_list_t){ .valid = true, .size = 0 };
    return E_OK;
}
void parser_free()
{
    free(table);
    free(mempool.data);
}
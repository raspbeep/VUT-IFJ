# derived from build_grammar for precedence table

from typing import Dict, List, Set, Callable, Any, Tuple
import subprocess
import json
import sys

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError


def add_unique_to_list(in_list: List[str], source: List[str]):
    for s in source:
        if s not in in_list:
            in_list.append(s)


keywords = ['if', 'else', 'do', 'end', 'function', 'global', 'nil', 'require', 'return', 'while', 'then', '#integer',
            '#number', 'local', 'and', 'or', 'not']


def get_token_name(token):

    if token == EPS:
        print('Warn: get_token_name on EPS')
        return 'EPS'
    elif token == '- (unary)':
        return 'T_MINUS_UNARY'
    # elif token in keywords:
    #    return 'TOKEN_KW_' + token.replace('-', '_').upper()
    elif token[0] == '<' and token[-1] == '>':
        tokensubstr = token[1:-1]
        # if tokensubstr in keywords:
        #    return 'TOKEN_KW_' + tokensubstr.replace('-', '_').upper()
        # else:
        return 'T_' + tokensubstr.replace('-', '_').upper()
    else:
        d = {
            '(': 'LPAREN',
            ')': 'RPAREN',
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'ASTERISK',
            '/': 'SLASH',
            '%': 'PERCENT',
            '^': 'CARET',
            '//': 'DOUBLE_SLASH',
            '=': 'EQUALS',
            '~=': 'TILDE_EQUALS',
            '..': 'DOUBLE_DOT',
            '#': 'HASH',
            ':': 'COLON',
            '<': 'LT',
            '>': 'GT',
            '<=': 'LTE',
            '>=': 'GTE',
            '==': 'DOUBLE_EQUALS',
            ',': 'COMMA',
            '$': 'EOF'
        }
        return 'T_' + d.get(token, token.upper())


def load_config() -> Dict[str, Any]:
    with open('parser-config.json') as f:
        return json.loads(f.read())


def output_table_c(table: Dict[str, Dict[str, List[str]]], source_fname: str, header_fname: str):
    def is_nterm(token):
        return token[0] == '<' and token[-1] == '>' and token not in ['<type>', '<integer>', '<number>', '<identifier>', '<string>']

    # hash function and mod found with `bruteforce_hash.py`
    def hash_nt(nti, ti):
        return ((nti << shift) + ti) % mod

    def hash_t(nti, ti):
        return ((ti << shift) + nti) % mod

    config = load_config()
    mod = config['mod']
    nts = config['nts']
    ts = config['ts']
    shift = config['shift']
    nt_main = config['nt-main']
    hashf = hash_nt if nt_main else hash_t

    total_exp_len = sum(sum(len(exp) for exp in expd.values() if exp != [EPS]) for nterm, expd in table.items())

    # generate source file
    with open(source_fname, 'w') as f:
        f.write(f'/*\n * This file was generated by {sys.argv[0]}, DO NOT MODIFY!\n */\n')
        f.write( '#include <stdio.h>\n')
        f.write( '#include <stdlib.h>\n')
        f.write( '#include <stdbool.h>\n\n')
        f.write( '#include "parser-syn.h"\n')
        f.write( '#include "error.h"\n\n')
        f.write( 'const nterm_type_t parser_starting_nterm = NT_PROGRAM;\n')
        f.write( 'parser_table_t *table;\n\n')
        f.write( 'static struct {\n')
        f.write( '    void *data;\n')
        f.write( '    size_t size;\n')
        f.write( '    size_t offset;\n')
        f.write( '} mempool;\n\n')
        f.write( 'static void *alloc_tokens(size_t n_tokens)\n')
        f.write( '{\n')
        f.write( '    void *ret = (uint8_t *) mempool.data + mempool.offset;\n')
        f.write( '    mempool.offset += n_tokens * sizeof(token_type_t);\n')
        f.write( '    return ret;\n')
        f.write( '}\n')
        f.write( 'size_t parser_get_table_index(nterm_type_t nterm, term_type_t term)\n{\n    ')
        if nt_main:
            f.write(f'    return ((nterm << {shift}) + term) % {mod};\n')
        else:
            f.write(f'    return ((term << {shift}) + nterm) % {mod};\n')
        f.write( '}\n')

        # generate pretty-print functions for tokens
        f.write('const char *nterm_to_readable(nterm_type_t nterm)\n{\n')
        f.write('    switch(nterm) {\n')
        for i, nterm in enumerate(nts):
            token_name = get_token_name(nterm)
            f.write(f'        case NT_{token_name}: return "{nterm}";\n')
        f.write('    }\n}\n')

        f.write('const char *term_to_readable(nterm_type_t term)\n{\n')
        f.write('    switch(term) {\n')
        for i, term in enumerate(ts):
            token_name = get_token_name(term)
            f.write(f'        case T_{token_name}: return "{term}";\n')
        f.write('    }\n}\n')

        f.write( 'int parser_init()\n{\n')
        f.write(f'    mempool.data = calloc({total_exp_len}, sizeof(token_type_t));\n')
        f.write( '    if(mempool.data == NULL) {\n')
        f.write( '        return E_INT;\n')
        f.write( '    }\n')
        f.write(f'    mempool.size = {total_exp_len} * sizeof(token_type_t);\n\n')
        f.write(f'    size_t rule_count = {mod};\n')
        f.write( '    table = calloc(1, sizeof(parser_table_t) + rule_count * sizeof(exp_list_t));\n')
        f.write( '    if(table == NULL) {\n')
        f.write( '        return E_INT;\n')
        f.write( '    }\n\n')
        f.write( '    table->bucket_count = rule_count;')

        index_set = set()
        for nterm, expd in table.items():
            for term, exp in expd.items():

                nti = nts.index(nterm)
                ti = ts.index(term)
                table_ix = hashf(nti, ti)
                if table_ix in index_set:
                    print(f'error: index {table_ix} occurs multiple times')
                index_set.add(table_ix)

                # epsilon expansion
                if exp == [EPS]:
                    f.write(f'    table->data[{table_ix}] = (exp_list_t){{ .valid = true, .size = 0 }};\n')
                    continue

                f.write(f'    table->data[{table_ix}] = (exp_list_t){{ .valid = true, .size = {len(exp)}, .data = alloc_tokens({len(exp)}) }};\n')

                for i, token in enumerate(exp):
                    token_name = get_token_name(token)
                    if is_nterm(token):
                        f.write(f'    table->data[{table_ix}].data[{i}].is_nterm = true;\n')
                        f.write(f'    table->data[{table_ix}].data[{i}].nterm = NT_{token_name};\n')
                    else:
                        f.write(f'    table->data[{table_ix}].data[{i}].term = T_{token_name};\n')
        f.write('}\n')

        f.write('void parser_free()\n{\n')
        f.write('    free(table);\n')
        f.write('    free(mempool.data);\n')
        f.write('}\n')

    with open(header_fname, 'w') as f:
        f.write(f'/*\n * This file was generated by {sys.argv[0]}, DO NOT MODIFY!\n */\n')
        f.write( '#pragma once\n\n')
        f.write( '// order of these two enums is crucial\n')
        f.write('typedef enum {\n')
        for nterm in nts:
            token_name = get_token_name(nterm)
            f.write(f'    NT_{token_name},\n')
        f.write('} nterm_type_t;\n\n')

        f.write('typedef enum {\n')
        for term in ts:
            token_name = get_token_name(term)
            f.write(f'    T_{token_name},\n')
        f.write('} term_type_t;\n')

EPS = 'ε'
starting_symbol = '<program>'

# rules is a dict connecting non-terminals (head) to possible derivations (grammar strings)
# list of python strings is considered a grammar string
rules: Dict[str, List[List[str]]] = {
    '<program>': [['require', '<string>', '<global-statement-list>']],
    '<global-statement-list>': [['<global-statement>', '<global-statement-list>'], [EPS]],
    '<global-statement>': [['<func-decl>'], ['<func-def>'], ['<identifier>', '(', '<optional-expression-list>', ')']],

    '<func-decl>': [['global', '<identifier>', ':', 'function', '(', '<type-list>', ')', '<func-type-list>']],
    '<type-list>': [['<type>', '<type-list2>'], [EPS]],
    '<type-list2>': [[',', '<type-list2>'], [EPS]],
    '<func-def>': [
        ['function', '<identifier>', '(', '<identifier-list-with-types>', ')', '<func-type-list>', '<statement-list>',
         'end']],
    '<identifier-list-with-types>': [['<identifier-with-type>', '<identifier-list-with-types2>'], [EPS]],
    '<identifier-list-with-types2>': [[',', '<identifier-with-type>', '<identifier-list-with-types2>'], [EPS]],
    '<func-type-list>': [[':', '<type>', '<func-type-list2>'], [EPS]],
    '<func-type-list2>': [[',', '<type>', '<func-type-list2>'], [EPS]],

    '<statement-list>': [['<statement>', '<statement-list>'], [EPS]],
    '<statement>': [['<cond-statement>'], ['<while-loop>'], ['<for-loop>'], ['<repeat-until>'], ['<declaration>'],
                    ['<assignment>'], ['<return-statement>'], ['break']],

    '<cond-statement>': [['if', '<expression>', 'then', '<statement-list>', '<cond-opt-elseif>']],
    '<cond-opt-elseif>': [['elseif', '<expression>', 'then', '<cond-opt-elseif>'], ['else', '<statement-list>', 'end'],
                          ['end']],
    '<while-loop>': [['while', '<expression>', 'do', '<statement-list>', 'end']],
    '<for-loop>': [
        ['for', '<identifier>', '=', '<number>', ',', '<expression>', '<optional-for-step>', 'do', '<statement-list>',
         'end']],
    '<optional-for-step>': [[',', '<expression>'], [EPS]],
    '<repeat-until>': [['repeat', '<statement-list>', 'until', '<expression>']],

    '<declaration>': [['local', '<identifier-with-type>', '<decl-optional-assignment>']],
    '<decl-optional-assignment>': [['=', '<expression>'], [EPS]],
    '<identifier-with-type>': [['<identifier>', ':', '<type>']],

    '<assignment>': [['<identifier-list>', '=', '<expression-list>']],
    '<identifier-list>': [['<identifier>', '<identifier-list2>']],
    '<identifier-list2>': [[',', '<identifier>', '<identifier-list2>'], [EPS]],

    '<return-statement>': [['return', '<expression>']],

    '<expression-list>': [['<expression>', '<expression-list2>']],
    '<expression-list2>': [[',', '<expression>', '<expression-list2>'], [EPS]],
    '<optional-expression-list>': [['<expression>', '<expression-list2>'], [EPS]],

    '<optional-parenthesized-expression-list>': [['(', '<expression-list>', ')'], [EPS]],
}

precedence_rules = {
    '<unop>': [['-'], ['#'], ['not']],
    '<binop>': [['+'], ['-'], ['*'], ['/'], ['//'], ['%'], ['^'], ['..'], ['and'], ['or'], ['<'], ['<='], ['>'], ['>='],
                ['=='], ['~=']],
    '<expression>': [['<term>'], ['<term>', '<binop>', '<expression>']],
    '<term>': [['<factor>'], ['<unop>', '<term>']],
    '<factor>': [['<integer>'], ['<number>'], ['<string>'], ['nil'], ['<identifier>'], ['(', '<expression>', ')']],
}

for head, production in precedence_rules.items():
    rules[head] = production


terminals: List[str] = list({
    token
    for exps in rules.values()
    for exp in exps
    for token in exp
    if token not in rules
})

non_terminals: List[str] = list(rules.keys())

add_unique_to_list(non_terminals, list(precedence_rules.keys()))

for productions in precedence_rules.values():
    for production in productions:
        for token in production:
            if token not in non_terminals:
                add_unique_to_list(terminals, [token])

def check_rules(rules, show_eps = False):

    for head, productions in rules.items():
        if productions[0] == head:
            print("Note: ", head, " is left recursive")

    factors = {}
    for head, productions in rules.items():
        max_count = 0
        for p in productions:
            count = 0
            for o in productions:
                if len(o) > 0 and len(p) > 0:
                    if o[0] == p[0]:
                        count += 1
            if count > max_count:
                max_count = count
        factors[head] = max_count

    for head, count in factors.items():
        if count > 1:
            print("Note: ", head, " can be factorized (", count, "occurences)")

    if show_eps:
        for head, productions in rules.items():
            for p in productions:
                if p == [EPS]:
                    print("Note: ", head, " is epsilon production")


def rules_left_factor(rules):
    new_rules = {}
    for head, productions in rules.items():
        print("Checking ", head)
        for p in productions:
            print("Production: ", p)
            common = None
            lf_list = []
            for i in range(0, len(p)):
                count = 0
                plist = p[:len(p) - i]
                print("Plist: ", plist)
                for o in productions:
                    print("Against ", o[:len(p) - i])
                    if plist == o[:len(p) - i]:
                        count += 1
                        if count > 1:
                            print("Can be factored")
                            common = plist
                            lf_list.append(o[len(p) - i:])
                            break
                if count > 1:
                    break
            if common:
                print("Factoring to ", common)
                for lf in lf_list:
                    print(lf)

    return new_rules


def rules_remove_eps_production(rules):
    new_rules = rules

    def find_eps_production():
        for head, productions in new_rules.items():
            for production in productions:
                if production == [EPS]:
                    return head
        return None

    def build_variation(in_list: List[List[str]], s):
        out_list: List[List[str]] = []
        variation = [s]
        if s == eps_nt:
            variation.append('')
        for s in variation:
            for production in in_list:
                c = production.copy()
                if s != '':
                    c.append(s)
                if c not in out_list:
                    out_list.append(c)
        return out_list

    def create_productions(dest, production):
        variations: List[List[str]] = [[]]
        for s in production:
            variations = build_variation(variations, s)
        for r in variations:
            dest.append(r)

    def remove_eps_production(in_rules):
        in_rules[eps_nt].remove([EPS])
        out_rules = {}
        for head, productions in in_rules.items():
            out_rules[str(head)] = []
            for production in productions:
                create_productions(out_rules[str(head)], production)
        return out_rules

    while eps_nt := find_eps_production():
        new_rules = remove_eps_production(new_rules)

    return new_rules


empty_set: Dict[str, List[str]] = {}
first_set: Dict[str, List[str]] = {}
follow_set: Dict[str, List[str]] = {}
predict = {}
rule_list = []
precedence_table = {}
Associativity = Enum(["LEFT", "RIGHT"])


def create_table():

    print("Non terminals:", file=sys.stderr)
    for nt in non_terminals:
        print("  ", nt, file=sys.stderr)
    print("Terminals:", file=sys.stderr)
    for t in terminals:
        print("  ", t, file=sys.stderr)

    def get_productions_containing(symbol):
        out_list = []
        for head, productions in rules.items():
            for production in productions:
                if symbol in production:
                    out_list.append((head, production))
        return out_list

    def symbol_derives_to_eps(s):
        if s in non_terminals:
            for production in rules[s]:
                for p in production:
                    if not symbol_derives_to_eps(p):
                        return False
            return True
        else:
            return s == EPS

    def derives_to_eps(production):
        for s in production:
            if not symbol_derives_to_eps(s):
                return False
        return True

    for head, productions in rules.items():
        is_empty = False
        for p in productions:
            if derives_to_eps(p):
                is_empty = True
                break
        if is_empty:
            empty_set[head] = [EPS]

    print("Empty: ", list(empty_set.keys()), file=sys.stderr)

    def add_first_symbols(first, symbol):
        if symbol in non_terminals:
            for production in rules[symbol]:
                for s in production:
                    if s not in empty_set:
                        add_first_symbols(first, s)
                        break
        elif symbol != EPS:
            first.append(symbol)

    for t in terminals:
        first_set[t] = [t]

    def create_first(in_list: List[str], symbol):
        if symbol in terminals:
            add_unique_to_list(in_list, [symbol])
        else:
            for production in rules[symbol]:
                for p in production:
                    vars = []
                    create_first(vars, p)
                    add_unique_to_list(in_list, vars)
                    if p not in empty_set.keys():
                        break

    for head, productions in rules.items():
        first_set[head] = []
        create_first(first_set[head], head)
        print("First ", head, ": ", first_set[head], file=sys.stderr)

    for head, productions in rules.items():
        follow_set[head] = []
    follow_set[starting_symbol].append('$')

    def create_follow_from_production(phead, production, pos):
        out_list = []
        epsilon_production = True
        for i in range(pos + 1, len(production)):
            for s in first_set[production[i]]:
                if s != EPS:
                    out_list.append(s)
            if production[i] not in empty_set.keys():
                epsilon_production = False
                break
        if epsilon_production:
            out_list += follow_set[phead]
        return out_list

    for head in rules.keys():
        for phead, production in get_productions_containing(head):
            for i in range(0, len(production)):
                if production[i] == head:
                    temp = create_follow_from_production(phead, production, i)
                    add_unique_to_list(follow_set[head], temp)

    for head in rules.keys():
        print("Follow (", head, "):", follow_set[head], file=sys.stderr)

    def empty(x):
        return derives_to_eps(x)

    def first(x):
        out_list = []
        for p in x:
            vars = []
            create_first(vars, p)
            add_unique_to_list(out_list, vars)
            if p not in empty_set.keys():
                break
        return out_list

    for head, productions in rules.items():
        for p in productions:
            rule_list.append((head, p))

    for i, (head, production) in enumerate(rule_list):
        print("rule", i, ": (", head, "->", production, ")", file=sys.stderr)

    for i, (head, production) in enumerate(rule_list):
        predict[i] = []
        add_unique_to_list(predict[i], first(production))
        if empty(production):
            add_unique_to_list(predict[i], follow_set[head])
        print("Predict(", i, "):", predict[i], file=sys.stderr)

    terminals.remove(EPS)
    terminals.append('$')
    check_rules(rules)


def get_priority(t):
    d = {
        **dict.fromkeys(['^'], 7),
        **dict.fromkeys(['not', '- (unary)', '#'], 7),
        **dict.fromkeys(['*', '/', '//', '%'], 6),
        **dict.fromkeys(['+', '-'], 5),
        **dict.fromkeys(['..'], 4),
        **dict.fromkeys(['<', '>', '<=', '>=', '~=', '=='], 3),
        **dict.fromkeys(['and'], 2),
        **dict.fromkeys(['or'], 1),
        ** dict.fromkeys(['$'], -1)
    }
    return d.get(t, 0)


symbol_lt = '⋖'
symbol_gt = '⋗'
symbol_eq = '≐'

binops = [
    '+', '-', '*', '/', '//', '%', '^', '..', 'and', 'or', '<', '<=',
    '>', '>=',
    '==', '~='
]

unops = [
    '- (unary)', '#', 'not'
]

def generate_precedence():
    opterminals = binops + unops + [
        '$',
        '(',
        ')'
    ]

    print("opterminals ", opterminals)

    assoc = {
        Associativity.LEFT:  [ '*', '/', '%', '//', '+', '-', '<', '>', '<=', '>=', '~=', '==', 'and', 'or'],
        Associativity.RIGHT: ['not', '- (unary)', '^', '..', '#']
    }

    def get_productions_containing(symbol):
        out_list = []
        for head, productions in precedence_rules.items():
            for production in productions:
                if symbol in production:
                    out_list.append((head, production))
        return out_list

    def filtered(in_list):
        out_list = []
        for s in in_list:
            if s in opterminals or s in ['(', ')', '$']:
                out_list.append(s)
        return out_list

    def is_left_associative(t):
        return t in assoc[Associativity.LEFT]

    def is_right_associative(t):
        return t in assoc[Associativity.RIGHT]

    def get_symbols_before(production, pos):
        out_list = []
        for i in reversed(range(0, pos)):
            if production[i] in non_terminals:
                add_unique_to_list(out_list, first_set[production[i]])
                if production[i] not in empty_set.keys():
                    break
            else:
                out_list.append(production[i])
        return out_list

    def symbol_can_precede(symbol, out_list):
        rlist = get_productions_containing(symbol)
        for (head, production) in rlist:
            for i, s in enumerate(production):
                if s == symbol:
                    sym = get_symbols_before(production, i)
                    add_unique_to_list(out_list, sym)
                    if len(sym) == 0:
                        symbol_can_precede(head, out_list)

    def get_symbols_after(production, pos):
        out_list = []
        for i in range(pos + 1, len(production)):
            if production[i] in non_terminals:
                print("Unhanled! Is NT")
            else:
                out_list.append(production[i])
        return out_list

    def symbol_can_succeed(symbol, out_list):
        print("SCS: ", symbol)
        rlist = get_productions_containing(symbol)
        for (head, production) in rlist:

            for i, s in enumerate(production):
                if s == symbol:
                    sym = get_symbols_after(production, i)
                    print("Sym", symbol, "at pos", i, ": ", sym)
                    add_unique_to_list(out_list, filtered(sym))
                    if len(sym) == 0:
                        print("After ", head, ": ", filtered(follow_set[head]))
                        add_unique_to_list(out_list, filtered(follow_set[head]))

    for t in opterminals:
        print("Priority of", t, " ", get_priority(t))

    parenthesis_precede = ['$']
    symbol_can_precede('(', parenthesis_precede)
    print("Symbols can precede (: ", parenthesis_precede)

    parenteses_succeed = ['$']
    symbol_can_succeed(')', parenteses_succeed)
    print("Symbols can succeed ): ", parenteses_succeed)

    identifier_precede = ['$']
    symbol_can_precede('<identifier>', identifier_precede)
    print("Symbols can precede i: ", identifier_precede)

    identifier_succeed = ['$']
    symbol_can_succeed('<identifier>', identifier_succeed)
    print("Symbols can succeed i: ", identifier_succeed)

    terminals_identifiers = [
                    '<identifier>',
                    '<integer>',
                    '<number>',
                    '<string>',
                    '<bool>',
                    '<nil>']

    for i in terminals_identifiers:
        opterminals.append(i)

    for t in opterminals:
        precedence_table[t] = {}
    for op1 in opterminals:
        p1 = get_priority(op1)
        for op2 in opterminals:
            p2 = get_priority(op2)
            if op1 in unops and op2 in terminals_identifiers:
                precedence_table[op1][op2] = symbol_lt
            elif op1 in terminals_identifiers:
                if op2 in identifier_succeed:
                    precedence_table[op1][op2] = symbol_gt
            elif op2 in terminals_identifiers:
                if op1 in identifier_precede:
                    precedence_table[op1][op2] = symbol_lt
            elif op1 == '(' and op2 == ')':
                precedence_table[op1][op2] = symbol_eq
            elif op1 == '(':
                if op2 not in [')', '$']:
                    precedence_table[op1][op2] = symbol_lt
            elif op2 == ')':
                if op1 not in ['(', '$']:
                    precedence_table[op1][op2] = symbol_gt
            elif op1 in parenthesis_precede and op2 == '(':
                precedence_table[op1][op2] = symbol_lt
            elif op1 == ')' and op2 in parenteses_succeed:
                precedence_table[op1][op2] = symbol_gt
            elif p1 > p2:
                precedence_table[op1][op2] = symbol_gt
            elif p1 < p2:
                precedence_table[op1][op2] = symbol_lt
            else:
                if is_left_associative(op1) and is_left_associative(op2):
                    precedence_table[op1][op2] = symbol_gt
                elif is_right_associative(op1) and is_right_associative(op2):
                    precedence_table[op1][op2] = symbol_lt


def prec_keys_order():
    return sorted(list(precedence_table.keys()), key=lambda i: get_priority(i), reverse=True)


def generate_xlsx():
    if xlsxwriter is None:
        print('Error: xlsxwriter not loaded', file=sys.stderr)
        return

    workbook = xlsxwriter.Workbook('rules.xlsx')
    worksheet = workbook.add_worksheet("One")

    row = 0
    col = 0
    longest = 0
    for i, (head, production) in enumerate(rule_list):
        cell = "rule" + str(i + 1) + ": (" + str(head) + " -> " + str(production) + ")"
        worksheet.write(row + i + 1, col, cell)
        if len(cell) > longest:
            longest = len(cell)
    worksheet.set_column(row, col, longest * 1.6)

    row = 1
    col = 1
    for i, t in enumerate(terminals):
        worksheet.write(row, col + i + 1, str(t))
    for i, nt in enumerate(non_terminals):
        worksheet.write(row + i + 1, col, nt)
        for j, (head, production) in enumerate(rule_list):
            if head == nt:
                for k, t in enumerate(terminals):
                    if t in predict[j]:
                        worksheet.write(row + i + 1, col + k + 1, j + 1)
    workbook.close()



def generate_xlsx_prec():
    if xlsxwriter is None:
        print('xlsxwriter not loaded', file=sys.stderr)
        return

    workbook = xlsxwriter.Workbook('rules.xlsx')
    worksheet = workbook.add_worksheet("Precedence")

    def key_format(s):
        return '\'' + s + '\''

    longest = 0
    for key in precedence_table.keys():
        if len(key_format(key)) > longest:
            longest = len(key_format(key))

    col = 1
    row = 1
    worksheet.set_column(col, col, longest * 1.1)
    for i, key in enumerate(prec_keys_order()):
        worksheet.write(row, col + i + 1, key_format(key))
        worksheet.set_column(col + i + 1, col + i + 1, longest * 1.1)
    row += 1
    for i, key in enumerate(prec_keys_order()):
        values = precedence_table[str(key)]
        worksheet.write(row + i, col, key_format(key))
        for j, col_key in enumerate(prec_keys_order()):
            if col_key in list(values.keys()):
                worksheet.write(row + i, col + j + 1, values[col_key])

    workbook.close()


def indent(amount):
    indent_str = ''
    for i in range(0, amount):
        indent_str += '    '
    return indent_str


def generate_files(source_path: str, header_path: str):
    def get_rules_for_nterm(nt):
        out_list = {}
        for i, (head, production) in enumerate(rule_list):
            if head == nt:
                for t in terminals:
                    if t in predict[i]:
                        if i not in out_list.keys():
                            out_list[i] = [production, [t]]
                        else:
                            out_list[i][1].append(t)
        return out_list

    proto_arguments = 'parse_tree_t *ptree'
    proto_call = 'ptree'
    token_var = 'token'
    return_type = 'bool'
    func_next_token = 'get_next_token()'

    def proto(nt):
        return return_type + ' ' + rule_func_name(nt) + '(' + proto_arguments + ')'

    def rule_func_name(nt):
        return 'RULE_' + get_token_name(nt)

    def proc_create_node(f, nt, i):
        #f.write(indent(i) + 'ptree = calloc(1, sizeof(parse_tree_t));\n')
        #f.write(indent(i) + 'if (!ptree) { //E_INT\n')
        #f.write(indent(i + 1) + 'return false;\n')
        #f.write(indent(i) + '}\n')
        f.write(indent(i) + 'ptree->type = (token_type_t){ .is_nterm = true, .nterm = ' + get_token_name(nt) + ' };\n')

    def proc_get_next_token(f, i):
        f.write(indent(i) + 'if (' + func_next_token + ' != E_OK) {\n')
        f.write(indent(i + 1) + 'return false;')
        f.write(indent(i) + '}\n')

    def proc_alloc_tree_children(f, i, amount):
        f.write(indent(i) + f'ptree->children = calloc({amount}, sizeof(parse_tree_t));\n')
        f.write(indent(i) + '//printf("alloc at %s\\n", nterm_to_string(nterm));\n')
        f.write(indent(i) + 'if (!ptree->children) {\n')
        f.write(indent(i + 1) + 'return false; //E_INT\n')
        f.write(indent(i) + '}\n')
        f.write(indent(i) + f'ptree->length = {amount};\n')

    with open(header_path, 'w') as f:
        f.write(f'/*\n * The contents of this file were generated by a {sys.argv[0]} tool.\n */\n')
        f.write('#pragma once\n\n')

        f.write('typedef enum {\n')
        for nt in non_terminals:
            f.write(indent(1) + get_token_name(nt) + ',\n')
        f.write('} nterm_type_t;\n\n')

        f.write('typedef enum {\n')
        for t in terminals:
            f.write(indent(1) + get_token_name(t) + ',\n')
        f.write('} term_type_t;\n')

        f.write('const char *nterm_to_string(nterm_type_t nterm);')
        f.write('const char *term_to_string(term_type_t term);')

    with open('src/experimental-enum.c', 'w') as f:
        f.write('#include "experimental-enum.h"\n')
        # generate pretty-print functions for tokens
        f.write('const char *nterm_to_string(nterm_type_t nterm)\n{\n')
        f.write(indent(1) + 'switch(nterm) {\n')
        for i, nterm in enumerate(non_terminals):
            f.write(indent(2) + f'case {get_token_name(nterm)}: return "{nterm}";\n')
        f.write(indent(1) + '}\n}\n')

        f.write('const char *term_to_string(term_type_t term)\n{\n')
        f.write(indent(1) + 'switch(term) {\n')
        for i, term in enumerate(terminals):
            f.write(indent(2) + f'case {get_token_name(term)}: return "{term}";\n')
        f.write(indent(1) + '}\n}\n')

    with open(source_path, 'w') as f:
        f.write(f'/*\n * The contents of this file were generated by a {sys.argv[0]} tool.\n */\n')
        f.write('#include "experimental.h"\n')
        f.write('#include <stdlib.h>\n')
        f.write('#include <stdbool.h>\n\n')

        for nt in non_terminals:
            f.write(proto(nt) + ';\n')
        f.write('\n')

        for nt in non_terminals:
            f.write(proto(nt) + ' {\n')

            proc_create_node(f, nt, 1)

            subroutines = get_rules_for_nterm(nt)
            if_index = 0
            for i, (subroutine, terms) in subroutines.items():
                f.write(indent(1))
                if if_index != 0:
                    f.write('else ')
                f.write('if (')
                if_index += 1
                for t_index, t in enumerate(terms):
                    if t_index != 0:
                        f.write(' || ')
                    f.write(f'{token_var}.type == {get_token_name(t)}')
                f.write(') {\n')

                #proc_create_node(f, nt, 1)

                accepted_token = False
                if len(subroutine) > 0 and subroutine[0] in terminals:
                    accepted_token = True

                # proc_create_node(f, nt, 2)
                if len(subroutine) > 0 and subroutine[0] not in non_terminals:
                    subroutine = subroutine[1:]

                nt_count = 0
                for s in subroutine:
                    if s in non_terminals:
                        nt_count += 1
                if nt_count > 0:
                    #f.write(indent(2) + '//append ' + str(nt_count) + ' children\n')
                    proc_alloc_tree_children(f, 2, nt_count)

                tree_index = 0
                for s in subroutine:
                    if accepted_token:
                        proc_get_next_token(f, 2)
                        accepted_token = False
                    if s in terminals:
                        f.write(indent(2) + f'if ({token_var}.type != {get_token_name(s)})\n')
                        f.write(indent(2) + '{\n')
                        f.write(indent(3) + 'return false; //E_SYN\n')
                        f.write(indent(2) + '}\n')
                    else:
                        f.write(indent(2) + f'if ({rule_func_name(s)}(&ptree->children[{tree_index}]) != true)\n')
                        f.write(indent(2) + '{\n')
                        f.write(indent(3) + 'return false; //E_SYN\n')
                        f.write(indent(2) + '}\n')
                        tree_index += 1
                if accepted_token:
                    proc_get_next_token(f, 2)
                    accepted_token = False
                f.write(indent(2) + 'return true;')

                f.write(indent(1) + '}\n')
            f.write(indent(1) + 'return false; //E_SYN\n')
            f.write('}\n\n')

        f.write('int parse_start(parse_tree_t *ptree) {\n')
        proc_get_next_token(f, 1)
        f.write(indent(1) + 'return ' + rule_func_name(starting_symbol) + '(ptree)? E_OK : E_INT;\n')
        f.write('}\n')


def value_to_precedence_enum_at(key, values):
    if key in list(values.keys()):
        d = {
            symbol_lt: 'PREC_LT',
            symbol_gt: 'PREC_GT',
            symbol_eq: 'PREC_EQ',
        }
        return d.get(values[key])
    return 'PREC_ZE'


def generate_precedence_files(path):
    table_size = len(precedence_table.keys())
    table_size_def = 'TABLE_SIZE'
    table_var = 'precedence_table'

    with open(path, 'w') as f:
        f.write('/* THIS FILE IS AUTO GENERATED */\n')
        f.write('#pragma once''\n')
        f.write('#include "parser-generated.h"\n')
        f.write('#include <stdint.h>\n')
        f.write('#include <stdbool.h>\n')

        f.write('typedef enum {\n')
        f.write(indent(1) + 'PREC_ZE = 0,\n')
        f.write(indent(1) + 'PREC_LT,\n')
        f.write(indent(1) + 'PREC_GT,\n')
        f.write(indent(1) + 'PREC_EQ,\n')
        f.write('} precedence_t;\n')

        f.write(f'#define {table_size_def} ({table_size})\n')
        f.write(f'#define T_MINUS_UNARY (420)\n')

        init_list = ''
        for i, row in enumerate(prec_keys_order()):
            init_list_row = ''
            values = precedence_table[row]
            for j, col_key in enumerate(prec_keys_order()):
                init_list_row += value_to_precedence_enum_at(col_key, values) + ', '
            init_list += '{' + init_list_row[:-2] + '},\n'

        f.write(f'const uint8_t {table_var}[{table_size_def}][{table_size_def}] = {{{init_list[:-2]}}}\n;\n')

        term_list = ''
        for key in prec_keys_order():
            term_list += get_token_name(key) + ', '
        f.write(f'const term_type_t precedence_terminals[] = {{{term_list[:-2]}}};\n')

        f.write('int term_to_index(term_type_t type) {\n')
        uix = -1
        for i, key in enumerate(prec_keys_order()):
            if key == '- (unary)':
                uix = i
                break

        f.write('if (type == T_MINUS_UNARY) {\n')
        f.write(f'return {uix};\n')
        f.write('}\n')

        f.write(indent(1) + 'switch (type) {\n')
        for i, key in enumerate(prec_keys_order()):
            if key != '- (unary)':
                f.write(indent(1) + f'case {get_token_name(key)}: return {i};\n')
        f.write(indent(1) + 'default: return -1;\n')
        f.write(indent(1) + '}\n')
        f.write('}\n')

        f.write('bool is_binary_op(term_type_t type) {\n')
        f.write(indent(1) + 'switch (type) {\n')
        for t in binops:
            f.write(indent(1) + f'case {get_token_name(t)}: return true;\n')
        f.write(indent(1) + 'default: return false;\n')
        f.write(indent(1) + '}\n')
        f.write('}\n')

        f.write('bool is_unary_op(term_type_t type) {\n')
        f.write('if (type == T_MINUS_UNARY) {\n')
        f.write('return true;\n')
        f.write('}\n')

        f.write(indent(1) + 'switch (type) {\n')
        for t in unops:
            if t != '- (unary)':
                f.write(indent(1) + f'case {get_token_name(t)}: return true;\n')
        f.write(indent(1) + 'default: return false;\n')
        f.write(indent(1) + '}\n')
        f.write('}\n')

        f.write('const char* term_to_string(term_type_t type) {\n')
        f.write('if (type == T_MINUS_UNARY) {\n')
        f.write('return "T_MINUS_UNARY";\n')
        f.write('}\n')
        f.write(indent(1) + 'switch (type) {\n')
        for i, key in enumerate(prec_keys_order()):
            if key != '- (unary)':
                f.write(indent(1) + f'case {get_token_name(key)}: return "{get_token_name(key)}";\n')
        f.write(indent(1) + 'default: return "N\\\\A";\n')
        f.write(indent(1) + '}\n')
        f.write('}\n')


if __name__ == '__main__':

    # calculate total amount of expansion rules and all the unique ones
    all_exp_rules: List[Tuple[str, ...]] = sum(([tuple(exp) for exp in exps] for exps in rules.values()), [])
    print(f'{len(all_exp_rules)} expansion rules ({len(set(all_exp_rules))} unique)', file=sys.stderr)
    print(f'terms: {len(terminals)}', file=sys.stderr)
    print(f'nonterms: {len(non_terminals)}', file=sys.stderr)

    if len(sys.argv) != 3:
        print(f'usage: {sys.argv[0]} src_file header_file', file=sys.stderr)
        exit(1)

    sys.stderr.write('Generating excel table...\n')
    create_table()

    # calculate total amount of expansion rules and all the unique ones
    all_exp_rules: List[Tuple[str, ...]] = sum(([tuple(exp) for exp in exps] for exps in rules.values()), [])
    print(f'\n{len(all_exp_rules)} expansion rules ({len(set(all_exp_rules))} unique)', file=sys.stderr)
    print(f'terms: {len(terminals)}', file=sys.stderr)
    print(f'nonterms: {len(non_terminals)}\n', file=sys.stderr)

    generate_precedence()

    src_file, header_file = sys.argv[1:3]
    sys.stderr.write('Generating files...\n')

    prec_path = '..//include//parser-precedence-table.h'

    generate_precedence_files(prec_path)
    generate_xlsx_prec()

    try:
        sys.stderr.write('Formatting files... ')
        subprocess.run(['clang-format', '--style=file', '-i', prec_path], check=True)
    except subprocess.CalledProcessError:
        print('failed to format files with `clang-format`', file=sys.stderr)
    else:
        sys.stderr.write('[OK]\n')

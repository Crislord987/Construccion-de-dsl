grammar DeepLearningDSL;

program         : statement* EOF;

// === STATEMENTS ===
statement       : assignment
                | expressionStatement
                | controlStructure
                | plotStatement
                | fileOperation
                | ';'
                ;

assignment      : ID '=' expression ';';
expressionStatement : expression ';';

// === CONTROL STRUCTURES ===
controlStructure
                : ifStatement
                | whileStatement
                ;

ifStatement     : 'if' booleanExpression 'then' statement* ('else' statement*)? 'fi';
whileStatement  : 'while' booleanExpression 'do' statement* 'done';

// === EXPRESSIONS ===
expression
    : expression op=('*'|'/') expression
    | expression op=('+'|'-') expression
    | expression op='^' expression
    | expression op=('==' | '!=' | '<' | '<=' | '>' | '>=') expression
    | '(' expression ')'
    | matrixLiteral
    | listLiteral
    | NUMBER
    | STRING
    | ID
    | matrixOperation
    | trigFunction
    | mlOperation
    | TRUE
    | FALSE 
    ;

booleanExpression
                : expression comparator expression
                | 'not' booleanExpression
                | booleanExpression ('and'|'or') booleanExpression
                ;

comparator      : '==' | '!=' | '<' | '<=' | '>' | '>=';

matrixOperation : 'transpose' '(' expression ')'
                | 'inverse' '(' expression ')'
                | 'matmul' '(' expression ',' expression ')'
                | 'matsum' '(' expression ',' expression ')'
                | 'matsub' '(' expression ',' expression ')'
                ;

mlOperation     : 'linearRegression' '(' expression ',' expression ')'
                | 'mlpClassifier' '(' expression ',' expression ',' expression ')'
                | 'kmeans' '(' expression ',' expression ')'
                ;

trigFunction    : 'sin' '(' expression ')'
                | 'cos' '(' expression ')'
                | 'tan' '(' expression ')'
                | 'sqrt' '(' expression ')'
                | 'log' '(' expression ')'
                | 'exp' '(' expression ')'
                ;

plotStatement   : 'plot' '(' expression ',' expression ')' ';'
                | 'scatter' '(' expression ',' expression ')' ';'
                | 'hist' '(' expression ')' ';'
                ;

fileOperation   : 'readFile' '(' expression ')' ';'
                | 'writeFile' '(' expression ',' expression ')' ';'
                ;

literal         : NUMBER
                | STRING
                | matrixLiteral
                | listLiteral
                ;
TRUE: 'true';
FALSE: 'false';

matrixLiteral   : '[' listLiteral (',' listLiteral)* ']';
listLiteral     : '[' (expression (',' expression)*)? ']';

// === TOKENS ===
ID              : [a-zA-Z_][a-zA-Z_0-9]*;
NUMBER          : '-'? DIGIT+ ('.' DIGIT+)?;
STRING          : '"' (~["])* '"';

fragment DIGIT  : [0-9];

WS              : [ \t\r\n]+ -> skip;
COMMENT         : '//' ~[\r\n]* -> skip;


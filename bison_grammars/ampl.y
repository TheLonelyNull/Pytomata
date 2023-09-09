%define lr.type canonical-lr

%token PROGRAM ID MAIN TAKES RETURNS BOOLEAN INTEGER STRING ARRAY CHILLAX
%token VARS AS END LET BACK DO IF ELIF ELSE INPUT OUTPUT WHILE
%token EQ GEQ GT LEQ LT NEQ OR AND TRUE FALSE MOD NUM NOT

%%

programN: PROGRAM ID ':' funcdefstar MAIN ':' body;
funcdefstar: funcdef funcdefstar
           |
           ;
semicolonvarseqstar: ';' varseq semicolonvarseqstar
                   |
                   ;
funcdef: ID ':' TAKES varseq semicolonvarseqstar RETURNS type body;
varsvarseqsemicolonvarseqstaroptional: VARS varseq semicolonvarseqstar
                                     |
                                     ;
body: varsvarseqsemicolonvarseqstaroptional statements;
commaidstar: ',' ID commaidstar
           |
           ;
varseq: ID commaidstar AS type;
boleanorinteger: BOOLEAN
               | INTEGER
               ;
arrayoptional: ARRAY
             |
             ;
type: boleanorinteger arrayoptional;

semicolonstatementstar: ';' statement semicolonstatementstar
                      | 
                      ;
statements: CHILLAX
           | statement semicolonstatementstar END;
statement: assign
         | backN
         | doN
         | ifN
         | inputN
         | outputN
         | whileN
         ;
bracketsimplebracketoptionall: '[' simple ']'
                             |
                             ;
exprorarraysimple: expr
                 | ARRAY simple
                 ;
assign: LET ID bracketsimplebracketoptionall '=' exprorarraysimple;
exproptional: expr
            | 
            ;
backN: BACK exproptional;
commaexprstar: ',' expr commaexprstar
             |
             ;
doN: DO ID '(' expr commaexprstar ')';
elifexprcolonstatementsstar: ELIF expr ':' statements elifexprcolonstatementsstar
                           |
                           ;
elsecolonstatementsoptional: ELSE ':' statements
                           |
                           ;
ifN: IF expr ':' statements elifexprcolonstatementsstar elsecolonstatementsoptional;
inputN: INPUT ID bracketsimplebracketoptionall;
stringexpr: STRING
          | expr
          ;
andstringexprstar:  '&' stringexpr andstringexprstar
                 |
                 ;
outputN: OUTPUT stringexpr andstringexprstar;
whileN: WHILE expr ':' statements;
reloporsimpleoptional: relop simple
                     |
                     ;
expr: simple reloporsimpleoptional;
relop: EQ 
     | GEQ 
     | GT 
     | LEQ
     | LT
     | NEQ
     ;
minusoptional: '-'
             |
             ;
addoptermstar: addop term addoptermstar
             |
             ;
simple: minusoptional term addoptermstar;
addop: '-'
     | OR
     | '+'
     ;
mulopfactorstar: mulop factor mulopfactorstar
               |
               ;
term: factor mulopfactorstar;
mulop: AND
     | '/'
     | '*'
     | MOD
     ;
bracksimpbrackexprcommaexprstaroptional: '[' simple ']'
                                       | '(' expr commaexprstar ')'
                                       |
                                       ;
factor: ID bracksimpbrackexprcommaexprstaroptional
      | NUM
      | '(' expr ')'
      | NOT factor
      | TRUE
      | FALSE
      ;

%%

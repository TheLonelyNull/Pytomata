%%

programN: 'program' 'id' ':' funcdefstar 'main' ':' body;
funcdefstar: funcdef funcdefstar
           |
           ;
semicolonvarseqstar: ';' varseq semicolonvarseqstar
                   |
                   ;
funcdef: 'id' ':' 'takes' varseq semicolonvarseqstar 'returns' type body;
varsvarseqsemicolonvarseqstaroptional: 'vars' varseq semicolonvarseqstar
                                     |
                                     ;
body: varsvarseqsemicolonvarseqstaroptional statements;
commaidstar: ',' 'id' commaidstar
           |
           ;
varseq: 'id' commaidstar 'as' type;
boleanorinteger: 'boolean'
               | 'integer'
               ;
arrayoptional: 'array'
             |
             ;
type: boleanorinteger arrayoptional;

semicolonstatementstar: ';' statement semicolonstatementstar
                      | 
                      ;
statements:'chillax'
           | statement semicolonstatementstar 'end';
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
                 | 'array' simple
                 ;
assign: 'let' 'id' bracketsimplebracketoptionall '=' exprorarraysimple;
exproptional: expr
            | 
            ;
backN: 'back' exproptional;
commaexprstar: ',' expr commaexprstar
             |
             ;
doN: 'do' 'id' '(' expr commaexprstar ')';
elifexprcolonstatementsstar: 'elif' expr ':' statements elifexprcolonstatementsstar
                           |
                           ;
elsecolonstatementsoptional: 'else' ':' statements
                           |
                           ;
ifN: 'if' expr ':' statements elifexprcolonstatementsstar elsecolonstatementsoptional;
inputN: 'input' 'id' bracketsimplebracketoptionall;
stringexpr: 'STRING'
          | expr
          ;
andstringexprstar:  '&' stringexpr andstringexprstar
                 |
                 ;
outputN: 'output' stringexpr andstringexprstar;
whileN: 'while' expr ':' statements;
reloporsimpleoptional: relop simple
                     |
                     ;
expr: simple reloporsimpleoptional;
relop: '='
     | '>='
     | '>'
     | '<='
     | '<'
     | '/='
     ;
minusoptional: '-'
             |
             ;
addoptermstar: addop term addoptermstar
             |
             ;
simple: minusoptional term addoptermstar;
addop: '-'
     | 'or'
     | '+'
     ;
mulopfactorstar: mulop factor mulopfactorstar
               |
               ;
term: factor mulopfactorstar;
mulop: 'and'
     | '/'
     | '*'
     | 'mod'
     ;
bracksimpbrackexprcommaexprstaroptional: '[' simple ']'
                                       | '(' expr commaexprstar ')'
                                       |
                                       ;
factor: 'id' bracksimpbrackexprcommaexprstaroptional
      | 'num'
      | '(' expr ')'
      | 'not' factor
      | 'true'
      | 'false'
      ;

%%
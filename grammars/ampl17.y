%%

initsymbol: programN
          ;

funcdefstar: |
             funcdef funcdefstar 
           ;

programN: 'program' id ':' funcdefstar 'main' ':' body
        ;

semicolonvarseqstar: |
                     ';' varseq semicolonvarseqstar 
                   ;

typeornothing: type |
               'nothing' 
             ;

funcdef: id ':' 'takes' varseq semicolonvarseqstar 'returns' typeornothing body
       ;

vardecloptional: |
                 vardecl 
               ;

body: vardecloptional statements 'end' 
    ;

idstar: |
        ',' id idstar
      ;

varseq: id idstar ':' type
      ;

booleanorinteger: 'boolean' |
                  'integer' 
                ;

arrayoptional: |
               'array' 
             ;

type: booleanorinteger arrayoptional 
    ;

varseqsemicolonstar: |
                     varseq ';' varseqsemicolonstar 
                   ;

vardecl: varseq ';' varseqsemicolonstar 
       ;

statements: 'chillax' |
            statement semicolonstatementstar 
          ;

semicolonstatementstar: |
                        ';' statement semicolonstatementstar 
                      ;

statement: assign |
           doN |
           inputN |
           outputN |
           popN |
           whenN |
           whileN 
         ;

simpleoptional: |
                  '[' simple ']' 
                ;

exprorarraysimple: expr |
                   'array' simple 
                 ;

assign: 'let' id simpleoptional '=' exprorarraysimple
      ;

exprstar: |
          ',' expr exprstar 
        ;

doN: 'do' id '(' expr exprstar ')'
   ;

inputN: 'input'  id simpleoptional
      ;

stringorexpr: 'string' |
              expr 
            ;

stringorexprstar: |
                  '.' stringorexpr stringorexprstar 
                ;

outputN: 'output' stringorexpr stringorexprstar 
       ;

exproptional: |
              expr 
            ;

popN: 'pop' exproptional 
    ;

caseexprcolonstatementsendstar: |
                                'case' expr ':' statements 'end' caseexprcolonstatementsendstar 
                              ;

otherwisecolonstatementsendoptional: |
                                     'otherwise'  ':' statements 'end'
                                   ;

whenN: 'when' 'case' expr ':' statements 'end' caseexprcolonstatementsendstar otherwisecolonstatementsendoptional
     ;

whileN: 'while' expr ':' statements 'end' 
      ;

relopsimpleoptional: |
                     relop simple 
                   ;

expr: simple relopsimpleoptional 
    ;

relop: '=' |
       '>=' |
       '>' |
       '<=' |
       '<' |
       '/=' 
     ;

minusoptional: |
               '-' 
             ;

addoptermstar: |
               addop term addoptermstar 
             ;

simple: minusoptional term addoptermstar 
      ;

addop: '-' |
       'or' |
       '+' 
     ;

mulopfactorstar: |
                 mulop factor mulopfactorstar 
               ;

term: factor mulopfactorstar 
    ;

mulop: 'and' |
       '/' |
       '*' |
       'rem' 
     ;

simpleoptionalorexprexprstaroptional: |
                                '[' simple ']' |
                                '(' expr exprstar ')'
                              ;

factor: id simpleoptionalorexprexprstaroptional|
        num |
        '(' expr ')'|
        'not' factor |
        'true' |
        'false' 
      ;

id: 'a'
  ;

num: '0'
   ;
%%

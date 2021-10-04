%%
programN: 'program' id funcdefstar body
        ;
        
funcdefstar: |
             funcdef funcdefstar
             ;

typeidstar: |
            ',' type id typeidstar
            ;

typeidtypeidstar: |
                  type id typeidstar
                  ;
                  
arrowtypeoptional: |
                   '->' type
                   ;

funcdef: define id '(' typeidtypeidstar ')' arrowtypeoptional body
         ;
         
vardefstar: |
            vardef vardefstar
            ;
            

body: begin vardefstar statements end
      ;
      
booleanorint: boolean
              | integer
              ;
              
arrayoptional: |
               array
               ;

type: booleanorint arrayoptional
      ;
      
idstar: |
        ',' id idstar
        ;

vardef: type id idstar ';'
        ;

statements: 'chill'
            | statement statementstar
            ;

statementstar: |
               ';' statement statementstar
               ;

statement: exitN
 	   |ifN
 	   |whileN
 	   |name
 	   |readN
 	   |writeN
 	   ;
exproptional: |
              expr
              ;

exitN: 'exit' exproptional
       ;
elseifstar: |
            'elsif' expr 'then' statements elseifstar
            ;

elseoptional: |
              'else' statements
              ;

ifN: 'if' expr 'then' statements elseifstar elseoptional  'end'
     ;
     
arglistorassign: arglist
                 |indexoptional '<-' exprarrsimple
                 ;

indexoptional: |
               index
               ;

exprarrsimple: expr
               |array simple
               ;

name: id arglistorassign
      ;

readN: 'read' id indexoptional
       ;
       
stringexpr: string
            |expr
            ;
            
stringexprstar: |
                '.' stringexpr stringexprstar
                ;

writeN: 'write' stringexpr stringexprstar
        ;

whileN: 'while' expr do statements end
        ;
        
exprstar: |
          ',' expr exprstar
          ;
          
exprstaroptional: |
                  expr exprstar
                  ;

arglist: '(' exprstaroptional ')'
         ;

index: '[' simple ']'
       ;
       
relopsimpleoptional: |
                     relop simple
                     ;

expr: simple relopsimpleoptional
      ;

relop: '='
       |'>='
       |'>'
       |'<='
       |'<'
       |'#'
       ;
       
minusoptional: |
               '-'
               ;

addoptermstar: |
               addop term addoptermstar
               ;

simple: minusoptional term addoptermstar
        ;
addop: '-'
       |'or'
       |'+'
       ;
       
mulopfactorstar:
                 |mulop factor mulopfactorstar
                 ;

term: factor mulopfactorstar
      ;
      
mulop: 'and'.
mulop: zzzzzzz/'.
mulop: (*).
mulop: (mod).
'(index|arglist)?': index.
'(index|arglist)?': arglist.
'(index|arglist)?': epsilon.
factor: id, '(index|arglist)?'.
factor: num.
factor: '(', expr, ')'.
factor: not, factor.
factor: true.
factor: false.
%%

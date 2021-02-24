%%

programN: 'program' id ':' funcdefstar 'main' ':' body
	;

funcdefstar:
	   | funcdef funcdefstar
	   ;

funcdef: id ':' 'takes' varseq varseqstar 'returns' typeornothing body
       ;

typeornothing: type
	     | 'nothing'
	     ;

type: booleanorint arrayoptional
    ;

booleanorint: 'boolean'
	    | 'integer'
	    ;

arrayoptional:
	     | 'array'
	     ;
varseqstar:
	  | ';' varseq varseqstar
	  ;

varseq: id idstar ':' type
      ;

vardecl: varseq ';' varseqstar
       ;

vardecloptional:
	       | vardecl
	       ;

body: vardecloptional statements 'end'
    ;

idstar:
      |',' id idstar
      ;
statements: 'chillax'
	  | statement statementstar
	  ;

statementstar:
	      | ';' statement statementstar
	      ;
statement: assign
	 | doN
	 | inputN
	 | outputN
	 | popN
	 | whenN
	 | whileN
	 ;

simpleoptional:
	      | '[' simple ']'
	      ;

exprarrsimple: expr
	     | 'array' simple
	     ;
assign: 'let' id simpleoptional  '=' exprarrsimple
      ;

exprstar:
	| ',' expr exprstar
	;

doN: 'do' id '(' expr exprstar ')'
   ;

inputN: 'input' id simpleoptional
      ;

stringexpr: 'string'
	  | expr
	  ;

stringexprstar:
	      | '.' stringexpr stringexprstar
	      ;

outputN: 'output' stringexpr stringexprstar
       ;

exproptional:
	    | expr
	    ;

popN: 'pop' exproptional
    ;

caseexprstatendstar:
		   | 'case' expr ':' statements 'end' caseexprstatendstar
		   ;

otherwisestatendoptional:
		       | 'otherwise' ':' statements 'end'
		       ;

whenN: 'when' 'case' expr ':' statements 'end' caseexprstatendstar otherwisestatendoptional
     ;

whileN: 'while' expr ':' statements 'end'
      ;

relopsimpleoptional:
		   | relop simple
		   ;

expr: simple relopsimpleoptional
    ;

relop: '='
     | '>='
     | '>'
     | '<='
     | '<'
     | '/='
     ;

minusopt:
	| '-'
	;

addopttermstar:
	      |addop term addopttermstar
	      ;

simple: minusopt term addopttermstar
      ;

addop: '-'
     | 'or'
     | '+'
     ;

mulopfactorstar:
	       | mulop factor mulopfactorstar
	       ;

term: factor mulopfactorstar
    ;

mulop: 'and'
     | '/'
     | '*'
     | 'rem'
     ;

simpleorexproptional:
		    | '[' simple ']'
		    | '(' expr exprstar ')'
		    ;

factor: id simpleorexproptional
      | '(' expr ')'
      | 'not' factor
      | 'true'
      | 'false'
      ;

id: 'a'
  ;
%%

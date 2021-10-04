%%
expr: simple  relopsimpleoptional
    ;

relopsimpleoptional:|
		    relop simple
		    ;

relop:'=' |
      '>='|
      '>' |
      '<='|
      '<' |
      '/='
      ;

minusoptional:|
	      '-'
	      ;

addoptermstar:|
	      addop term addoptermstar
	      ;

simple:minusoptional term addoptermstar
       ;

addop:'-'|
      'or'|
      '+'
      ;

mulopfactorstar:|
		mulop factor mulopfactorstar
		;

term:factor mulopfactorstar
     ;

mulop:'and'|
      '/'|
      '*'|
      'rem'
      ;

simpleexprexprstaroptional:|
			   '[' simple ']'|
                           '(' expr exprstarl ')'
                           ;

exprstarl:|
	  ',' expr exprstarl
	  ;

factor: 'id' simpleexprexprstaroptional|
	'num'|
	'(' expr ')'|
	'not' factor|
	'true'|
	'false'
	;

%%

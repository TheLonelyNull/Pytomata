%%

prog:	 'program' 'id' '=' blck
	 ;


stmtstar:
	 |stmt ';' stmtstar
	 ;

blck: 	'{' declstar stmtstar '}'
	 ;

decl:	 'var' 'id' ':' type
	;

declstar:
	|decl ';' declstar
	;

type:	 'bool'|
	 'int'
	 ;

elseoption:
	| 'else' stmt
	;

stmt: 	 'if' expr 'then' stmt elseoption|
	 'id' '=' expr|
	 'sleep'|
	 blck
	 ;

expr: 	 expr '==' expr|
	 expr '+' expr|
	 '(' expr ')'|
	 'id'|
	 'num'
	 ;
%%

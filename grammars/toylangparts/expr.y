%%
expr: 	 expr '==' expr|
	 expr '+' expr|
	 '(' expr ')'|
	 'id'|
	 'num'
	 ;
%%
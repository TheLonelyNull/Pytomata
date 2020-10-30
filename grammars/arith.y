%%

E: E '*' E
 | E '/' E
 | E '+' E
 | E '-' E
 | '(' E ')'
 | optionalminus 'num'
 | 'id'
 ;
optionalminus:
	     | '-'
	     ;
%%
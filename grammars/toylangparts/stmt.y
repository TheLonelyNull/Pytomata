%%
stmt: 	 'if' 'expr' 'then' stmt elseoption|
	 'while' 'expr' 'do' stmt|
	 id '=' 'expr'|
	 'sleep'
	 'blck'
	 ;
elseoption:
	 |'else' stmt
	 ;
%%
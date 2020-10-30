%%
/* Terminals: a,b,c 		*/
/* Non-Termianls A, B, S	*/
/* Start Symbol: S 		*/
S : A 'a'
  ;

S : 'b' A 'b'
  ;

A : 'a'
  ;

%%

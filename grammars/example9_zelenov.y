%%

S: V '=' E ';'
 | E ';'
 ;

E: A T
 ;

T:
 | T '+' A
 | '+' A
 ;

V: 'id'
 ;

A: 'id'
 ;
%%

%%

E_prime: E
       ;

E: E '+' T
 | T
 ;

T: '(' E ')'
 ;

T: 'id'
 ;

%%

%%

E: T E_prime
 ;

E_prime:
       | '+' T E_prime
       | '-' T E_prime
       ;
T: F T_prime
 ;

T_prime:
       | '*' F T_prime
       ;

F: '(' E ')'
 | 'id'
 ;

%%

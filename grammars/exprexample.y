%%

E: E '+' F
 | E '-' F
 | F
 ;

F: 'num'
 | 'id'
 | '(' E ')'
 ;

%%

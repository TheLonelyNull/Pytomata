%%

e: e '+' t
 | e '-' t
 | t
 ;

t: t '*' f
 | t '/' f
 | f
 ;

f: 'num'
 | 'id'
 | '(' e ')'
 ;

%%

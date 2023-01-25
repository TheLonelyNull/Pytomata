%%
reloporsimpleoptional: relop simple
                     |
                     ;
expr: simple reloporsimpleoptional;
relop: '='
     | '>='
     | '>'
     | '<='
     | '<'
     | '/='
     ;
minusoptional: '-'
             |
             ;
addoptermstar: addop term addoptermstar
             |
             ;
simple: minusoptional term addoptermstar;
addop: '-'
     | 'or'
     | '+'
     ;
mulopfactorstar: mulop factor mulopfactorstar
               |
               ;
term: factor mulopfactorstar;
mulop: 'and'
     | '/'
     | '*'
     | 'mod'
     ;

commaexprstar: ',' expr commaexprstar
             |
             ;
bracksimpbrackexprcommaexprstaroptional: '[' simple ']'
                                       | '(' expr commaexprstar ')'
                                       |
                                       ;
factor: 'id' bracksimpbrackexprcommaexprstaroptional
      | 'num'
      | '(' expr ')'
      | 'not' factor
      | 'true'
      | 'false'
      ;

%%
%%

initsymbol: value
          ;

value: object |
       array |
       'number'|
       'string' |
       'true' |
       'false' |
       'null'
     ;


membersoptional: |
                 members
               ;

object: '{' membersoptional '}'
      ;

pairstar: |
          ',' pair pairstar
        ;

members: pair pairstar
       ;

pair: string ':' value
    ;

elementsoptional: |
                  elements
                ;

array: '[' elementsoptional ']'
     ;

valuestar: |
           ',' value valuestar
         ;

elements: value valuestar
        ;


%%

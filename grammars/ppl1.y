%%

prog: 'program' 'id' 'has' declsemicolonstarstar block 'id' 'FULLSTOP';
semicolostar: ';' semicolostar
	    |
	    ;
semicolonplus: ';' semicolostar
             ;
declsemicolonstarstar: decl semicolonplusdeclsemicolonstarstar
                     |
                     ;
publicprivateoptional: 'public'
                     | 'private'
                     |
                     ;
constdeclvardeclfundeclprocdecltypedecl: constdecl
                                       | vardecl
                                       | fundecl
                                       | procdecl
                                       | typedecl
                                       ;
decl: publicprivateoptional constdeclvardeclfundeclprocdecltypedecl;
constdecl: 'const' 'id' ':' btype 'is' expr;
commaidstar: ',' 'id' commaidstar
           |
           ;
vardecl: 'var' 'id' commaidstar ':' stype;
funparamsoptional: funparams
                 |
                 ;
fundecl: 'function' 'id' '(' funparamsoptional ')' 'returns' typeN 'is' block 'id';
commafunparamstar: ',' funparam commafunparamstar
                 |
                 ;
funparams: funparam commafunparamstar;
funparam: 'id' commaidstar ':' stype;
procparamsoptional: procparams
                  |
                  ;
procdecl: 'procedure' 'id' '(' procparamsoptional ')' 'is' block 'id';
commaprocparamstar: ',' procparam commaprocparamstar
                  |
                  ;
procparams: procparam commaprocparamstar;
inoutinoutoptional: 'in'
                  | 'out '
                  | 'inout'
                  |
                  ;
procparam: inoutinoutoptional 'id' commaidstar ':' stype;
typedecl: 'type' 'id' 'is' typeN;
btype: 'bool'
     | unsignedoptional 'int'
     ;
unsignedoptional: 'unsigned'
                |
                ;
stype: btype
     | 'id'
     ;
typeN: btype
     | 'id'
     | 'array' 'of' typeN
     | 'pointer' 'to' typeN
     ;
semicolonstmtstar: ';' stmt semicolonstmtstar
                 |
                 ;
stmts: stmt semicolonstmtstar;
stmt: assign
    | matchN
    | loopN
    | call
    | block
    ;
assign: lval '<-' expr;
lval: 'id'
    | lval '[' expr ']'
    | '!' lval
    ;
elsesmtoptional: 'else' stmt
               |
               ;
matchN: 'match' expr 'with' mclauses elsesmtoptional;
semicolonmclausestar: ';' mclause semicolonmclausestar
                    |
                    ;
mclauses: mclause semicolonmclausestar;
mclause: expr 'RIGHTARROW' stmt;
whileexproptional: 'while' expr
                 |
                 ;
untilexproptional: 'until' expr
                 |
                 ;
loopN: 'loop' whileexproptional stmt untilexproptional;
argsoptional: args
            |
            ;
call: 'id' '(' argsoptional ')';
commaexprstar: ',' expr commaexprstar
             |
             ;
args: expr commaexprstar;
vardeclsemistar: vardecl ';' vardeclsemistar
               |
               ;
block: 'begin' vardeclsemistar stmts 'end';
expr: expr binop expr
    | lval
    | call
    |'~' expr
    |'~~' expr
    | '(' expr ')'
    | '0'
    | 'true'
    | 'false'
    ;
binop: '=='
     | '<>'
     | '>='
     | '>'
     | '<='
     | '<'
     | '<<'
     | '>>'
     | '&'
     | '^'
     | '|'
     | '&&'
     | '^^'
     | '||'
     ;

%%
%%
prog: 'EENHEID' id optionalintbrackets sysblock id 'FULLSTOP'
    ;
optionalintbrackets: |
		     '[' int ']'
		     ;

optionaldecl: |
	      decls
	      ;
	      
optionalstmts: |
		stmts
		;

sysblock: 'BEGIN' optionaldecl optionalstmts 'EINDE'
          ;
          
declstar: |
	  ';' decl declstar
          ;

decls: decl declstar
       ;

decl: constdecl|
      vardecl|
      fundecl|
      procdecl
      ;

constdecl: 'KONST' id ':' stype ':=' expr
           ;

idstar: |
	',' id idstar
	;
	
vardecl: 'VER' id idstar ':' type
	 ;
	 
opstionalfunparams: |
		    funparams
		    ;
		    
fundecl: 'FUNKSIE' id '(' opstionalfunparams ')' ':' type ':=' block id
         ;
         
funparamstar: |
              ',' funparam funparamstar
              ;

funparams: funparam funparamstar
           |id idstar ':' type
           ;

funparam: id idstar ':' type
          ;
           
optionalprocparams: |
                    procparams
                    ;
                    
procdecl: 'PROSEDURE' id '(' optionalprocparams ')' ':=' block id
          ;
          
procparamsstar: |
                ',' procparam procparamsstar
                ;
                
procparams: procparam procparamsstar
            ;
            
veroptional: |
             'VER'
             ;
             
procparam: veroptional id idstar ':' type
           ;
           
skikkingoptional: |
                  'SKIKKING'
                  ;

type: stype skikkingoptional
      ;

stype: 'WAARHEID'
       |lanklanklankoptional ntype
       ;

lankoptional: |
              'LANK'
              ;
              
lanklankoptional: |
                  'LANK' lankoptional
                  ;

lanklanklankoptional: |
                      'LANK' lanklankoptional
                      ;


ntype: 'AFTELBAR'
       |'BREUK'
       ;
       
stmtstar: |
          ';' stmt stmtstar
          ;

stmts: stmt stmtstar
       ;
       
stmt: assign
      |cond
      |loop
      |call
      |block
      ;
      
assign: lval ':=' expr
        ;
        
exprbracoptional: |
                  '[' expr ']'
                  ;

lval: id exprbracoptional
      ;
      
anderssmtoptional: |
                   'ANDERS' stmt
                   ;

cond: 'INDIEN' expr 'DAN' stmt anderssmtoptional
      ;
      
loop: 'TERWYL' expr 'DOEN' lstmt
      ;
      
argsoptional: |
              args
              ;
              
call: id '(' argsoptional ')'
    ;
    
exprstar: |
          ',' expr exprstar
          ;

args: expr exprstar
      ;
      
vdeclstar: |
           vdecls
           ;

block: 'BEGIN' vdeclstar optionalstmts 'EINDE'
       ;
       
vardeclstar: |
             ';' vardecl vardeclstar
             ;

vdecls: vardecl vardeclstar
        ;
        
lstmtstar: |
           ';' lstmt lstmtstar
           ;

lstmts: lstmt lstmtstar
        ;
      
lstmt: 'AFBREEK'
       |assign
       |call
       |loop
       |lcond
       |lblock
       ;
       
anderslstmtoptional: |
                     'ANDERS' lstmt
                     ;

lcond: 'INDIEN' expr 'DAN' lstmt anderslstmtoptional
       ;
lstmtsoptional: |
                lstmts
                ;

lblock: 'BEGIN' vdeclstar lstmtsoptional 'EINDE'
        ;

expr: expr binop expr
      |lval
      |call
      |'-' expr
      |'(' expr ')'
      | int
      |'WAAR'
      |'VALS'
      ;

binop: '=='
       |'!='
       |'>='
       |'>'
       |'<='
       |'<'
       |'-'
       |'+'
       |'/'
       |'*'
       |'**'
       ;

id:'a'
    ;

int: '0'
     ;
%%
%%

graphN: strictoptional digraphorgraph idoptional '{' stmtlist '}'
      ;
strictoptional:
	      | 'strict'
	      ;

digraphorgraph:'graph'
	      | 'digraph'
	      ;

idoptional: 
	  | 'id'
	  ;

semicolonoptional:
		 | ';'
		 ;

stmtlistoptional:
		| stmtlist
		;

stmtstmtlistoptional:
		    | stmt semicolonoptional stmtlistoptional
		    ;

stmtlist: stmtstmtlistoptional
	;

stmt: attrstmt
    | nodestmt
    | edgestmt
    | subgraphn
    | 'id' '=' 'id'
    ;

graphnodeedge: 'graph'
	     | 'node'
	     | 'edge'
	     ;

attrstmt: graphnodeedge attrlist
	;

alistoptional:
	     | alist
	     ;

attrlistoptional:
		| attrlist
		;

attrlist: '[' alistoptional ']' attrlistoptional
	;

commaoptional: 
	     | ','
	     ;

alist : 'id' '=' 'id' commaoptional alistoptional
      ;

nodestmt: nodeid attrlistoptional
	;

portoptional:
	    | port
	    ;

nodeid: 'id' portoptional
      ;

compassptoptional:
		 | ':' compasspt
		 ;

port: ':' 'id' compassptoptional
    | ':' compasspt
    ;

compasspt: 'id'
	 ;

nodeidsubgraphn: nodeid
	       | subgraphn
	       ;

edgestmt: nodeidsubgraphn edgerhs attrlistoptional
	;

edgerhsoptional:
	       | edgerhs
	       ;

edgerhs: edgeop nodeidsubgraphn edgerhsoptional
       ;

edgeop: '->'
      | '--'
      ;

subgraphidoptional: 
		  | 'subgraph' idoptional
		  ;

subgraphn: subgraphidoptional '{' stmtlist '}'
	 ;


%%

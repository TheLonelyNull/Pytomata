%%

sourceFile: packageClause eos importdecleosstar topleveldecleosstar;
importdecleosstar: importDecl eos importdecleosstar|
		   ;
topleveldecleosstar: topLevelDecl eos topleveldecleosstar|
		     ;
packageClause: 'package' 'a';
importspecorspeceosstar: importSpec;
importspeceosstar: importSpec eos importspeceosstar
                   |;
importspecorspeceosstar: '(' importspeceosstar ')';
importDecl: 'import' importspecorspeceosstar;
dotidoptional: '.'
             | 'a'
             | ;
importSpec: dotidoptional importPath;
importPath: 'STRING';
topLevelDecl: declaration
            | functionDecl
            | methodDecl;
declaration: constDecl
           | typeDecl
           | varDecl;
constspecorspeceosstar: constSpec
                      | '(' constspeceosstar ')';
constspeceosstar: constSpec eos constspeceosstar
                | ;
constDecl: 'const' constspecorspeceosstar;
typeNOptional: typeN
             | ;
typnOptionalEqualExpresionListOptional: typeNOptional '=' expressionList
                                      | ;
constSpec: identifierList typnOptionalEqualExpresionListOptional;
commaIdStar: ',' 'a' commaIdStar
           | ;
identifierList: 'a' commaIdStar;
commaexpresionstar: ',' expression commaexpresionstar
                  | ;

expressionList: expression commaexpresionstar;
typespectypespeceosstar: typeSpec
                       | '(' typespeceosstar ')';
typespeceosstar: typeSpec eos typespeceosstar
               | ;
typeDecl: 'type' typespectypespeceosstar;
typeSpec: 'a' typeN;
functionorsignature: function
                   | signature;
functionDecl: 'func' 'a' functionorsignature;
function: signature block;
methodDecl: 'func' receiver 'a' functionorsignature;
receiver: parameters;
varSpecOrVarSpecEosStar: varSpec
                       | '(' varSpecEosStar ')';
varSpecEosStar: varSpec eos varSpecEosStar
              | ;
varDecl: 'var' varSpecOrVarSpecEosStar;
equalExpressionListOptional: '=' expressionList
                           | ;
typeNEqualExpressionListOptionalEqualExpresionList: typeN equalExpressionListOptional
                                                  | '=' expressionList;
varSpec: identifierList typeNEqualExpressionListOptionalEqualExpresionList;
block: 'CURLY_OPEN' statementList 'CURLY_CLOSED';
statementeosstar: statement eos statementeosstar
                | ;
statementList: statementeosstar;
statement: declaration
            |labeledStmt
            | simpleStmt
            | goStmt
            | returnStmt
            | breakStmt
            | continueStmt
            | gotoStmt
            | fallthroughStmt
            | block
            | ifStmt
            | switchStmt
            | selectStmt
            | forStmt
            | deferStmt;
simpleStmt: sendStmt
          | expressionStmt
          | incDecStmt
          | assignment
          | shortVarDecl
          | emptyStmt;
expressionStmt: expression;
sendStmt: expression '<-' expression;
plusplusorminmin:  '++'
                |  '--' ;
incDecStmt: expression plusplusorminmin;
assignment: expressionList assign_op expressionList;
assign_op:  '+='
            |  '-='
            | '|='
            |  '^='
            |  '*='
            |  '/='
            | '%='
            |  '<<='
            |  '>>='
            |  '&='
            |  '&^='
            | '=';
shortVarDecl: identifierList ':=' expressionList;
emptyStmt: ';';
labeledStmt: 'a' ':' statement;
expressionListOptional: expressionList
                      | ;
returnStmt: 'return' expressionListOptional;
tidoptional: 'a'
           | ;
breakStmt: 'break' tidoptional;
continueStmt: 'continue' tidoptional;
gotoStmt: 'goto' 'a';
fallthroughStmt: 'fallthrough';
deferStmt: 'defer' expression;
simpleStmtOptional: simpleStmt ';'
                  | ;
elseifstmtblockoptional: 'else' ifStmt
                       | block
                       | ;
ifStmt: 'if' simpleStmtOptional expression block elseifstmtblockoptional;
switchStmt: exprSwitchStmt
          | typeSwitchStmt;
expressionOptional: expression
                  | ;
exprCaseClauseStar: exprCaseClause exprCaseClauseStar
                  | ;

exprSwitchStmt: 'switch' simpleStmtOptional expressionOptional 'CURLY_OPEN' exprCaseClauseStar 'CURLY_CLOSED';
typeCaseClauseStar: typeCaseClause typeCaseClauseStar
                  | ;
typeSwitchStmt: 'switch' simpleStmtOptional typeSwitchGuard 'CURLY_OPEN' typeCaseClauseStar 'CURLY_CLOSED';

exprCaseClause: exprSwitchCase ':' statementList;

exprSwitchCase: 'case' expressionList
              | 'default';

idcolonequaloptional: 'a' ':='
                    | ;
typeSwitchGuard: idcolonequaloptional primaryExpr '.' '(' 'type' ')';
typeCaseClause: typeSwitchCase ':' statementList;
typeSwitchCase: 'case' typeList
              | 'default';
commatypeNStar: ',' typeN commatypeNStar
              | ;
typeList: typeN commatypeNStar;
commClauseStar: commClause commClauseStar
              | ;
selectStmt: 'select' 'CURLY_OPEN' commClauseStar 'CURLY_CLOSED';
commClause: commCase ':' statementList;
sendStmtOrRecvStmt: sendStmt
                  | recvStmt;
commCase: 'case' sendStmtOrRecvStmt
        | 'default';
expressionListEqualIdListColonEqualOptional: expressionList '='
                                           | identifierList ':='
                                           | ;
recvStmt: expressionListEqualIdListColonEqualOptional expression;
expressionOrForClauseOrRangeClauseOptional: expression
                                          | forClause
                                          | rangeClause
                                          | ;
forStmt: 'for' expressionOrForClauseOrRangeClauseOptional block;
simpleStmtOptional: simpleStmt
                  | ;
forClause: simpleStmtOptional ';' expressionOptional ';' simpleStmtOptional;
rangeClause: expressionListEqualIdListColonEqualOptional 'range' expression;
goStmt: 'go' expression;
typeN: typeName
     | typeLit
     | '(' typeN ')';
typeName: 'A'
        | qualifiedTypeIdent;
typeLit: arrayType
         |structType
         |pointerType
         |functionType
         |interfaceType
         |sliceType
         |mapType
         |channelType;
arrayType: '[' arrayLength ']' elementType;
arrayLength: expression;
elementType: typeN;
pointerType: '*' typeN;
methodSpecEosStar: methodSpec eos methodSpecEosStar
                 | ;
interfaceType: 'interface' 'CURLY_OPEN' methodSpecEosStar 'CURLY_CLOSED';
sliceType: '[' ']' elementType;
mapType: 'map' '[' typeN ']' elementType;
chanorchanarrowarrowchan: 'chan'
                        | 'chan' '<-'
                        |  '<-' 'chan';
channelType: chanorchanarrowarrowchan elementType;
methodSpec: 'a' parameters result
          | typeName
          | 'a' parameters;
functionType: 'func' signature;
signature: parameters result
         | parameters;
result: parameters
      | typeN;
commaOptional: ','
             | ;
parameterListCommaOptional: parameterList commaOptional
                          | ;
parameters: '(' parameterListCommaOptional ')';
commaParameterDeclStar: ',' parameterDecl commaParameterDeclStar
                      | ;
parameterList: parameterDecl commaParameterDeclStar;
identifierListOptional: identifierList
                      | ;
elipsesOptioanl:  '...'
               | ;
parameterDecl: identifierListOptional elipsesOptioanl typeN;
operand: literal
       | operandName
       | methodExpr
       | '(' expression ')';
literal: basicLit
       | compositeLit
       | functionLit;
basicLit: '0'
        | '0.0'
        | '1i'
        | 'STRING';
operandName: 'a'
           | qualifiedIdent;
qualifiedIdent: 'a' '.' 'a';
qualifiedTypeIdent:  'A' '.' 'A';
compositeLit: literalType literalValue;
literalType: structType
           | arrayType
           | '[' '...' ']' elementType
           | sliceType
           | mapType
           | typeName;
elementListCommaOptionalOptional: elementList commaOptional
                                | ;
literalValue: 'CURLY_OPEN' elementListCommaOptionalOptional 'CURLY_CLOSED';
commaKeyedElementOptional: ',' keyedElement commaKeyedElementOptional
                         | ;
elementList: keyedElement commaKeyedElementOptional;
keycolonOptional: key ':'
                | ;
keyedElement: keycolonOptional element;
key: 'a'
   | expression
   | literalValue;
element: expression
       | literalValue;
fieldDeclEosStar: fieldDecl eos fieldDeclEosStar
                | ;
structType: 'struct' 'CURLY_OPEN' fieldDeclEosStar 'CURLY_CLOSED';
identifierListTypeNorAnonymousField: identifierList typeN
                                   | anonymousField;
stringLitOptional: 'STRING'
                 | ;
fieldDecl: identifierListTypeNorAnonymousField stringLitOptional;
starOptional: '*'
            | ;
anonymousField: starOptional typeName;
functionLit: 'func' function;
primaryExpr: operand
           | conversion
           | primaryExpr selector
           | primaryExpr index
           | primaryExpr slice
           | primaryExpr typeAssertion
           | primaryExpr arguments;
selector: '.' 'a';
index: '[' expression ']';
expresionOptionalMany: expressionOptional ':' expressionOptional
                     | expressionOptional ':' expression ':' expression;
slice: '[' expresionOptionalMany ']';
typeAssertion: '.' '(' typeN ')';
expressionListOrTypeNExpressionListOptional: expressionList;
commaExpressionListOptional: ',' expressionList
                           | ;
expressionListOrTypeNExpressionListOptional: typeN commaExpressionListOptional;
expresionListTypeNCommaExpressionListOptionalOptional: expressionListOrTypeNExpressionListOptional elipsesOptioanl commaOptional
                                                     | ;
arguments: '(' expresionListTypeNCommaExpressionListOptionalOptional ')';
methodExpr: receiverType '.' 'a';
receiverType: typeName
            | '(' '*' typeName ')'
            | '(' receiverType ')';
expression: unaryExpr;
symbleOpps: '||'
            |'&&'
            |'=='
            |'!='
            |'<'
            |'<='
            |';>'
            |'>='
            |'+'
            |'-'
            |'|'
            |'^'
            |'*'
            |'/'
            |'%'
            |'<<'
            |'>>'
            |'&'
            |'&^';
expression: expression symbleOpps expression;
unaryExpr: primaryExpr;
addOpps: '+'
            |'-'
            |'!'
            |'^'
            |'*'
            |'&'
            |'<-';
unaryExpr: addOpps unaryExpr;
conversion: typeN '(' expression commaOptional ')';
eos: ';';

%%
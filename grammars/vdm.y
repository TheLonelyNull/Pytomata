%%

initsymbol: 'begin_of_file' document 'end_of_file' 
          ;

anymodulestar: |
               anymodule anymodulestar 
             ;

document: anymodule anymodulestar |
          definitionblock definitionblockstar 
        ;

definitionblockstar: |
                     definitionblock definitionblockstar 
                   ;

anymodule: moduleN 
         ;

modulebodyoptional: |
                    modulebody 
                  ;

moduleN: 'moduleid' interface modulebodyoptional 'endid' 
       ;

importdefinitionlistoptional: |
                              importdefinitionlist 
                            ;

interface: importdefinitionlistoptional exportdefinition 
         ;

importdefinitionstar: |
                      ',' importdefinition importdefinitionstar 
                    ;

importdefinitionlist: 'imports' importdefinition importdefinitionstar 
                    ;

importdefinition: 'fromid' importmodulesignature 
                ;

importmodulesignature: 'all' |
                       importsignature importsignaturestar 
                     ;

importsignaturestar: |
                     importsignature importsignaturestar 
                   ;

importsignature: importtypessignature |
                 importvaluessignature |
                 importfunctionssignature |
                 importoperationssignature 
               ;

semicolontypeimportstar: |
                         ';' typeimport semicolontypeimportstar 
                       ;

semicolonoptional: |
                   ';' 
                 ;

importtypessignature: 'types' typeimport semicolontypeimportstar semicolonoptional 
                    ;

renamednameoptional: |
                     'renamed' name 
                   ;

typeimport: name renamednameoptional |
            typedefinition renamednameoptional 
          ;

semicolonvalueimportstar: |
                          ';' valueimport semicolonvalueimportstar 
                        ;

importvaluessignature: 'values' valueimport semicolonvalueimportstar semicolonoptional 
                     ;

colontypeoptional: |
                   ':' type 
                 ;

valueimport: name colontypeoptional renamednameoptional 
           ;

semicolonfunctionimportstar: |
                             ';' functionimport semicolonfunctionimportstar 
                           ;

importfunctionssignature: 'functions' functionimport semicolonfunctionimportstar semicolonoptional 
                        ;

functionimporttypeoptional: |
                            functionimporttype 
                          ;

functionimport: name functionimporttypeoptional renamednameoptional 
              ;

typevariablelistoptional: |
                          typevariablelist 
                        ;

functionimporttype: typevariablelistoptional ':' functiontype 
                  ;

semicolonoperationimportstar: |
                              ';' operationimport semicolonoperationimportstar 
                            ;

importoperationssignature: 'operations' operationimport semicolonoperationimportstar semicolonoptional 
                         ;

colonoperationtypeoptional: |
                            ':' operationtype 
                          ;

operationimport: name colonoperationtypeoptional renamednameoptional 
               ;

exportdefinition: 'exports' exportmodulesignature 
                ;

exportmodulesignature: 'all' |
                       exportsignature exportsignaturestar 
                     ;

exportsignaturestar: |
                     exportsignature exportsignaturestar 
                   ;

exportsignature: exporttypessignature |
                 exportvaluessignature |
                 exportfunctionssignature |
                 exportoperationssignature 
               ;

semicolontypeexportstar: |
                         ';' typeexport semicolontypeexportstar 
                       ;

exporttypessignature: 'types' typeexport semicolontypeexportstar semicolonoptional 
                    ;

structoptional: |
                'struct' 
              ;

typeexport: structoptional name 
          ;

semicolonvaluesignaturestar: |
                             ';' valuesignature semicolonvaluesignaturestar 
                           ;

exportvaluessignature: 'values' valuesignature semicolonvaluesignaturestar semicolonoptional 
                     ;

valuesignature: namelist ':' type 
              ;

semicolonfunctionsignaturestar: |
                                ';' functionsignature semicolonfunctionsignaturestar 
                              ;

exportfunctionssignature: 'functions' functionsignature semicolonfunctionsignaturestar semicolonoptional 
                        ;

functionsignature: namelist typevariablelistoptional ':' functiontype 
                 ;

semicolonoperationsignaturestar: |
                                 ';' operationsignature semicolonoperationsignaturestar 
                               ;

exportoperationssignature: 'operations' operationsignature semicolonoperationsignaturestar semicolonoptional 
                         ;

operationsignature: namelist ':' operationtype 
                  ;

modulebody: 'definitions' definitionblock definitionblockstar 
          ;

definitionblock: typedefinitions |
                 statedefinition |
                 valuedefinitions |
                 functiondefinitions |
                 operationdefinitions 
               ;

semicolontypedefinitionstar: |
                             ';' typedefinition semicolontypedefinitionstar 
                           ;

typedefinitions: 'types' typedefinition semicolontypedefinitionstar semicolonoptional 
               ;

invariantoptional: |
                   invariant 
                 ;

typedefinition: 'id=' type invariantoptional |
                'id::' fieldlist invariantoptional 
              ;

type: bracketedtype |
      basictype |
      quotetype |
      compositetype |
      uniontype |
      producttype |
      optionaltype |
      settype |
      seqtype |
      maptype |
      partialfunctiontype |
      typename |
      typevariable 
    ;

bracketedtype: type 
             ;

basictype: 'bool' |
           'nat' |
           'nat1' |
           'int' |
           'rat' |
           'real' |
           'char' |
           'token' 
         ;

quotetype: 'quote_literal' 
         ;

compositetype: 'composeidof' fieldlist 'end' 
             ;

fieldstar: |
           field fieldstar 
         ;

fieldlist: fieldstar 
         ;

idcolonoptional: |
                 'id:' 
               ;

field: idcolonoptional type |
       idcolonminusoptional type 
     ;

idcolonminusoptional: |
                      'id:-' 
                    ;

ortypestar: |
            '|' type ortypestar 
          ;

uniontype: type '|' type ortypestar 
         ;

startypestar: |
              '*' type startypestar 
            ;

producttype: type '*' type startypestar 
           ;

optionaltype: '[' type ']' 
            ;

settype: set0type |
         set1type 
       ;

set0type: 'setof' type 
        ;

set1type: 'set1of' type 
        ;

seqtype: seq0type |
         seq1type 
       ;

seq0type: 'seqof' type 
        ;

seq1type: 'seq1of' type 
        ;

maptype: generalmaptype |
         injectivemaptype 
       ;

generalmaptype: 'map' type 'to' type 
              ;

injectivemaptype: 'inmap' type 'to' type 
                ;

functiontype: partialfunctiontype |
              totalfunctiontype 
            ;

partialfunctiontype: discretionarytype '->' type 
                   ;

totalfunctiontype: discretionarytype '+>' type 
                 ;

discretionarytype: type |
                   
                 ;

typename: name 
        ;

typevariable: 'type_variable_identifier' 
            ;

initialisationoptional: |
                        initialisation 
                      ;

statedefinition: 'stateidof' fieldlist invariantoptional initialisationoptional 'end' semicolonoptional 
               ;

invariant: 'inv' invariantinitialfunction 
         ;

initialisation: 'init' invariantinitialfunction 
              ;

invariantinitialfunction: pattern '==' expression 
                        ;

valuedefinitionoptional: |
                         valuedefinition 
                       ;

semicolonvaluedefinitionstar: |
                              ';' valuedefinition semicolonvaluedefinitionstar 
                            ;

valuedefinitions: 'values' valuedefinitionoptional semicolonvaluedefinitionstar semicolonoptional 
                ;

colonoptional: |
               ':' 
             ;

valuedefinition: pattern colonoptional '=' expression 
               ;

functiondefinitionoptional: |
                            functiondefinition 
                          ;

semicolonfunctiondefinitionstar: |
                                 ';' functiondefinition semicolonfunctiondefinitionstar 
                               ;

functiondefinitions: 'functions' functiondefinitionoptional semicolonfunctiondefinitionstar semicolonoptional 
                   ;

functiondefinition: explicitfunctiondefinition |
                    implicitfunctiondefinition |
                    extendedexplicitfunctiondefinition 
                  ;

preexpressionoptional: |
                       preexpression 
                     ;

postexpressionoptional: |
                        postexpression 
                      ;

measurenameoptional: |
                     measurename 
                   ;

explicitfunctiondefinition: 'id' typevariablelistoptional ':' functiontype 'id' parameterslist '==' functionbody preexpressionoptional postexpressionoptional measurenameoptional 
                          ;

preexpression: 'pre' expression 
             ;

postexpression: 'post' expression 
              ;

measurename: 'measure' name 
           ;

implicitfunctiondefinition: 'id' typevariablelistoptional parametertypes identifiertypepairlist preexpressionoptional 'post' expression 
                          ;

extendedexplicitfunctiondefinition: 'id' typevariablelistoptional parametertypes identifiertypepairlist '==' functionbody preexpressionoptional postexpressionoptional 
                                  ;

typevariableidentifierstar: |
                            ',type_variable_identifier' typevariableidentifierstar 
                          ;

typevariablelist: '[type_variable_identifiertype_variable_identifier' typevariableidentifierstar ']' 
                ;

idcolontypeidentifiertypepairliststar: |
                                       ',id:' type identifiertypepairlist idcolontypeidentifiertypepairliststar 
                                     ;

identifiertypepairlist: 'id:' type idcolontypeidentifiertypepairliststar 
                      ;

patterntypepairlistoptional: |
                             patterntypepairlist 
                           ;

parametertypes: patterntypepairlistoptional 
              ;

patternlistcolontypepatterntypepairliststar: |
                                             ',pattern_list:' type patterntypepairlist patternlistcolontypepatterntypepairliststar 
                                           ;

patterntypepairlist: 'pattern_list:' type patternlistcolontypepatterntypepairliststar 
                   ;

parametersstar: |
                parameters parametersstar 
              ;

parameterslist: parameters parametersstar 
              ;

patternlistoptional: |
                     'pattern_list' 
                   ;

parameters: patternlistoptional 
          ;

functionbody: expression |
              'issubclassresponsibility' |
              'isnotyetspecified' 
            ;

operationdefinitionoptional: |
                             operationdefinition 
                           ;

semicolonoperationdefinitionstar: |
                                  ';' operationdefinition semicolonoperationdefinitionstar 
                                ;

operationdefinitions: 'operations' operationdefinitionoptional semicolonoperationdefinitionstar semicolonoptional 
                    ;

operationdefinition: explicitoperationdefinition |
                     implicitoperationdefinition |
                     extendedexplicitoperationdefinition 
                   ;

explicitoperationdefinition: 'id:' operationtype 'id' parameters '==' operationbody preexpressionoptional postexpressionoptional 
                           ;

identifiertypepairlistoptional: |
                                identifiertypepairlist 
                              ;

implicitoperationdefinition: 'id' parametertypes identifiertypepairlistoptional implicitoperationbody 
                           ;

externalsoptional: |
                   externals 
                 ;

exceptionsoptional: |
                    exceptions 
                  ;

implicitoperationbody: externalsoptional preexpressionoptional postexpression exceptionsoptional 
                     ;

extendedexplicitoperationdefinition: 'id' parametertypes identifiertypepairlistoptional '==' operationbody externalsoptional preexpressionoptional postexpressionoptional exceptionsoptional 
                                   ;

operationtype: discretionarytype '==>' discretionarytype 
             ;

operationbody: statement |
               'issubclassresponsibility' |
               'isnotyetspecified' 
             ;

varinformationstar: |
                    varinformation varinformationstar 
                  ;

externals: 'ext' varinformationstar 
         ;

varinformation: mode namelist colonoptional 
              ;

mode: 'rd' |
      'wr' 
    ;

exceptions: 'errs' errorlist 
          ;

errorstar: |
           notbisonerror errorstar 
         ;

errorlist: notbisonerror errorstar 
         ;

notbisonerror: 'id:' expression '->' expression 
     ;

expressionstar: |
                ',' expression expressionstar 
              ;

expressionlist: expression expressionstar 
              ;

expression: bracketedexpression |
            letexpression |
            letbeexpression |
            defexpression |
            ifexpression |
            casesexpression |
            unaryexpression |
            binaryexpression |
            quantifiedexpression |
            iotaexpression |
            setenumeration |
            setcomprehension |
            setrangeexpression |
            sequenceenumeration |
            sequencecomprehension |
            subsequence |
            mapenumeration |
            mapcomprehension |
            tupleconstructor |
            recordconstructor |
            recordmodifier |
            apply |
            fieldselect |
            tupleselect |
            functiontypeinstantiation |
            lambdaexpression |
            narrowexpression |
            generalisexpression |
            undefinedexpression |
            preconditionexpression |
            'isofbaseclass_expression' |
            'isofclass_expression' |
            'samebaseclass_expression' |
            'sameclass_expression' |
            'act_expression' |
            'fin_expression' |
            'active_expression' |
            'req_expression' |
            'waiting_expression' |
            'time_expression' |
            name |
            oldname |
            'symbolic_literal' 
          ;

bracketedexpression: expression 
                   ;

localdefinitionstar: |
                     ',' localdefinition localdefinitionstar 
                   ;

letexpression: 'let' localdefinition localdefinitionstar 'in' expression 
             ;

bestexpressionoptional: |
                        'best' expression 
                      ;

letbeexpression: 'let' multiplebind bestexpressionoptional 'in' expression 
               ;

semicolonpatternbindequalexpressionstar: |
                                         ';' patternbind '=' expression semicolonpatternbindequalexpressionstar 
                                       ;

defexpression: 'def' patternbind '=' expression semicolonpatternbindequalexpressionstar semicolonoptional 'in' expression 
             ;

elseifexpressionoptional: |
                          elseifexpression 
                        ;

ifexpression: 'if' expression 'then' expression elseifexpressionoptional 'else' expression 
            ;

elseifexpression: 'elseif' expression 'then' expression 
                ;

othersexpressionoptional: |
                          ',' othersexpression 
                        ;

casesexpression: 'cases' expression ':' casesexpressionalternatives othersexpressionoptional 'end' 
               ;

casesexpressionalternativestar: |
                                ',' casesexpressionalternative casesexpressionalternativestar 
                              ;

casesexpressionalternatives: casesexpressionalternative casesexpressionalternativestar 
                           ;

casesexpressionalternative: 'pattern_list->' expression 
                          ;

othersexpression: 'others->' expression 
                ;

unaryexpression: prefixexpression |
                 mapinverse 
               ;

prefixexpression: unaryoperator expression 
                ;

unaryoperator: unaryplus |
               unaryminus |
               arithmeticabs |
               floorT |
               notT |
               setcardinality |
               finitepowerset |
               distributedsetunion |
               distributedsetintersection |
               sequencehead |
               sequencetail |
               sequencelength |
               sequenceelements |
               sequenceindices |
               sequencereverse |
               distributedsequenceconcatenation |
               mapdomain |
               maprange |
               distributedmapmerge 
             ;

unaryplus: '+' 
         ;

unaryminus: '-' 
          ;

arithmeticabs: 'abs' 
             ;

floorT: 'floor' 
      ;

notT: 'not' 
    ;

setcardinality: 'card' 
              ;

finitepowerset: 'power' 
              ;

distributedsetunion: 'dunion' 
                   ;

distributedsetintersection: 'dinter' 
                          ;

sequencehead: 'hd' 
            ;

sequencetail: 'tl' 
            ;

sequencelength: 'len' 
              ;

sequenceelements: 'elems' 
                ;

sequenceindices: 'inds' 
               ;

sequencereverse: 'reverse' 
               ;

distributedsequenceconcatenation: 'conc' 
                                ;

mapdomain: 'dom' 
         ;

maprange: 'rng' 
        ;

distributedmapmerge: 'merge' 
                   ;

mapinverse: 'inverse' expression 
          ;

binaryexpression: expression binaryoperator expression 
                ;

binaryoperator: arithmeticplus |
                arithmeticminus |
                arithmeticmultiplication |
                arithmeticdivide |
                arithmeticintegerdivision |
                arithmeticrem |
                arithmeticmod |
                lessthan |
                lessthanorequal |
                greaterthan |
                greaterthanorequal |
                equal |
                notequal |
                orT |
                andT |
                imply |
                logicalequivalence |
                notinset |
                inset |
                subsetT |
                propersubset |
                setunion |
                setdifference |
                setintersection |
                sequenceconcatenate |
                maporsequencemodify |
                mapmerge |
                mapdomainrestrictto |
                mapdomainrestrictby |
                maprangerestrictto |
                maprangerestrictby |
                composition |
                iterate 
              ;

arithmeticplus: '+' 
              ;

arithmeticminus: '-' 
               ;

arithmeticmultiplication: '*' 
                        ;

arithmeticdivide: '/' 
                ;

arithmeticintegerdivision: 'div' 
                         ;

arithmeticrem: 'rem' 
             ;

arithmeticmod: 'mod' 
             ;

lessthan: '<' 
        ;

lessthanorequal: '<=' 
               ;

greaterthan: '>' 
           ;

greaterthanorequal: '>=' 
                  ;

equal: '=' 
     ;

notequal: '<>' 
        ;

orT: 'or' 
   ;

andT: 'and' 
    ;

imply: '=>' 
     ;

logicalequivalence: '<=>' 
                  ;

notinset: 'notinset' 
        ;

inset: 'inset' 
     ;

subsetT: 'subset' 
       ;

propersubset: 'psubset' 
            ;

setunion: 'union' 
        ;

setdifference: '\\'
             ;

setintersection: 'inter' 
               ;

sequenceconcatenate: '^' 
                   ;

maporsequencemodify: '++' 
                   ;

mapmerge: 'munion' 
        ;

/* >: */
mapdomainrestrictto: 'mapdomainrestrictto'
                   ;

mapdomainrestrictby: '<-' 
                   ;
/* :> */
maprangerestrictto: 'maprangerestrictto'
                  ;
/*:-> */
maprangerestrictby: 'maprangerestrictby'
                  ;

composition: 'comp' 
           ;

iterate: '**' 
       ;

quantifiedexpression: allexpression |
                      existsexpression |
                      existsuniqueexpression 
                    ;

allexpression: 'forall' bindlist '&' expression 
             ;

existsexpression: 'exists' bindlist '&' expression 
                ;

existsuniqueexpression: 'exists1' bind '&' expression 
                      ;

iotaexpression: 'iota' bind '&' expression 
              ;

expressionlistoptional: |
                        expressionlist 
                      ;

setenumeration: '{' expressionlistoptional '}' 
              ;

andexpressionoptional: |
                       '&' expression 
                     ;

setcomprehension: '{' expression '|' bindlist andexpressionoptional '}' 
                ;

setrangeexpression: '{' expression ',...,' expression '}' 
                  ;

sequenceenumeration: '[' expressionlistoptional ']' 
                   ;

sequencecomprehension: '[' expression '|' bindlist andexpressionoptional ']' 
                     ;

subsequence: expression expression ',...,' expression 
           ;

mapletstar: |
            ',' maplet mapletstar 
          ;

mapenumeration: '{' maplet mapletstar '}' |
                '{|->}' 
              ;

maplet: expression '|->' expression 
      ;

mapcomprehension: '{' maplet '|' bindlist andexpressionoptional '}' 
                ;

tupleconstructor: 'mk_' expression ',' expressionlist 
                ;

recordconstructor: 'mk_name' expressionlistoptional 
                 ;

recordmodificationstar: |
                        ',' recordmodification recordmodificationstar 
                      ;

recordmodifier: 'mu' expression ',' recordmodification recordmodificationstar 
              ;

recordmodification: 'id|->' expression 
                  ;

apply: expression expressionlistoptional 
     ;

fieldselect: expression '.id' 
           ;

tupleselect: expression '.#numeral' 
           ;

typestar: |
          ',' type typestar 
        ;

functiontypeinstantiation: 
                         ;

lambdaexpression: 'lambda' typebindlist '&' expression 
                ;

narrowexpression: 'narrow_' expression ',' type 
                ;

generalisexpression: isexpression |
                     typejudgement 
                   ;

isexpression: 'is_name' expression |
              'is_basic_type' expression 
            ;

typejudgement: 'is_' expression ',' type 
             ;

undefinedexpression: 'undefined' 
                   ;

preconditionexpression: 'pre_' expressionlist 
                      ;

identifierstar: |
                '`identifier' identifierstar 
              ;

name: 'id' identifierstar 
    ;

namestar: |
          ',' name namestar 
        ;

namelist: name namestar 
        ;

oldname: 'id�' 
       ;

statedesignator: name |
                 fieldreference |
                 maporsequencereference 
               ;

fieldreference: statedesignator '.id' 
              ;

maporsequencereference: statedesignator expression 
                      ;

statement: letstatement |
           letbestatement |
           defstatement |
           blockstatement |
           generalassignstatement |
           ifstatement |
           casesstatement |
           sequenceforloop |
           setforloop |
           indexforloop |
           whileloop |
           nondeterministicstatement |
           callstatement |
           specificationstatement |
           'start_statement' |
           'start_list_statement' |
           'stop_statement' |
           'stop_list_statement' |
           'duration_statement' |
           'cycles_statement' |
           'return_statement' |
           alwaysstatement |
           trapstatement |
           recursivetrapstatement |
           exitstatement |
           errorstatement |
           identitystatement 
         ;

letstatement: 'let' localdefinition localdefinitionstar 'in' statement 
            ;

localdefinition: valuedefinition |
                 functiondefinition 
               ;

letbestatement: 'let' multiplebind bestexpressionoptional 'in' statement 
              ;

semicolonequalsdefinitionstar: |
                               ';' equalsdefinition semicolonequalsdefinitionstar 
                             ;

defstatement: 'def' equalsdefinition semicolonequalsdefinitionstar semicolonoptional 'in' statement 
            ;

equalsdefinition: patternbind '=' expression 
                ;

dclstatementstar: |
                  dclstatement dclstatementstar 
                ;

semicolonstatementstar: |
                        ';' statement semicolonstatementstar 
                      ;

blockstatement: dclstatementstar statement semicolonstatementstar semicolonoptional 
              ;

assignmentdefinitionstar: |
                          ',' assignmentdefinition assignmentdefinitionstar 
                        ;

dclstatement: 'dcl' assignmentdefinition assignmentdefinitionstar ';' 
            ;

colonequalexpressionoptional: |
                              ':=' expression 
                            ;

assignmentdefinition: 'identifier:' type colonequalexpressionoptional 
                    ;

generalassignstatement: assignstatement |
                        multipleassignstatement 
                      ;

assignstatement: statedesignator ':=' expression 
               ;

semicolonassignstatementstar: |
                              ';' assignstatement semicolonassignstatementstar 
                            ;

multipleassignstatement: 'atomic' assignstatement ';' assignstatement semicolonassignstatementstar 
                       ;

elseifstatementstar: |
                     elseifstatement elseifstatementstar 
                   ;

elsestatementoptional: |
                       'else' statement 
                     ;

ifstatement: 'if' expression 'then' statement elseifstatementstar elsestatementoptional 
           ;

elseifstatement: 'elseif' expression 'then' statement 
               ;

othersstatementoptional: |
                         ',' othersstatement 
                       ;

casesstatement: 'cases' expression ':' casesstatementalternatives othersstatementoptional 'end' 
              ;

casesstatementalternativestar: |
                               ',' casesstatementalternative casesstatementalternativestar 
                             ;

casesstatementalternatives: casesstatementalternative casesstatementalternativestar 
                          ;

casesstatementalternative: 'pattern_list->' statement 
                         ;

othersstatement: 'others->' statement 
               ;

sequenceforloop: 'for' patternbind 'in' expression 'do' statement 
               ;

setforloop: 'forall' pattern 'inset' expression 'do' statement 
          ;

byexpressionoptional: |
                      'by' expression 
                    ;

indexforloop: 'foridentifier=' expression 'to' expression byexpressionoptional 'do' statement 
            ;

whileloop: 'while' expression 'do' statement 
         ;

statementstar: |
               ',' statement statementstar 
             ;

nondeterministicstatement: '||' statement statementstar 
                         ;

callstatement: name expressionlistoptional 
             ;

specificationstatement: '[' implicitoperationbody ']' 
                      ;

alwaysstatement: 'always' statement 'in' statement 
               ;

trapstatement: 'trap' patternbind 'with' statement 'in' statement 
             ;

recursivetrapstatement: 'tixe' traps 'in' statement 
                      ;

patternbindorminusgtstatementstar: |
                                   ',' patternbind '|->' statement patternbindorminusgtstatementstar 
                                 ;

traps: '{' patternbind '|->' statement patternbindorminusgtstatementstar '}' 
     ;

expressionoptional: |
                    expression 
                  ;

exitstatement: 'exit' expressionoptional 
             ;

errorstatement: notbisonerror 
              ;

identitystatement: 'skip' 
                 ;

pattern: patternidentifier |
         matchvalue |
         setenumpattern |
         setunionpattern |
         seqenumpattern |
         seqconcpattern |
         mapenumerationpattern |
         mapmuinonpattern |
         tuplepattern |
         'object_pattern' |
         recordpattern 
       ;

patternidentifier: 'identifier' |
                   '-' 
                 ;

matchvalue: expression |
            'symbolic_literal' 
          ;

setenumpattern: '{' patternlistoptional '}' 
              ;

setunionpattern: pattern 'union' pattern 
               ;

seqenumpattern: '[' patternlistoptional ']' 
              ;

seqconcpattern: pattern '�' pattern 
              ;

mapenumerationpattern: '{' mapletpatternlist '}' |
                       '{|->}' 
                     ;

mapletpatternstar: |
                   ',' mapletpattern mapletpatternstar 
                 ;

mapletpatternlist: mapletpattern mapletpatternstar 
                 ;

mapletpattern: pattern '|->' pattern 
             ;

mapmuinonpattern: pattern 'munion' pattern 
                ;

tuplepattern: 'mk_' pattern ',pattern_list' 
            ;

recordpattern: 'mk_name' patternlistoptional 
             ;

patternbind: pattern |
             bind 
           ;

bind: setbind |
      seqbind |
      typebind 
    ;

setbind: pattern 'inset' expression 
       ;

seqbind: pattern 'inseq' expression 
       ;

typebind: pattern ':' type 
        ;

multiplebindstar: |
                  ',' multiplebind multiplebindstar 
                ;

bindlist: multiplebind multiplebindstar 
        ;

multiplebind: multiplesetbind |
              multipleseqbind |
              multipletypebind 
            ;

multiplesetbind: 'pattern_listinset' expression 
               ;

multipleseqbind: 'pattern_listinseq' expression 
               ;

multipletypebind: 'pattern_list:' type 
                ;

typebindstar: |
              ',' typebind typebindstar 
            ;

typebindlist: typebind typebindstar 
            ;


%%

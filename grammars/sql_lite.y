%%

initsymbol: 'begin_of_file' sqlstmtlist 'end_of_file' 
          ;

semicolonstar: |
               ';' semicolonstar 
             ;

plussemicolon: ';' plussemicolon |
               ';' 
             ;

plussemicolonsqlstmtstar: |
                          plussemicolon sqlstmt plussemicolonsqlstmtstar 
                        ;

sqlstmtlist: semicolonstar sqlstmt plussemicolonsqlstmtstar semicolonstar 
           ;

tKQUERYtKPLANoptional: |
                       't_K_QUERYt_K_PLAN' 
                     ;

tKEXPLAINtKQUERYtKPLANoptionaloptional: |
                                        't_K_EXPLAIN' tKQUERYtKPLANoptional 
                                      ;

altertablestmtoranalyzestmtorattachstmtorbeginstmtorcommitstmtorcompoundselectstmtorcreateindexstmtorcreatetablestmtorcreatetriggerstmtorcreateviewstmtorcreatevirtualtablestmtordeletestmtordeletestmtlimitedordetachstmtordropindexstmtordroptablestmtordroptriggerstmtordropviewstmtorfactoredselectstmtorinsertstmtorpragmastmtorreindexstmtorreleasestmtorrollbackstmtorsavepointstmtorsimpleselectstmtorselectstmtorupdatestmtorupdatestmtlimitedorvacuumstmt: altertablestmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     analyzestmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     attachstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     beginstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     commitstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     compoundselectstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     createindexstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     createtablestmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     createtriggerstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     createviewstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     createvirtualtablestmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     deletestmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     deletestmtlimited |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     detachstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     dropindexstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     droptablestmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     droptriggerstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     dropviewstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     factoredselectstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     insertstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     pragmastmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     reindexstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     releasestmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     rollbackstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     savepointstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     simpleselectstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     selectstmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     updatestmt |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     updatestmtlimited |
                                                                                                                                                                                                                                                                                                                                                                                                                                                                     vacuumstmt 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ;

sqlstmt: tKEXPLAINtKQUERYtKPLANoptionaloptional altertablestmtoranalyzestmtorattachstmtorbeginstmtorcommitstmtorcompoundselectstmtorcreateindexstmtorcreatetablestmtorcreatetriggerstmtorcreateviewstmtorcreatevirtualtablestmtordeletestmtordeletestmtlimitedordetachstmtordropindexstmtordroptablestmtordroptriggerstmtordropviewstmtorfactoredselectstmtorinsertstmtorpragmastmtorreindexstmtorreleasestmtorrollbackstmtorsavepointstmtorsimpleselectstmtorselectstmtorupdatestmtorupdatestmtlimitedorvacuumstmt 
       ;

databasenameoptional: |
                      databasename '.' 
                    ;

tKRENAMEtKTOnewtablenameortKADDtKCOLUMNoptionalcolumndef: 't_K_RENAMEt_K_TO' newtablename |
                                                          't_K_ADD' tKCOLUMNoptional columndef 
                                                        ;

tKCOLUMNoptional: |
                  't_K_COLUMN' 
                ;

altertablestmt: 't_K_ALTERt_K_TABLE' databasenameoptional tablename tKRENAMEtKTOnewtablenameortKADDtKCOLUMNoptionalcolumndef 
              ;

databasenameortableorindexnameordatabasenametableorindexnameoptional: |
                                                                      databasename |
                                                                      tableorindexname |
                                                                      databasename '.' tableorindexname 
                                                                    ;

analyzestmt: 't_K_ANALYZE' databasenameortableorindexnameordatabasenametableorindexnameoptional 
           ;

tKDATABASEoptional: |
                    't_K_DATABASE' 
                  ;

attachstmt: 't_K_ATTACH' tKDATABASEoptional expr 't_K_AS' databasename 
          ;

tKDEFERREDortKIMMEDIATEortKEXCLUSIVEoptional: |
                                              't_K_DEFERRED' |
                                              't_K_IMMEDIATE' |
                                              't_K_EXCLUSIVE' 
                                            ;

transactionnameoptional: |
                         transactionname 
                       ;

tKTRANSACTIONtransactionnameoptionaloptional: |
                                              't_K_TRANSACTION' transactionnameoptional 
                                            ;

beginstmt: 't_K_BEGIN' tKDEFERREDortKIMMEDIATEortKEXCLUSIVEoptional tKTRANSACTIONtransactionnameoptionaloptional 
         ;

tKCOMMITortKEND: 't_K_COMMIT' |
                 't_K_END' 
               ;

commitstmt: tKCOMMITortKEND tKTRANSACTIONtransactionnameoptionaloptional 
          ;

tKRECURSIVEoptional: |
                     't_K_RECURSIVE' 
                   ;

commontableexpressionstar: |
                           ',' commontableexpression commontableexpressionstar 
                         ;

tKWITHtKRECURSIVEoptionalcommontableexpressioncommontableexpressionstaroptional: |
                                                                                 't_K_WITH' tKRECURSIVEoptional commontableexpression commontableexpressionstar 
                                                                               ;

tKALLoptional: |
               't_K_ALL' 
             ;

tKUNIONtKALLoptionalortKINTERSECTortKEXCEPT: 't_K_UNION' tKALLoptional |
                                             't_K_INTERSECT' |
                                             't_K_EXCEPT' 
                                           ;

plustKUNIONtKALLoptionalortKINTERSECTortKEXCEPTselectcore: tKUNIONtKALLoptionalortKINTERSECTortKEXCEPT selectcore plustKUNIONtKALLoptionalortKINTERSECTortKEXCEPTselectcore |
                                                           tKUNIONtKALLoptionalortKINTERSECTortKEXCEPT selectcore 
                                                         ;

orderingtermstar: |
                  ',' orderingterm orderingtermstar 
                ;

tKORDERtKBYorderingtermorderingtermstaroptional: |
                                                 't_K_ORDERt_K_BY' orderingterm orderingtermstar 
                                               ;

tKOFFSETor: 't_K_OFFSET' |
            ',' 
          ;

tKOFFSETorexproptional: |
                        tKOFFSETor expr 
                      ;

tKLIMITexprtKOFFSETorexproptionaloptional: |
                                           't_K_LIMIT' expr tKOFFSETorexproptional 
                                         ;

compoundselectstmt: tKWITHtKRECURSIVEoptionalcommontableexpressioncommontableexpressionstaroptional selectcore plustKUNIONtKALLoptionalortKINTERSECTortKEXCEPTselectcore tKORDERtKBYorderingtermorderingtermstaroptional tKLIMITexprtKOFFSETorexproptionaloptional 
                  ;

tKUNIQUEoptional: |
                  't_K_UNIQUE' 
                ;

tKIFtKNOTtKEXISTSoptional: |
                           't_K_IFt_K_NOTt_K_EXISTS' 
                         ;

indexedcolumnstar: |
                   ',' indexedcolumn indexedcolumnstar 
                 ;

tKWHEREexproptional: |
                     't_K_WHERE' expr 
                   ;

createindexstmt: 't_K_CREATE' tKUNIQUEoptional 't_K_INDEX' tKIFtKNOTtKEXISTSoptional databasenameoptional indexname 't_K_ON' tablename indexedcolumn indexedcolumnstar tKWHEREexproptional 
               ;

tKTEMPortKTEMPORARYoptional: |
                             't_K_TEMP' |
                             't_K_TEMPORARY' 
                           ;

columndefstar: |
               ',' columndef columndefstar 
             ;

tableconstraintstar: |
                     ',' tableconstraint tableconstraintstar 
                   ;

tKWITHOUTtIDENTIFIERoptional: |
                              't_K_WITHOUTt_IDENTIFIER' 
                            ;

columndefcolumndefstartableconstraintstartKWITHOUTtIDENTIFIERoptionalortKASselectstmt: columndef columndefstar tableconstraintstar tKWITHOUTtIDENTIFIERoptional |
                                                                                       't_K_AS' selectstmt 
                                                                                     ;

createtablestmt: 't_K_CREATE' tKTEMPortKTEMPORARYoptional 't_K_TABLE' tKIFtKNOTtKEXISTSoptional databasenameoptional tablename columndefcolumndefstartableconstraintstartKWITHOUTtIDENTIFIERoptionalortKASselectstmt 
               ;

tKBEFOREortKAFTERortKINSTEADtKOFoptional: |
                                          't_K_BEFORE' |
                                          't_K_AFTER' |
                                          't_K_INSTEADt_K_OF' 
                                        ;

tKDELETEortKINSERTortKUPDATEtKOFcolumnnamecolumnnamestaroptional: 't_K_DELETE' |
                                                                  't_K_INSERT' |
                                                                  't_K_UPDATE' tKOFcolumnnamecolumnnamestaroptional 
                                                                ;

columnnamestar: |
                ',' columnname columnnamestar 
              ;

tKOFcolumnnamecolumnnamestaroptional: |
                                      't_K_OF' columnname columnnamestar 
                                    ;

tKFORtKEACHtKROWoptional: |
                          't_K_FORt_K_EACHt_K_ROW' 
                        ;

tKWHENexproptional: |
                    't_K_WHEN' expr 
                  ;

updatestmtorinsertstmtordeletestmtorselectstmt: updatestmt |
                                                insertstmt |
                                                deletestmt |
                                                selectstmt 
                                              ;

plusupdatestmtorinsertstmtordeletestmtorselectstmtsemicolon: updatestmtorinsertstmtordeletestmtorselectstmt ';' plusupdatestmtorinsertstmtordeletestmtorselectstmtsemicolon |
                                                             updatestmtorinsertstmtordeletestmtorselectstmt ';' 
                                                           ;

createtriggerstmt: 't_K_CREATE' tKTEMPortKTEMPORARYoptional 't_K_TRIGGER' tKIFtKNOTtKEXISTSoptional databasenameoptional triggername tKBEFOREortKAFTERortKINSTEADtKOFoptional tKDELETEortKINSERTortKUPDATEtKOFcolumnnamecolumnnamestaroptional 't_K_ON' databasenameoptional tablename tKFORtKEACHtKROWoptional tKWHENexproptional 't_K_BEGIN' plusupdatestmtorinsertstmtordeletestmtorselectstmtsemicolon 't_K_END' 
                 ;

createviewstmt: 't_K_CREATE' tKTEMPortKTEMPORARYoptional 't_K_VIEW' tKIFtKNOTtKEXISTSoptional databasenameoptional viewname 't_K_AS' selectstmt 
              ;

moduleargumentstar: |
                    ',' moduleargument moduleargumentstar 
                  ;

moduleargumentmoduleargumentstaroptional: |
                                          moduleargument moduleargumentstar 
                                        ;

createvirtualtablestmt: 't_K_CREATEt_K_VIRTUALt_K_TABLE' tKIFtKNOTtKEXISTSoptional databasenameoptional tablename 't_K_USING' modulename moduleargumentmoduleargumentstaroptional 
                      ;

withclauseoptional: |
                    withclause 
                  ;

deletestmt: withclauseoptional 't_K_DELETEt_K_FROM' qualifiedtablename tKWHEREexproptional 
          ;

tKORDERtKBYorderingtermorderingtermstaroptionaltKLIMITexprtKOFFSETorexproptionaloptional: |
                                                                                          tKORDERtKBYorderingtermorderingtermstaroptional 't_K_LIMIT' expr tKOFFSETorexproptional 
                                                                                        ;

deletestmtlimited: withclauseoptional 't_K_DELETEt_K_FROM' qualifiedtablename tKWHEREexproptional tKORDERtKBYorderingtermorderingtermstaroptionaltKLIMITexprtKOFFSETorexproptionaloptional 
                 ;

detachstmt: 't_K_DETACH' tKDATABASEoptional databasename 
          ;

tKIFtKEXISTSoptional: |
                      't_K_IFt_K_EXISTS' 
                    ;

dropindexstmt: 't_K_DROPt_K_INDEX' tKIFtKEXISTSoptional databasenameoptional indexname 
             ;

droptablestmt: 't_K_DROPt_K_TABLE' tKIFtKEXISTSoptional databasenameoptional tablename 
             ;

droptriggerstmt: 't_K_DROPt_K_TRIGGER' tKIFtKEXISTSoptional databasenameoptional triggername 
               ;

dropviewstmt: 't_K_DROPt_K_VIEW' tKIFtKEXISTSoptional databasenameoptional viewname 
            ;

compoundoperatorselectcorestar: |
                                compoundoperator selectcore compoundoperatorselectcorestar 
                              ;

factoredselectstmt: tKWITHtKRECURSIVEoptionalcommontableexpressioncommontableexpressionstaroptional selectcore compoundoperatorselectcorestar tKORDERtKBYorderingtermorderingtermstaroptional tKLIMITexprtKOFFSETorexproptionaloptional 
                  ;

tKINSERTortKREPLACEortKINSERTtKORtKREPLACEortKINSERTtKORtKROLLBACKortKINSERTtKORtKABORTortKINSERTtKORtKFAILortKINSERTtKORtKIGNORE: 't_K_INSERT' |
                                                                                                                                   't_K_REPLACE' |
                                                                                                                                   't_K_INSERTt_K_ORt_K_REPLACE' |
                                                                                                                                   't_K_INSERTt_K_ORt_K_ROLLBACK' |
                                                                                                                                   't_K_INSERTt_K_ORt_K_ABORT' |
                                                                                                                                   't_K_INSERTt_K_ORt_K_FAIL' |
                                                                                                                                   't_K_INSERTt_K_ORt_K_IGNORE' 
                                                                                                                                 ;

columnnamecolumnnamestaroptional: |
                                  columnname columnnamestar 
                                ;

exprstar: |
          ',' expr exprstar 
        ;

exprexprstarstar: |
                  ',' expr exprstar exprexprstarstar 
                ;

tKVALUESexprexprstarexprexprstarstarorselectstmtortKDEFAULTtKVALUES: 't_K_VALUES' expr exprstar exprexprstarstar |
                                                                     selectstmt |
                                                                     't_K_DEFAULTt_K_VALUES' 
                                                                   ;

insertstmt: withclauseoptional tKINSERTortKREPLACEortKINSERTtKORtKREPLACEortKINSERTtKORtKROLLBACKortKINSERTtKORtKABORTortKINSERTtKORtKFAILortKINSERTtKORtKIGNORE 't_K_INTO' databasenameoptional tablename columnnamecolumnnamestaroptional tKVALUESexprexprstarexprexprstarstarorselectstmtortKDEFAULTtKVALUES 
          ;

equalpragmavalueorpragmavalueoptional: |
                                       '=' pragmavalue |
                                       pragmavalue 
                                     ;

pragmastmt: 't_K_PRAGMA' databasenameoptional pragmaname equalpragmavalueorpragmavalueoptional 
          ;

collationnameordatabasenameoptionaltablenameorindexnameoptional: |
                                                                 collationname |
                                                                 databasenameoptional tablenameorindexname 
                                                               ;

tablenameorindexname: tablename |
                      indexname 
                    ;

reindexstmt: 't_K_REINDEX' collationnameordatabasenameoptionaltablenameorindexnameoptional 
           ;

tKSAVEPOINToptional: |
                     't_K_SAVEPOINT' 
                   ;

releasestmt: 't_K_RELEASE' tKSAVEPOINToptional savepointname 
           ;

tKTOtKSAVEPOINToptionalsavepointnameoptional: |
                                              't_K_TO' tKSAVEPOINToptional savepointname 
                                            ;

rollbackstmt: 't_K_ROLLBACK' tKTRANSACTIONtransactionnameoptionaloptional tKTOtKSAVEPOINToptionalsavepointnameoptional 
            ;

savepointstmt: 't_K_SAVEPOINT' savepointname 
             ;

simpleselectstmt: tKWITHtKRECURSIVEoptionalcommontableexpressioncommontableexpressionstaroptional selectcore tKORDERtKBYorderingtermorderingtermstaroptional tKLIMITexprtKOFFSETorexproptionaloptional 
                ;

compoundoperatorselectorvaluesstar: |
                                    compoundoperator selectorvalues compoundoperatorselectorvaluesstar 
                                  ;

selectstmt: tKWITHtKRECURSIVEoptionalcommontableexpressioncommontableexpressionstaroptional selectorvalues compoundoperatorselectorvaluesstar tKORDERtKBYorderingtermorderingtermstaroptional tKLIMITexprtKOFFSETorexproptionaloptional 
          ;

tKDISTINCTortKALLoptional: |
                           't_K_DISTINCT' |
                           't_K_ALL' 
                         ;

resultcolumnstar: |
                  ',' resultcolumn resultcolumnstar 
                ;

tableorsubquerystar: |
                     ',' tableorsubquery tableorsubquerystar 
                   ;

tableorsubquerytableorsubquerystarorjoinclause: tableorsubquery tableorsubquerystar |
                                                joinclause 
                                              ;

tKFROMtableorsubquerytableorsubquerystarorjoinclauseoptional: |
                                                              't_K_FROM' tableorsubquerytableorsubquerystarorjoinclause 
                                                            ;

tKHAVINGexproptional: |
                      't_K_HAVING' expr 
                    ;

tKGROUPtKBYexprexprstartKHAVINGexproptionaloptional: |
                                                     't_K_GROUPt_K_BY' expr exprstar tKHAVINGexproptional 
                                                   ;

selectorvalues: 't_K_SELECT' tKDISTINCTortKALLoptional resultcolumn resultcolumnstar tKFROMtableorsubquerytableorsubquerystarorjoinclauseoptional tKWHEREexproptional tKGROUPtKBYexprexprstartKHAVINGexproptionaloptional |
                't_K_VALUES' expr exprstar exprexprstarstar 
              ;

tKORtKROLLBACKortKORtKABORTortKORtKREPLACEortKORtKFAILortKORtKIGNOREoptional: |
                                                                              't_K_ORt_K_ROLLBACK' |
                                                                              't_K_ORt_K_ABORT' |
                                                                              't_K_ORt_K_REPLACE' |
                                                                              't_K_ORt_K_FAIL' |
                                                                              't_K_ORt_K_IGNORE' 
                                                                            ;

columnnameequalexprstar: |
                         ',' columnname '=' expr columnnameequalexprstar 
                       ;

updatestmt: withclauseoptional 't_K_UPDATE' tKORtKROLLBACKortKORtKABORTortKORtKREPLACEortKORtKFAILortKORtKIGNOREoptional qualifiedtablename 't_K_SET' columnname '=' expr columnnameequalexprstar tKWHEREexproptional 
          ;

updatestmtlimited: withclauseoptional 't_K_UPDATE' tKORtKROLLBACKortKORtKABORTortKORtKREPLACEortKORtKFAILortKORtKIGNOREoptional qualifiedtablename 't_K_SET' columnname '=' expr columnnameequalexprstar tKWHEREexproptional tKORDERtKBYorderingtermorderingtermstaroptionaltKLIMITexprtKOFFSETorexproptionaloptional 
                 ;

vacuumstmt: 't_K_VACUUM' 
          ;

typenameoptional: |
                  typename 
                ;

columnconstraintstar: |
                      columnconstraint columnconstraintstar 
                    ;

columndef: columnname typenameoptional columnconstraintstar 
         ;

plusname: name plusname |
          name 
        ;

signednumberorsignednumbersignednumberoptional: |
                                                signednumber |
                                                signednumber ',' signednumber 
                                              ;

typename: plusname signednumberorsignednumbersignednumberoptional 
        ;

tKCONSTRAINTnameoptional: |
                          't_K_CONSTRAINT' name 
                        ;

tKASCortKDESCoptional: |
                       't_K_ASC' |
                       't_K_DESC' 
                     ;

tKAUTOINCREMENToptional: |
                         't_K_AUTOINCREMENT' 
                       ;

tKPRIMARYtKKEYtKASCortKDESCoptionalconflictclausetKAUTOINCREMENToptionalortKNOToptionaltKNULLconflictclauseortKUNIQUEconflictclauseortKCHECKexprortKDEFAULTsignednumberorliteralvalueorexprortKCOLLATEcollationnameorforeignkeyclause: 't_K_PRIMARYt_K_KEY' tKASCortKDESCoptional conflictclause tKAUTOINCREMENToptional |
                                                                                                                                                                                                                                       tKNOToptional 't_K_NULL' conflictclause |
                                                                                                                                                                                                                                       't_K_UNIQUE' conflictclause |
                                                                                                                                                                                                                                       't_K_CHECK' expr |
                                                                                                                                                                                                                                       't_K_DEFAULT' signednumberorliteralvalueorexpr |
                                                                                                                                                                                                                                       't_K_COLLATE' collationname |
                                                                                                                                                                                                                                       foreignkeyclause 
                                                                                                                                                                                                                                     ;

tKNOToptional: |
               't_K_NOT' 
             ;

signednumberorliteralvalueorexpr: signednumber |
                                  literalvalue |
                                  expr 
                                ;

columnconstraint: tKCONSTRAINTnameoptional tKPRIMARYtKKEYtKASCortKDESCoptionalconflictclausetKAUTOINCREMENToptionalortKNOToptionaltKNULLconflictclauseortKUNIQUEconflictclauseortKCHECKexprortKDEFAULTsignednumberorliteralvalueorexprortKCOLLATEcollationnameorforeignkeyclause 
                ;

tKROLLBACKortKABORTortKFAILortKIGNOREortKREPLACE: 't_K_ROLLBACK' |
                                                  't_K_ABORT' |
                                                  't_K_FAIL' |
                                                  't_K_IGNORE' |
                                                  't_K_REPLACE' 
                                                ;

tKONtKCONFLICTtKROLLBACKortKABORTortKFAILortKIGNOREortKREPLACEoptional: |
                                                                        't_K_ONt_K_CONFLICT' tKROLLBACKortKABORTortKFAILortKIGNOREortKREPLACE 
                                                                      ;

conflictclause: tKONtKCONFLICTtKROLLBACKortKABORTortKFAILortKIGNOREortKREPLACEoptional 
              ;

expr: literalvalue |
      't_BIND_PARAMETER' |
      databasenameoptionaltablenameoptional columnname |
      unaryoperator expr |
      expr '||' expr |
      expr starordivorpercent expr |
      expr plusorminus expr |
      expr ltltorgtgtorandoror expr |
      expr ltorltequalorgtorgtequal expr |
      expr equalorequalequalor!equalorltgtortKISortKIStKNOTortKINortKLIKEortKGLOBortKMATCHortKREGEXP expr |
      expr 't_K_AND' expr |
      expr 't_K_OR' expr |
      functionname tKDISTINCToptionalexprexprstarorstaroptional |
      expr |
      't_K_CAST' expr 't_K_AS' typename |
      expr 't_K_COLLATE' collationname |
      expr tKNOToptional tKLIKEortKGLOBortKREGEXPortKMATCH expr tKESCAPEexproptional |
      expr tKISNULLortKNOTNULLortKNOTtKNULL |
      expr 't_K_IS' tKNOToptional expr |
      expr tKNOToptional 't_K_BETWEEN' expr 't_K_AND' expr |
      expr tKNOToptional 't_K_IN' selectstmtorexprexprstaroptionalordatabasenameoptionaltablename |
      tKNOToptionaltKEXISTSoptional selectstmt |
      't_K_CASE' exproptional plustKWHENexprtKTHENexpr tKELSEexproptional 't_K_END' |
      raisefunction 
    ;

databasenameoptionaltablenameoptional: |
                                       databasenameoptional tablename '.' 
                                     ;

starordivorpercent: '*' |
                    '/' |
                    '%' 
                  ;

plusorminus: '+' |
             '-' 
           ;

ltltorgtgtorandoror: '<<' |
                     '>>' |
                     '&' |
                     ' | ' 
                   ;

ltorltequalorgtorgtequal: '<' |
                          '<=' |
                          '>' |
                          '>=' 
                        ;

equalorequalequalor!equalorltgtortKISortKIStKNOTortKINortKLIKEortKGLOBortKMATCHortKREGEXP: '=' |
                                                                                           '==' |
                                                                                           '!=' |
                                                                                           '<>' |
                                                                                           't_K_IS' |
                                                                                           't_K_ISt_K_NOT' |
                                                                                           't_K_IN' |
                                                                                           't_K_LIKE' |
                                                                                           't_K_GLOB' |
                                                                                           't_K_MATCH' |
                                                                                           't_K_REGEXP' 
                                                                                         ;

tKDISTINCToptional: |
                    't_K_DISTINCT' 
                  ;

tKDISTINCToptionalexprexprstarorstaroptional: |
                                              tKDISTINCToptional expr exprstar |
                                              '*' 
                                            ;

tKLIKEortKGLOBortKREGEXPortKMATCH: 't_K_LIKE' |
                                   't_K_GLOB' |
                                   't_K_REGEXP' |
                                   't_K_MATCH' 
                                 ;

tKESCAPEexproptional: |
                      't_K_ESCAPE' expr 
                    ;

tKISNULLortKNOTNULLortKNOTtKNULL: 't_K_ISNULL' |
                                  't_K_NOTNULL' |
                                  't_K_NOTt_K_NULL' 
                                ;

selectstmtorexprexprstaroptional: |
                                  selectstmt |
                                  expr exprstar 
                                ;

selectstmtorexprexprstaroptionalordatabasenameoptionaltablename: selectstmtorexprexprstaroptional |
                                                                 databasenameoptional tablename 
                                                               ;

tKNOToptionaltKEXISTSoptional: |
                               tKNOToptional 't_K_EXISTS' 
                             ;

exproptional: |
              expr 
            ;

plustKWHENexprtKTHENexpr: 't_K_WHEN' expr 't_K_THEN' expr plustKWHENexprtKTHENexpr |
                          't_K_WHEN' expr 't_K_THEN' expr 
                        ;

tKELSEexproptional: |
                    't_K_ELSE' expr 
                  ;

tKDELETEortKUPDATE: 't_K_DELETE' |
                    't_K_UPDATE' 
                  ;

tKSETtKNULLortKSETtKDEFAULTortKCASCADEortKRESTRICTortKNOtKACTION: 't_K_SETt_K_NULL' |
                                                                  't_K_SETt_K_DEFAULT' |
                                                                  't_K_CASCADE' |
                                                                  't_K_RESTRICT' |
                                                                  't_K_NOt_K_ACTION' 
                                                                ;

tKONtKDELETEortKUPDATEtKSETtKNULLortKSETtKDEFAULTortKCASCADEortKRESTRICTortKNOtKACTIONortKMATCHname: 't_K_ON' tKDELETEortKUPDATE tKSETtKNULLortKSETtKDEFAULTortKCASCADEortKRESTRICTortKNOtKACTION |
                                                                                                     't_K_MATCH' name 
                                                                                                   ;

tKONtKDELETEortKUPDATEtKSETtKNULLortKSETtKDEFAULTortKCASCADEortKRESTRICTortKNOtKACTIONortKMATCHnamestar: |
                                                                                                         tKONtKDELETEortKUPDATEtKSETtKNULLortKSETtKDEFAULTortKCASCADEortKRESTRICTortKNOtKACTIONortKMATCHname tKONtKDELETEortKUPDATEtKSETtKNULLortKSETtKDEFAULTortKCASCADEortKRESTRICTortKNOtKACTIONortKMATCHnamestar 
                                                                                                       ;

tKINITIALLYtKDEFERREDortKINITIALLYtKIMMEDIATEoptional: |
                                                       't_K_INITIALLYt_K_DEFERRED' |
                                                       't_K_INITIALLYt_K_IMMEDIATE' 
                                                     ;

tKNOToptionaltKDEFERRABLEtKINITIALLYtKDEFERREDortKINITIALLYtKIMMEDIATEoptionaloptional: |
                                                                                        tKNOToptional 't_K_DEFERRABLE' tKINITIALLYtKDEFERREDortKINITIALLYtKIMMEDIATEoptional 
                                                                                      ;

foreignkeyclause: 't_K_REFERENCES' foreigntable columnnamecolumnnamestaroptional tKONtKDELETEortKUPDATEtKSETtKNULLortKSETtKDEFAULTortKCASCADEortKRESTRICTortKNOtKACTIONortKMATCHnamestar tKNOToptionaltKDEFERRABLEtKINITIALLYtKDEFERREDortKINITIALLYtKIMMEDIATEoptionaloptional 
                ;

tKIGNOREortKROLLBACKortKABORTortKFAILerrormessage: 't_K_IGNORE' |
                                                   tKROLLBACKortKABORTortKFAIL ',' errormessage 
                                                 ;

tKROLLBACKortKABORTortKFAIL: 't_K_ROLLBACK' |
                             't_K_ABORT' |
                             't_K_FAIL' 
                           ;

raisefunction: 't_K_RAISE' tKIGNOREortKROLLBACKortKABORTortKFAILerrormessage 
             ;

tKCOLLATEcollationnameoptional: |
                                't_K_COLLATE' collationname 
                              ;

indexedcolumn: columnname tKCOLLATEcollationnameoptional tKASCortKDESCoptional 
             ;

tKPRIMARYtKKEYortKUNIQUE: 't_K_PRIMARYt_K_KEY' |
                          't_K_UNIQUE' 
                        ;

tKPRIMARYtKKEYortKUNIQUEindexedcolumnindexedcolumnstarconflictclauseortKCHECKexprortKFOREIGNtKKEYcolumnnamecolumnnamestarforeignkeyclause: tKPRIMARYtKKEYortKUNIQUE indexedcolumn indexedcolumnstar conflictclause |
                                                                                                                                           't_K_CHECK' expr |
                                                                                                                                           't_K_FOREIGNt_K_KEY' columnname columnnamestar foreignkeyclause 
                                                                                                                                         ;

tableconstraint: tKCONSTRAINTnameoptional tKPRIMARYtKKEYortKUNIQUEindexedcolumnindexedcolumnstarconflictclauseortKCHECKexprortKFOREIGNtKKEYcolumnnamecolumnnamestarforeignkeyclause 
               ;

ctetablenametKASselectstmtstar: |
                                ',' ctetablename 't_K_AS' selectstmt ctetablenametKASselectstmtstar 
                              ;

withclause: 't_K_WITH' tKRECURSIVEoptional ctetablename 't_K_AS' selectstmt ctetablenametKASselectstmtstar 
          ;

tKINDEXEDtKBYindexnameortKNOTtKINDEXEDoptional: |
                                                't_K_INDEXEDt_K_BY' indexname |
                                                't_K_NOTt_K_INDEXED' 
                                              ;

qualifiedtablename: databasenameoptional tablename tKINDEXEDtKBYindexnameortKNOTtKINDEXEDoptional 
                  ;

orderingterm: expr tKCOLLATEcollationnameoptional tKASCortKDESCoptional 
            ;

pragmavalue: signednumber |
             name |
             't_STRING_LITERAL' 
           ;

commontableexpression: tablename columnnamecolumnnamestaroptional 't_K_AS' selectstmt 
                     ;

resultcolumn: '*' |
              tablename '.*' |
              expr tKASoptionalcolumnaliasoptional 
            ;

tKASoptional: |
              't_K_AS' 
            ;

tKASoptionalcolumnaliasoptional: |
                                 tKASoptional columnalias 
                               ;

tKASoptionaltablealiasoptional: |
                                tKASoptional tablealias 
                              ;

tableorsubquery: databasenameoptional tablename tKASoptionaltablealiasoptional tKINDEXEDtKBYindexnameortKNOTtKINDEXEDoptional |
                 tableorsubquerytableorsubquerystarorjoinclause tKASoptionaltablealiasoptional |
                 selectstmt tKASoptionaltablealiasoptional 
               ;

joinoperatortableorsubqueryjoinconstraintstar: |
                                               joinoperator tableorsubquery joinconstraint joinoperatortableorsubqueryjoinconstraintstar 
                                             ;

joinclause: tableorsubquery joinoperatortableorsubqueryjoinconstraintstar 
          ;

joinoperator: ',' |
              tKNATURALoptional tKLEFTtKOUTERoptionalortKINNERortKCROSSoptional 't_K_JOIN' 
            ;

tKNATURALoptional: |
                   't_K_NATURAL' 
                 ;

tKOUTERoptional: |
                 't_K_OUTER' 
               ;

tKLEFTtKOUTERoptionalortKINNERortKCROSSoptional: |
                                                 't_K_LEFT' tKOUTERoptional |
                                                 't_K_INNER' |
                                                 't_K_CROSS' 
                                               ;

tKONexprortKUSINGcolumnnamecolumnnamestaroptional: |
                                                   't_K_ON' expr |
                                                   't_K_USING' columnname columnnamestar 
                                                 ;

joinconstraint: tKONexprortKUSINGcolumnnamecolumnnamestaroptional 
              ;

selectcore: 't_K_SELECT' tKDISTINCTortKALLoptional resultcolumn resultcolumnstar tKFROMtableorsubquerytableorsubquerystarorjoinclauseoptional tKWHEREexproptional tKGROUPtKBYexprexprstartKHAVINGexproptionaloptional |
            't_K_VALUES' expr exprstar exprexprstarstar 
          ;

compoundoperator: 't_K_UNION' |
                  't_K_UNIONt_K_ALL' |
                  't_K_INTERSECT' |
                  't_K_EXCEPT' 
                ;

ctetablename: tablename columnnamecolumnnamestaroptional 
            ;

plusorminusoptional: |
                     '+' |
                     '-' 
                   ;

signednumber: plusorminusoptional 't_NUMERIC_LITERAL' 
            ;

literalvalue: 't_NUMERIC_LITERAL' |
              't_STRING_LITERAL' |
              't_BLOB_LITERAL' |
              't_K_NULL' |
              't_K_CURRENT_TIME' |
              't_K_CURRENT_DATE' |
              't_K_CURRENT_TIMESTAMP' 
            ;

unaryoperator: '-' |
               '+' |
               '~' |
               't_K_NOT' 
             ;

errormessage: 't_STRING_LITERAL' 
            ;

moduleargument: expr |
                columndef 
              ;

columnalias: 't_IDENTIFIER' |
             't_STRING_LITERAL' 
           ;

keyword: 't_K_ABORT' |
         't_K_ACTION' |
         't_K_ADD' |
         't_K_AFTER' |
         't_K_ALL' |
         't_K_ALTER' |
         't_K_ANALYZE' |
         't_K_AND' |
         't_K_AS' |
         't_K_ASC' |
         't_K_ATTACH' |
         't_K_AUTOINCREMENT' |
         't_K_BEFORE' |
         't_K_BEGIN' |
         't_K_BETWEEN' |
         't_K_BY' |
         't_K_CASCADE' |
         't_K_CASE' |
         't_K_CAST' |
         't_K_CHECK' |
         't_K_COLLATE' |
         't_K_COLUMN' |
         't_K_COMMIT' |
         't_K_CONFLICT' |
         't_K_CONSTRAINT' |
         't_K_CREATE' |
         't_K_CROSS' |
         't_K_CURRENT_DATE' |
         't_K_CURRENT_TIME' |
         't_K_CURRENT_TIMESTAMP' |
         't_K_DATABASE' |
         't_K_DEFAULT' |
         't_K_DEFERRABLE' |
         't_K_DEFERRED' |
         't_K_DELETE' |
         't_K_DESC' |
         't_K_DETACH' |
         't_K_DISTINCT' |
         't_K_DROP' |
         't_K_EACH' |
         't_K_ELSE' |
         't_K_END' |
         't_K_ESCAPE' |
         't_K_EXCEPT' |
         't_K_EXCLUSIVE' |
         't_K_EXISTS' |
         't_K_EXPLAIN' |
         't_K_FAIL' |
         't_K_FOR' |
         't_K_FOREIGN' |
         't_K_FROM' |
         't_K_FULL' |
         't_K_GLOB' |
         't_K_GROUP' |
         't_K_HAVING' |
         't_K_IF' |
         't_K_IGNORE' |
         't_K_IMMEDIATE' |
         't_K_IN' |
         't_K_INDEX' |
         't_K_INDEXED' |
         't_K_INITIALLY' |
         't_K_INNER' |
         't_K_INSERT' |
         't_K_INSTEAD' |
         't_K_INTERSECT' |
         't_K_INTO' |
         't_K_IS' |
         't_K_ISNULL' |
         't_K_JOIN' |
         't_K_KEY' |
         't_K_LEFT' |
         't_K_LIKE' |
         't_K_LIMIT' |
         't_K_MATCH' |
         't_K_NATURAL' |
         't_K_NO' |
         't_K_NOT' |
         't_K_NOTNULL' |
         't_K_NULL' |
         't_K_OF' |
         't_K_OFFSET' |
         't_K_ON' |
         't_K_OR' |
         't_K_ORDER' |
         't_K_OUTER' |
         't_K_PLAN' |
         't_K_PRAGMA' |
         't_K_PRIMARY' |
         't_K_QUERY' |
         't_K_RAISE' |
         't_K_RECURSIVE' |
         't_K_REFERENCES' |
         't_K_REGEXP' |
         't_K_REINDEX' |
         't_K_RELEASE' |
         't_K_RENAME' |
         't_K_REPLACE' |
         't_K_RESTRICT' |
         't_K_RIGHT' |
         't_K_ROLLBACK' |
         't_K_ROW' |
         't_K_SAVEPOINT' |
         't_K_SELECT' |
         't_K_SET' |
         't_K_TABLE' |
         't_K_TEMP' |
         't_K_TEMPORARY' |
         't_K_THEN' |
         't_K_TO' |
         't_K_TRANSACTION' |
         't_K_TRIGGER' |
         't_K_UNION' |
         't_K_UNIQUE' |
         't_K_UPDATE' |
         't_K_USING' |
         't_K_VACUUM' |
         't_K_VALUES' |
         't_K_VIEW' |
         't_K_VIRTUAL' |
         't_K_WHEN' |
         't_K_WHERE' |
         't_K_WITH' |
         't_K_WITHOUT' 
       ;

name: anyname 
    ;

functionname: anyname 
            ;

databasename: anyname 
            ;

tablename: anyname 
         ;

tableorindexname: anyname 
                ;

newtablename: anyname 
            ;

columnname: anyname 
          ;

collationname: anyname 
             ;

foreigntable: anyname 
            ;

indexname: anyname 
         ;

triggername: anyname 
           ;

viewname: anyname 
        ;

modulename: anyname 
          ;

pragmaname: anyname 
          ;

savepointname: anyname 
             ;

tablealias: anyname 
          ;

transactionname: anyname 
               ;

anyname: 't_IDENTIFIER' |
         keyword |
         't_STRING_LITERAL' |
         anyname 
       ;


%%

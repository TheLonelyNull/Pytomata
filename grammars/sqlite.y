%%

AA: 'begin_of_file' AB 'end_of_file' 
  ;

AC: |
    ';' AC 
  ;

AE: ';' AE |
    ';' 
  ;

AD: |
    AE AF AD 
  ;

AB: AC AF AD AC 
  ;

AH: |
    't_K_QUERYt_K_PLAN' 
  ;

AG: |
    't_K_EXPLAIN' AH 
  ;

AI: AJ |
    AN |
    AP |
    AR |
    AV |
    AX |
    BJ |
    BO |
    BU |
    CD |
    CE |
    CH |
    CJ |
    CL |
    CM |
    CO |
    CP |
    CQ |
    CR |
    CT |
    CZ |
    DB |
    DE |
    DG |
    DI |
    DJ |
    DK |
    DU |
    DX |
    DY 
  ;

AF: AG AI 
  ;

AK: |
    HD '.' 
  ;

AL: 't_K_RENAMEt_K_TO' HG |
    't_K_ADD' AM DZ 
  ;

AM: |
    't_K_COLUMN' 
  ;

AJ: 't_K_ALTERt_K_TABLE' AK HE AL 
  ;

AO: |
    HD |
    HF |
    HD '.' HF 
  ;

AN: 't_K_ANALYZE' AO 
  ;

AQ: |
    't_K_DATABASE' 
  ;

AP: 't_K_ATTACH' AQ EP 't_K_AS' HD 
  ;

AS: |
    't_K_DEFERRED' |
    't_K_IMMEDIATE' |
    't_K_EXCLUSIVE' 
  ;

AU: |
    HR 
  ;

AT: |
    't_K_TRANSACTION' AU 
  ;

AR: 't_K_BEGIN' AS AT 
  ;

AW: 't_K_COMMIT' |
    't_K_END' 
  ;

AV: AW AT 
  ;

AZ: |
    't_K_RECURSIVE' 
  ;

BA: |
    ',' GC BA 
  ;

AY: |
    't_K_WITH' AZ GC BA 
  ;

BD: |
    't_K_ALL' 
  ;

BC: 't_K_UNION' BD |
    't_K_INTERSECT' |
    't_K_EXCEPT' 
  ;

BB: BC GQ BB |
    BC GQ 
  ;

BF: |
    ',' GA BF 
  ;

BE: |
    't_K_ORDERt_K_BY' GA BF 
  ;

BI: 't_K_OFFSET' |
    ',' 
  ;

BH: |
    BI EP 
  ;

BG: |
    't_K_LIMIT' EP BH 
  ;

AX: AY GQ BB BE BG 
  ;

BK: |
    't_K_UNIQUE' 
  ;

BL: |
    't_K_IFt_K_NOTt_K_EXISTS' 
  ;

BM: |
    ',' FR BM 
  ;

BN: |
    't_K_WHERE' EP 
  ;

BJ: 't_K_CREATE' BK 't_K_INDEX' BL AK HK 't_K_ON' HE FR BM BN 
  ;

BP: |
    't_K_TEMP' |
    't_K_TEMPORARY' 
  ;

BR: |
    ',' DZ BR 
  ;

BS: |
    ',' FT BS 
  ;

BT: |
    't_K_WITHOUT' t_id
  ;

BQ: DZ BR BS BT |
    't_K_AS' DK 
  ;

BO: 't_K_CREATE' BP 't_K_TABLE' BL AK HE BQ 
  ;

BV: |
    't_K_BEFORE' |
    't_K_AFTER' |
    't_K_INSTEADt_K_OF' 
  ;

BW: 't_K_DELETE' |
    't_K_INSERT' |
    't_K_UPDATE' BX 
  ;

BY: |
    ',' HH BY 
  ;

BX: |
    't_K_OF' HH BY 
  ;

BZ: |
    't_K_FORt_K_EACHt_K_ROW' 
  ;

CA: |
    't_K_WHEN' EP 
  ;

CC: DU |
    CT |
    CH |
    DK 
  ;

CB: CC ';' CB |
    CC ';' 
  ;

BU: 't_K_CREATE' BP 't_K_TRIGGER' BL AK HL BV BW 't_K_ON' AK HE BZ CA 't_K_BEGIN' CB 't_K_END' 
  ;

CD: 't_K_CREATE' BP 't_K_VIEW' BL AK HM 't_K_AS' DK 
  ;

CG: |
    ',' GY CG 
  ;

CF: |
    GY CG 
  ;

CE: 't_K_CREATEt_K_VIRTUALt_K_TABLE' BL AK HE 't_K_USING' HN CF 
  ;

CI: |
    FW 
  ;

CH: CI 't_K_DELETEt_K_FROM' FY BN 
  ;

CK: |
    BE 't_K_LIMIT' EP BH 
  ;

CJ: CI 't_K_DELETEt_K_FROM' FY BN CK 
  ;

CL: 't_K_DETACH' AQ HD 
  ;

CN: |
    't_K_IFt_K_EXISTS' 
  ;

CM: 't_K_DROPt_K_INDEX' CN AK HK 
  ;

CO: 't_K_DROPt_K_TABLE' CN AK HE 
  ;

CP: 't_K_DROPt_K_TRIGGER' CN AK HL 
  ;

CQ: 't_K_DROPt_K_VIEW' CN AK HM 
  ;

CS: |
    GR GQ CS 
  ;

CR: AY GQ CS BE BG 
  ;

CU: 't_K_INSERT' |
    't_K_REPLACE' |
    't_K_INSERTt_K_ORt_K_REPLACE' |
    't_K_INSERTt_K_ORt_K_ROLLBACK' |
    't_K_INSERTt_K_ORt_K_ABORT' |
    't_K_INSERTt_K_ORt_K_FAIL' |
    't_K_INSERTt_K_ORt_K_IGNORE' 
  ;

CV: |
    HH BY 
  ;

CX: |
    ',' EP CX 
  ;

CY: |
    ',' EP CX CY 
  ;

CW: 't_K_VALUES' EP CX CY |
    DK |
    't_K_DEFAULTt_K_VALUES' 
  ;

CT: CI CU 't_K_INTO' AK HE CV CW 
  ;

DA: |
    '=' GB |
    GB 
  ;

CZ: 't_K_PRAGMA' AK HO DA 
  ;

DC: |
    HI |
    AK DD 
  ;

DD: HE |
    HK 
  ;

DB: 't_K_REINDEX' DC 
  ;

DF: |
    't_K_SAVEPOINT' 
  ;

DE: 't_K_RELEASE' DF HP 
  ;

DH: |
    't_K_TO' DF HP 
  ;

DG: 't_K_ROLLBACK' AT DH 
  ;

DI: 't_K_SAVEPOINT' HP 
  ;

DJ: AY GQ BE BG 
  ;

DL: |
    GR DM DL 
  ;

DK: AY DM DL BE BG 
  ;

DN: |
    't_K_DISTINCT' |
    't_K_ALL' 
  ;

DO: |
    ',' GD DO 
  ;

DR: |
    ',' GG DR 
  ;

DQ: GG DR |
    GI 
  ;

DP: |
    't_K_FROM' DQ 
  ;

DT: |
    't_K_HAVING' EP 
  ;

DS: |
    't_K_GROUPt_K_BY' EP CX DT 
  ;

DM: 't_K_SELECT' DN GD DO DP BN DS |
    't_K_VALUES' EP CX CY 
  ;

DV: |
    't_K_ORt_K_ROLLBACK' |
    't_K_ORt_K_ABORT' |
    't_K_ORt_K_REPLACE' |
    't_K_ORt_K_FAIL' |
    't_K_ORt_K_IGNORE' 
  ;

DW: |
    ',' HH '=' EP DW 
  ;

DU: CI 't_K_UPDATE' DV FY 't_K_SET' HH '=' EP DW BN 
  ;

DX: CI 't_K_UPDATE' DV FY 't_K_SET' HH '=' EP DW BN CK 
  ;

DY: 't_K_VACUUM' 
  ;

EA: |
    EC 
  ;

EB: |
    EF EB 
  ;

DZ: HH EA EB 
  ;

ED: HB ED |
    HB 
  ;

EE: |
    GT |
    GT ',' GT 
  ;

EC: ED EE 
  ;

EG: |
    't_K_CONSTRAINT' HB 
  ;

EI: |
    't_K_ASC' |
    't_K_DESC' 
  ;

EJ: |
    't_K_AUTOINCREMENT' 
  ;

EH: 't_K_PRIMARYt_K_KEY' EI EM EJ |
    EK 't_K_NULL' EM |
    't_K_UNIQUE' EM |
    't_K_CHECK' EP |
    't_K_DEFAULT' EL |
    't_K_COLLATE' HI |
    FH 
  ;

EK: |
    't_K_NOT' 
  ;

EL: GT |
    GV |
    EP 
  ;

EF: EG EH 
  ;

EO: 't_K_ROLLBACK' |
    't_K_ABORT' |
    't_K_FAIL' |
    't_K_IGNORE' |
    't_K_REPLACE' 
  ;

EN: |
    't_K_ONt_K_CONFLICT' EO 
  ;

EM: EN 
  ;

EP: GV |
    t_bind_parameter |
    EQ HH |
    GW EP |
    EP '||' EP |
    EP ER EP |
    EP ES EP |
    EP ET EP |
    EP EU EP |
    EP EV EP |
    EP 't_K_AND' EP |
    EP 't_K_OR' EP |
    HC EW |
    EP |
    't_K_CAST' EP 't_K_AS' EC |
    EP 't_K_COLLATE' HI |
    EP EK EY EP EZ |
    EP FA |
    EP 't_K_IS' EK EP |
    EP EK 't_K_BETWEEN' EP 't_K_AND' EP |
    EP EK 't_K_IN' FB |
    FD DK |
    't_K_CASE' FE FF FG 't_K_END' |
    FO 
  ;

t_bind_parameter: '?' '0'|
		  ':' t_id|
		  '@' t_id|
		  '$' t_id
		  ;

t_id: 'A';


EQ: |
    AK HE '.' 
  ;

ER: '*' |
    '/' |
    '%' 
  ;

ES: '+' |
    '-' 
  ;

ET: '<<' |
    '>>' |
    '&' |
    ' | ' 
  ;

EU: '<' |
    '<=' |
    '>' |
    '>=' 
  ;

EV: '=' |
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

EX: |
    't_K_DISTINCT' 
  ;

EW: |
    EX EP CX |
    '*' 
  ;

EY: 't_K_LIKE' |
    't_K_GLOB' |
    't_K_REGEXP' |
    't_K_MATCH' 
  ;

EZ: |
    't_K_ESCAPE' EP 
  ;

FA: 't_K_ISNULL' |
    't_K_NOTNULL' |
    't_K_NOTt_K_NULL' 
  ;

FC: |
    DK |
    EP CX 
  ;

FB: FC |
    AK HE 
  ;

FD: |
    EK 't_K_EXISTS' 
  ;

FE: |
    EP 
  ;

FF: 't_K_WHEN' EP 't_K_THEN' EP FF |
    't_K_WHEN' EP 't_K_THEN' EP 
  ;

FG: |
    't_K_ELSE' EP 
  ;

FK: 't_K_DELETE' |
    't_K_UPDATE' 
  ;

FL: 't_K_SETt_K_NULL' |
    't_K_SETt_K_DEFAULT' |
    't_K_CASCADE' |
    't_K_RESTRICT' |
    't_K_NOt_K_ACTION' 
  ;

FJ: 't_K_ON' FK FL |
    't_K_MATCH' HB 
  ;

FI: |
    FJ FI 
  ;

FN: |
    't_K_INITIALLYt_K_DEFERRED' |
    't_K_INITIALLYt_K_IMMEDIATE' 
  ;

FM: |
    EK 't_K_DEFERRABLE' FN 
  ;

FH: 't_K_REFERENCES' HJ CV FI FM 
  ;

FP: 't_K_IGNORE' |
    FQ ',' GX 
  ;

FQ: 't_K_ROLLBACK' |
    't_K_ABORT' |
    't_K_FAIL' 
  ;

FO: 't_K_RAISE' FP 
  ;

FS: |
    't_K_COLLATE' HI 
  ;

FR: HH FS EI 
  ;

FV: 't_K_PRIMARYt_K_KEY' |
    't_K_UNIQUE' 
  ;

FU: FV FR BM EM |
    't_K_CHECK' EP |
    't_K_FOREIGNt_K_KEY' HH BY FH 
  ;

FT: EG FU 
  ;

FX: |
    ',' GS 't_K_AS' DK FX 
  ;

FW: 't_K_WITH' AZ GS 't_K_AS' DK FX 
  ;

FZ: |
    't_K_INDEXEDt_K_BY' HK |
    't_K_NOTt_K_INDEXED' 
  ;

FY: AK HE FZ 
  ;

GA: EP FS EI 
  ;

GB: GT |
    HB |
    't_STRING_LITERAL' 
  ;

GC: HE CV 't_K_AS' DK 
  ;

GD: '*' |
    HE '.*' |
    EP GE 
  ;

GF: |
    't_K_AS' 
  ;

GE: |
    GF GZ 
  ;

GH: |
    GF HQ 
  ;

GG: AK HE GH FZ |
    DQ GH |
    DK GH 
  ;

GJ: |
    GK GG GO GJ 
  ;

GI: GG GJ 
  ;

GK: ',' |
    GL GM 't_K_JOIN' 
  ;

GL: |
    't_K_NATURAL' 
  ;

GN: |
    't_K_OUTER' 
  ;

GM: |
    't_K_LEFT' GN |
    't_K_INNER' |
    't_K_CROSS' 
  ;

GP: |
    't_K_ON' EP |
    't_K_USING' HH BY 
  ;

GO: GP 
  ;

GQ: 't_K_SELECT' DN GD DO DP BN DS |
    't_K_VALUES' EP CX CY 
  ;

GR: 't_K_UNION' |
    't_K_UNIONt_K_ALL' |
    't_K_INTERSECT' |
    't_K_EXCEPT' 
  ;

GS: HE CV 
  ;

GU: |
    '+' |
    '-' 
  ;

GT: GU 't_NUMERIC_LITERAL' 
  ;

GV: 't_NUMERIC_LITERAL' |
    't_STRING_LITERAL' |
    't_BLOB_LITERAL' |
    't_K_NULL' |
    't_K_CURRENT_TIME' |
    't_K_CURRENT_DATE' |
    't_K_CURRENT_TIMESTAMP' 
  ;

GW: '-' |
    '+' |
    '~' |
    't_K_NOT' 
  ;

GX: 't_STRING_LITERAL' 
  ;

GY: EP |
    DZ 
  ;

GZ: t_id |
    't_STRING_LITERAL' 
  ;

HA: 't_K_ABORT' |
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

HB: HS 
  ;

HC: HS 
  ;

HD: HS 
  ;

HE: HS 
  ;

HF: HS 
  ;

HG: HS 
  ;

HH: HS 
  ;

HI: HS 
  ;

HJ: HS 
  ;

HK: HS 
  ;

HL: HS 
  ;

HM: HS 
  ;

HN: HS 
  ;

HO: HS 
  ;

HP: HS 
  ;

HQ: HS 
  ;

HR: HS 
  ;

HS: t_id |
    HA |
    't_STRING_LITERAL' |
    HS 
  ;


%%

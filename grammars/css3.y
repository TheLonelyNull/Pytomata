%%

init_symbol:  stylesheet ;
commentSpaceDoCdc: '/* T Comment */'|
		   'SPACE'|
		   '<!--'|
		   '-->';
CommentSpaceDoCdcStar: commentSpaceDoCdc CommentSpaceDoCdcStar|
 		       ;
charsetCommentSpaceCdoCdcStarStar: charset CommentSpaceDoCdcStar charsetCommentSpaceCdoCdcStarStar|
                                   ;
importsCommentSpaceDoCdcStarStar: imports CommentSpaceDoCdcStar importsCommentSpaceDoCdcStarStar|
                                  ;
namespaceCommentSpaceDoCdcStarStar: namespace_ CommentSpaceDoCdcStar namespaceCommentSpaceDoCdcStarStar|
                                    ;
nestedStatementCommentSpaceDoCdcStarStar: nestedStatement CommentSpaceDoCdcStar nestedStatementCommentSpaceDoCdcStarStar|
                                          ;
stylesheet: ws charsetCommentSpaceCdoCdcStarStar importsCommentSpaceDoCdcStarStar namespaceCommentSpaceDoCdcStarStar nestedStatementCommentSpaceDoCdcStarStar;
charset: '@charset ' ws 'STRING' ws ';' ws|
         '@charset ' ws 'STRING' ws;
stringOrUri: 'STRING'|
             'url(abc.com)';
imports: '@import' ws stringOrUri ws mediaQueryList ';' ws|
         '@import' ws stringOrUri ws ';' ws|
         '@import' ws stringOrUri ws mediaQueryList|
         '@import' ws stringOrUri ws;
namespacePrefixWsOptional: namespacePrefix ws|
                           ;
namespace_: '@namespace' ws namespacePrefixWsOptional stringOrUri ws ';' ws|
            '@namespace' ws namespacePrefixWsOptional stringOrUri ws;
namespacePrefix: ident;
media: '@media' ws mediaQueryList groupRuleBody ws;
commaWsMediaQuieryStar: ',' ws mediaQuery commaWsMediaQuieryStar|
                        ;
mediaQueryCommaWsMediaQueryStar: mediaQuery commaWsMediaQuieryStar|
                                 ;
mediaQueryList: mediaQueryCommaWsMediaQueryStar ws;
mediaOnlyNot: 'only'|
              'not'|
              ;
andWsMediaExpressionStar: 'and' ws mediaExpression andWsMediaExpressionStar|
                          ;
mediaQuery: mediaOnlyNot ws mediaType ws andWsMediaExpressionStar|
            mediaExpression andWsMediaExpressionStar;
mediaType: ident;
colonWsExprOptional: ':' ws expr|
                     ;
mediaExpression: '(' ws mediaFeature colonWsExprOptional ')' ws;
mediaFeature: ident ws;
pseudoPageStar: pseudoPage|
                ;
declarationOption: declaration|
                   ;
semicolonWsDeclaration: ';' ws declarationOption semicolonWsDeclaration|
                        ;
page: '@page' ws pseudoPageStar '{' ws  declarationOption  semicolonWsDeclaration '}' ws;
pseudoPage: ':' ident ws;
commaWsSelectorStar: ',' ws selector commaWsSelectorStar|
                     ;
selectorGroup: selector commaWsSelectorStar;
combinatorSimpleSelectorSequenceWsStar: combinator simpleSelectorSequence ws combinatorSimpleSelectorSequenceWsStar|
                                        ;
selector: simpleSelectorSequence ws combinatorSimpleSelectorSequenceWsStar;
combinator: '+' ws|
            '>' ws|
            '~' ws|
            'SPACE' ws;
typeSelectorOrUniversal: typeSelector|
                         universal;
t_HashOrClassNameAttribPseudoNegation: '#FFF'|
                                       className|
                                       attrib|
                                       pseudo|
                                       negation;
t_HashOrClassNameAttribPseudoNegationStar: t_HashOrClassNameAttribPseudoNegation t_HashOrClassNameAttribPseudoNegationStar|
                                           ;
simpleSelectorSequence: typeSelectorOrUniversal t_HashOrClassNameAttribPseudoNegationStar;
plusHashClassNameAttribPseudoNegation: t_HashOrClassNameAttribPseudoNegation plusHashClassNameAttribPseudoNegation|
                                       t_HashOrClassNameAttribPseudoNegation;
simpleSelectorSequence: plusHashClassNameAttribPseudoNegation;
typeNameSpacePrefixOptional: typeNamespacePrefix|
                             ;
typeSelector: typeNameSpacePrefixOptional elementName;
identStarOptional: ident|
                   '*'|
                   ;
typeNamespacePrefix: identStarOptional '|';
elementName: ident;
universal: typeNameSpacePrefixOptional '*';
className: ';' ident;
prefixMatchSuffixMatchSubstringMatchEqualIncludesDashMatch: '^='|
                                                            '$='|
                                                            '*='|
                                                            '='|
                                                            '~='|
                                                            '|=';
identOrString: ident|
               'STRING';
prefixSuffixSubStringMatchEqualIncludesDashMatchWsIdentStringwsOptional: prefixMatchSuffixMatchSubstringMatchEqualIncludesDashMatch ws identOrString ws|
                                                                         ;
attrib: '[' ws typeNameSpacePrefixOptional ident ws prefixSuffixSubStringMatchEqualIncludesDashMatchWsIdentStringwsOptional ']';
colonOptional: ':'|
               ;
identFunctionalPseudo: ident|
                       functionalPseudo;
pseudo: ':' colonOptional identFunctionalPseudo;
functionalPseudo: 'a (' ws expression ')';
plusMinusDimensionUnknownDimensionNumberStringIdent: '+'|
                                                     '-'|
                                                     '1px'|
                                                     '1 a'|
                                                     '1'|
                                                     'STRING'|
                                                     ident;
plusMinusDimensionUnknownDimensionNumberStringIdentws: plusMinusDimensionUnknownDimensionNumberStringIdent ws plusMinusDimensionUnknownDimensionNumberStringIdentws|
                                                       plusMinusDimensionUnknownDimensionNumberStringIdent ws;
expression: plusMinusDimensionUnknownDimensionNumberStringIdentws;
negation: ': not (' ws negationArg ws ')';
negationArg: typeSelector|
             universal|
             '#FFF'|
             className|
             attrib|
             pseudo;
operator_: '/' ws|
	   ',' ws|
	   'SPACE' ws|
	   '=' ws;
property_: ident ws|
           '-- a' ws|
           '*' ident|
           '_' ident;
declarationListOptional: declarationList|
                         ;
ruleset: selectorGroup '{' ws declarationListOptional '}' ws;
anyStar: any_ anyStar|
         ;
ruleset: anyStar '{' ws declarationListOptional '}' ws;
semiWsStar: ';' ws semiWsStar|
            ;
declarationList: semiWsStar declaration ws semicolonWsDeclaration;
prioOptional: prio|
              ;
declaration: property_ ':' ws expr prioOptional|
             property_ ':' ws value;
prio: '@important' ws;
anyBlockAtkeywordws: any_|
                     block|
                     atKeyword ws;
plusanyblockatkeywordws: anyBlockAtkeywordws plusanyblockatkeywordws|
                         anyBlockAtkeywordws;
value: plusanyblockatkeywordws;
operatorOptional: operator_|
                  ;
operatorOptionalTermStar: operatorOptional term operatorOptionalTermStar|
                          ;
expr: term operatorOptionalTermStar;
term: number ws|
      percentage ws|
      dimension ws|
      'STRING' ws|
      'u+?' ws|
      ident ws|
      var_|
      'url(abc.com)' ws|
      hexcolor|
      calc|
      function_|
      unknownDimension ws|
      dxImageTransform;
function_: 'a (' ws expr ')' ws;
dxImageTransform: 'progid:DXImageTransform.Microsoft. a(' ws expr ')' ws;
hexcolor: '#FFF' ws;
plusMinusOptional: '+'|
                   '-'|
                   ;
number: plusMinusOptional '0';
percentage: plusMinusOptional '0%';
dimension: plusMinusOptional '1px';
unknownDimension: plusMinusOptional '0 a';
any_: ident ws|
      number ws|
      percentage ws|
      dimension ws|
      unknownDimension ws|
      'STRING' ws|
      'url(abc.com)' ws|
      '#FFF' ws|
      'u+?' ws|
      '~=' ws|
      '|=' ws|
      ':' ws;
anyOrUnused: any_|
             unused;
anyOrUnusedStar: anyOrUnused anyOrUnusedStar|
                 ;
any_: 'a (' ws anyOrUnusedStar ')' ws|
      '(' ws anyOrUnusedStar ')' ws|
      '[' ws anyOrUnusedStar ']' ws;
blockOrSemWs: block|
              ';' ws;
atRule: atKeyword ws anyStar blockOrSemWs;
atKeyword:  '@' ident;
unused: block|
        atKeyword ws|
        ';' ws|
        '<!--' ws|
        '-->' ws;
declarationListNestedStatementNayblockAtKeywordwssmews: declarationList|
                                                        nestedStatement|
                                                        any_|
                                                        block|
                                                        atKeyword ws|
                                                        ';' ws;
declarationListNestedStatementNayblockAtKeywordwssmewsStar: declarationListNestedStatementNayblockAtKeywordwssmews declarationListNestedStatementNayblockAtKeywordwssmewsStar|
                                                            ;
block: '{' ws declarationListNestedStatementNayblockAtKeywordwssmewsStar '}' ws;
nestedStatement: ruleset|
                 media|
                 page|
                 fontFaceRule|
                 keyframesRule|
                 supportsRule|
                 viewport|
                 counterStyle|
                 fontFeatureValuesRule|
                 atRule;
nestedStatementStar: nestedStatement nestedStatementStar|
                     ;
groupRuleBody: '{' ws nestedStatementStar '}' ws;
supportsRule: '@supports' ws supportsCondition ws groupRuleBody;
supportsCondition: supportsNegation|
                   supportsConjunction|
                   supportsDisjunction|
                   supportsConditionInParens;
supportsConditionInParens: '(' ws supportsCondition ws ')'|
                           supportsDeclarationCondition|
                           generalEnclosed;
supportsNegation: 'not' ws 'SPACE' ws supportsConditionInParens;
plusWsSpacewsAndSpaceWsSupportConditionInParens: ws 'SPACE' ws 'and' ws 'SPACE' ws supportsConditionInParens plusWsSpacewsAndSpaceWsSupportConditionInParens|
                                                 ws 'SPACE' ws 'and' ws 'SPACE' ws supportsConditionInParens;
supportsConjunction: supportsConditionInParens plusWsSpacewsAndSpaceWsSupportConditionInParens;
pluswsSpacewsOrWsSpacewsSupportsConditionInParens: ws 'SPACE' ws 'or' ws 'SPACE' ws supportsConditionInParens pluswsSpacewsOrWsSpacewsSupportsConditionInParens|
                                                   ws 'SPACE' ws 'or' ws 'SPACE' ws supportsConditionInParens;
supportsDisjunction: supportsConditionInParens pluswsSpacewsOrWsSpacewsSupportsConditionInParens;
supportsDeclarationCondition: '(' ws declaration ')';
functionBack: 'a ('|
              '(';
generalEnclosed: functionBack anyOrUnusedStar ')';
var_: 'var(' ws '-- a' ws ')' ws;
calc: 'calc(' ws calcSum ')' ws;
PlusOrMinus: '+'|
             '-';
spaceWsPlusOrMinusWsSpaceWsCalcProductStar: 'SPACE' ws PlusOrMinus ws 'SPACE' ws calcProduct spaceWsPlusOrMinusWsSpaceWsCalcProductStar|
                                            ;
calcSum: calcProduct spaceWsPlusOrMinusWsSpaceWsCalcProductStar;
starWsCalcValueWsNumberWs: '*' ws calcValue|
                           '/' ws number ws;
starWsCalcValue: starWsCalcValueWsNumberWs starWsCalcValue|
                 ;
calcProduct: calcValue starWsCalcValue;
calcValue: number ws|
           dimension ws|
           unknownDimension ws|
           percentage ws|
           '(' ws calcSum ')' ws;
fontfaceDeclarationOptional: fontFaceDeclaration|
                             ;
wsfontfaceDeclarationOptionalStar: ';' ws fontfaceDeclarationOptional wsfontfaceDeclarationOptionalStar|
                                    ;
fontFaceRule: '@font-face' ws '{' ws fontfaceDeclarationOptional wsfontfaceDeclarationOptionalStar '}' ws;
fontFaceDeclaration: property_ ':' ws expr|
                     property_ ':' ws value;
keyframesRule: '@keyframes' ws 'SPACE' ws ident ws '{' ws keyframesBlocks '}' ws;
keyframSelectorWsDeclationListOptionalWsStar: keyframeSelector '{' ws declarationListOptional '}' ws keyframSelectorWsDeclationListOptionalWsStar|
                                              ;
keyframesBlocks: keyframSelectorWsDeclationListOptionalWsStar;
fromToPercentage: 'from'|
                  'to'|
                  '0%';
commaWsFromToPercentageWsStar: ',' ws fromToPercentage ws commaWsFromToPercentageWsStar|
                               ;
keyframeSelector: fromToPercentage ws commaWsFromToPercentageWsStar;
viewport: '@viewport' ws '{' ws declarationListOptional '}' ws;
counterStyle: '@counter-style' ws ident ws '{' ws declarationListOptional '}' ws;
featureValueBlockStar: featureValueBlock featureValueBlockStar|
                       ;
fontFeatureValuesRule: '@font-features-values' ws fontFamilyNameList ws '{' ws featureValueBlockStar '}' ws;
wsCommaWsFontFamilyNameStar: ws ',' ws fontFamilyName wsCommaWsFontFamilyNameStar|
                             ;
fontFamilyNameList: fontFamilyName wsCommaWsFontFamilyNameStar;
fontFamilyName: 'STRING';
wsIndentStar: ws ident wsIndentStar|
              ;
fontFamilyName: ident wsIndentStar;
featureValueDefinitionOptional: featureValueDefinition|
                                ;
wsSemiWsFeatureValueDefOptionalStar: ws ';' ws featureValueDefinitionOptional wsSemiWsFeatureValueDefOptionalStar|
                                     ;
featureValueBlock: featureType ws '{' ws featureValueDefinitionOptional wsSemiWsFeatureValueDefOptionalStar '}' ws;
featureType: atKeyword;
wsNumberStar: ws number wsNumberStar|
              ;
featureValueDefinition: ident ws ':' ws number wsNumberStar;
ident: 'a'|
       'only'|
       'not'|
       'and'|
       'or'|
       'from'|
       'to';
commentSpace: '/* T Comment */'|
              'SPACE';
commentSpaceStar: commentSpace commentSpaceStar|
                  ;
ws: commentSpaceStar;

%%
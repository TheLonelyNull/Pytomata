%%

initsymbol: 'begin_of_file' value 'end_of_file' 
          ;

value: object 
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

pair: fname |
      lname |
      dob |
      addr |
      age |
      email |
      phones 
    ;

fname: '"first-name":string' 
     ;

lname: '"last-name":string' 
     ;

dob: '"dob":date_string' 
   ;

age: '"age":' integer 
   ;

email: '"email":email_string' 
     ;

addr: '"address":' addrobj 
    ;

phones: '"phones":' phonearray 
      ;

addrmember: streetname |
            streetnum 
          ;

streetname: '"street-name":string' 
          ;

streetnum: '"street-num":string' 
         ;

phonemember: phonelabel |
             phonenum 
           ;

phonelabel: 'label:string' 
          ;

phonenum: 'number:string' 
        ;

integer: '0' |
         digit19 digitstar 
       ;

digitstar: |
           digit digitstar 
         ;

addrmembersoptional: |
                     addrmembers 
                   ;

addrobj: '{' addrmembersoptional '}' 
       ;

addrmembersstar: |
                 ',' addrmembers addrmembersstar 
               ;

addrmembers: addrmember addrmembersstar 
           ;

phoneelementsoptional: |
                       phoneelements 
                     ;

phonearray: '[' phoneelementsoptional ']' 
          ;

phoneobjstar: |
              ',' phoneobj phoneobjstar 
            ;

phoneelements: phoneobj phoneobjstar 
             ;

phonemembersoptional: |
                      phonemembers 
                    ;

phoneobj: '{' phonemembersoptional '}' 
        ;

phonemembersstar: |
                  ',' phonemembers phonemembersstar 
                ;

phonemembers: phonemember phonemembersstar 
            ;

digit: '0'
     ;

digit19: '1' |
         '2' |
         '3' |
         '4' |
         '5' |
         '6' |
         '7' |
         '8' |
         '9' 
       ;


%%

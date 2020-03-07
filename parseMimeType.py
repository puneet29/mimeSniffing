s = input()

http_code_points = set(['!', '#', '$', '%', '&', '\'', '*', '+', '-', '.', '^', '_', '`', '|', '~'])

http_quoted_points = set(['\u0009'] + [chr(i) for i in range(ord('\u0020'), ord('\u007E')+1)] + [chr(i) for i in range(ord('\u0080'), ord('\u00FF')+1)])

http_whitespace = set(['\u000A', '\u000D', '\u0009', '\u0020'])

# Removing leading and tailing whitespaces
for i in range(len(s)-1, -1, -1):
    if(s[i] in http_whitespace):
        s = s[:-1]
for i in range(len(s)):
    if(s[i] in http_whitespace):
        s = s[1:]

# Getting type and subtype
_type = s.split('/')[0]
_subtype = ''.join(s.split('/')[1:]).split(';')[0]

# Remove trailing whitespace from subtype
for i in range(len(_subtype)-1, -1, -1):
    if(_subtype[i] in http_whitespace):
        _subtype = _subtype[:-1]

# Check if type or subtype are empty strings
if(_type=='' or _subtype==''):
    raise Exception('Failure')

# Check if there are any non HTTP token code points in type or 
# subtype
for i in _type:
    if(i not in http_code_points and not i.isalnum()):
        raise Exception('Failure')
for i in _subtype:
    if(i not in http_code_points and not i.isalnum()):
        raise Exception('Failure')

# Make mimeType
mimeType = {'type': _type.lower(), 'subtype':  _subtype.lower(), 'parameters': {}}

position = s.index(';')

while(position < len(s)):
    position += 1
    if(s[position] in http_whitespace):
        continue
    parameterName = ''
    while(position<len(s) and s[position]!=';' and s[position]!='='):
        parameterName += s[position]
        position += 1
    parameterName = parameterName.lower()
    if(position<len(s)):
        if(s[position]==';'):
            continue
        position += 1
    if(position >= len(s)):
        break
    parameterValue = None
    if(s[position]=='"'):
        parameterValue = ''
        position += 1
        while(True):
            while(position<len(s) and s[position]!='"' and s[position]!='\u005C'):
                parameterValue += s[position]
                position += 1
            if(position >= len(s)):
                break
            quoteOrBackslash = s[position]
            position += 1
            if(quoteOrBackslash=='\u005C'):
                if(position >= len(s)):
                    parameterValue += '\u005C'
                    break
                parameterValue += s[position]
                position += 1
            else:
                assert quoteOrBackslash=='"'
                break
        while(position<len(s) and s[position]!=';'):
            position += 1
    else:
        parameterValue = ''
        while(position<len(s) and s[position]!=';'):
            parameterValue += s[position]
            position += 1
        for i in range(len(parameterValue)-1, -1, -1):
            if(i in http_whitespace):
                parameterValue = parameterValue[:-1]
        if(parameterValue==''):
            continue

    flag1 = True
    for i in parameterName:
        if(i not in http_code_points and not i.isalnum()):
            flag1 = False
    flag2 = True
    for i in parameterValue:
        if(i not in http_quoted_points):
            flag2 = False
    if(parameterName!='' and parameterName not in mimeType['parameters'] and flag1 and flag2):
        mimeType['parameters'][parameterName] = parameterValue

print(mimeType)

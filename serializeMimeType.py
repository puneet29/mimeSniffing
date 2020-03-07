http_code_points = set(['!', '#', '$', '%', '&', '\'', '*', '+', '-', '.', '^', '_', '`', '|', '~'])

mimeType = {'type': 'text', 'subtype': 'html', 'parameters': {'charset': 'shift_jis'}}

serialization = mimeType['type'] + '/' + mimeType['subtype']
for name, value in mimeType['parameters'].items():
    serialization += ';' + name + '='
    flag = False
    for i in value:
        if(i not in http_code_points and not i.isalnum()):
            flag = True
            break
    if(value=='' or flag):
        temp = ''
        for i in value:
            if(i=='\u0022' or i=='\u005C'):
                temp += '\u005C'
            temp += i
        value = '"' + temp + '"'
    print(flag)
    serialization += value
print(serialization)

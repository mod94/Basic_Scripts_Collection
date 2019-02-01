#print int("64",16)
#100
hstr = "86B4647350B0A7C50C68079A065A8929Cf703582EEf91BA6BF11092B6B032BD4"
count = 2
asciiNums = []

tmparr = [hstr[i:i+count] for i in range(0, len(hstr), count)]

outstr = ""


for pair in tmparr:
    nchar = int(pair,16)
    if nchar > 0:
        print ''.join("pair = " + pair + " ascii = " + str(nchar) + " char = " + chr(nchar))
        c = chr(nchar)
        outstr += c
        


print outstr

'''
Produces

pair = 86 ascii = 134 char = ?
pair = B4 ascii = 180 char = ?
pair = 64 ascii = 100 char = d
pair = 73 ascii = 115 char = s
pair = 50 ascii = 80 char = P
pair = B0 ascii = 176 char = ?
pair = A7 ascii = 167 char = ?
pair = C5 ascii = 197 char = ?
pair = 0C ascii = 12 char = 

pair = 68 ascii = 104 char = h
pair = 07 ascii = 7 char = 
pair = 9A ascii = 154 char = ?
pair = 06 ascii = 6 char = 
pair = 5A ascii = 90 char = Z
pair = 89 ascii = 137 char = ?
pair = 29 ascii = 41 char = )
pair = Cf ascii = 207 char = ?
pair = 70 ascii = 112 char = p
pair = 35 ascii = 53 char = 5
pair = 82 ascii = 130 char = ?
pair = EE ascii = 238 char = ?
pair = f9 ascii = 249 char = ?
pair = 1B ascii = 27 char = 
pair = A6 ascii = 166 char = ?
pair = BF ascii = 191 char = ?
pair = 11 ascii = 17 char = 
pair = 09 ascii = 9 char = 	
pair = 2B ascii = 43 char = +
pair = 6B ascii = 107 char = k
pair = 03 ascii = 3 char = 
pair = 2B ascii = 43 char = +
pair = D4 ascii = 212 char = ?

'''

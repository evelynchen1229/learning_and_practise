s = "abcbcd"
substr=""
newstr=""
tempstr=""
longeststr=''
#longeststr=[]
for n in range(len(s)-1):
    while s[n]<=s[n+1]:
        if n < len(s)-2:#prevent n+1 exceed the range
           # print(s[n])
            substr += s[n]
            n += 1

     #   elif s[-2]<=s[-1]:
      #      substr = s[-2:]

        else:
            break
    if n<len(s)-2:
        substr +=s[n]
    elif n == len(s)-2 and s[n] <=s[n+1]:# for getting the last two letters if they are in alphabet order
        substr = substr + s[n]+s[n+1]

    else:
        pass

    if len(substr)>len(longeststr):# only assign the longest substr
        longeststr=substr
    else:
        longeststr
    substr="" #reset substr for every for loop
print(longeststr)






































#def multiply ():
 #   user = input()
  #  cal = []
   # user = user.split()
    #for i in user:
     #   cal.append(i)


    #index = user.index("*")
    #a = int(cal[index-1])
   # b = int(cal[index+1])


#    c=0
#
#   for n in range (0,b):
 #       c += a
  #  return c


#result = multiply()
#print(result)

#a = multiply (4,19)
#print (a)

#from collections import defaultdict
#
#e = defaultdict(list)
#a = ['Stephensons','Peters & Peters']
#b = [['1234','2345'],['3456','3455']]
#
#for i in a:
#    e[i].extend(b[a.index(i)])
#
#print (e.items())




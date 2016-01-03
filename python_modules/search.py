def levenshtein(s, len_s, t, len_t):
    cost = 0
    
    # base case: empty strings
    if len_s == 0:
        return len_t
    if len_t == 0:
        return len_s
    
    #test if last characters of the strings match
    if s[len_s-1] == t[len_t-1]:
        cost = 0
    else:
        cost = 1
        
    #return minimum of delete char from s, delete char from t, and delete char from both
    return min(levenshtein(s, len_s - 1, t, len_t) + 1,
               levenshtein(s, len_s    , t, len_t - 1) + 1,
               levenshtein(s, len_s - 1, t, len_t - 1) + cost)

def searchSort(query, nameList):
    names = query.lower().split(' ')
    first, last = names[0], names[1]
    arr = []
    for e in nameList:
        n = e.lower().split(' ')
        f, l = n[0], n[1]
        arr.append(levenshtein(first,len(first),f,len(f)) + levenshtein(last,len(last),l,len(l)))
    arr = [list(a) for a in zip(nameList,arr)]
    arr.sort(key=lambda x: x[1])   
    return arr

print searchSort('Sarth Frey',['SaRTH FReY','Eddy Luuuuu','Michael Jackson','Sarthy freyyy','nat Woody'])

#print levenshtein("kitten",6,"mitten",6)
#print levenshtein("kitten",6,"guy",3)
#print levenshtein("kitten",6,"goooooooooogle",14)

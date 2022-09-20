def test(str_data):
    z={}
    for u,i in enumerate(str_data):
        if i not in z:
           z[i]=[1,u]
        else:
            z[i][0]+=1
    for u, i in z.items():
           if i[0]==1:
               return i[1]
    return -1
if __name__ == '__main__':
    ["Aibee Apple",'','aabb','a','aA','abcde',' aa','1a3','%#aa%']
    # s1 = "Aibee Apple"
    # print (test(s1))
    # s2 = "Aibee Apple"
    print (test('aa'))





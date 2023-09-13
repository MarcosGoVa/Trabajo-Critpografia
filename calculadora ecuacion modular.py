def congru(a,b,c):
    "Funcion que calcula la congruencia ax = b mod c"
    for i in range(0,c):
       if ((a*i - b)%c)== 0 :
          print(i)


congru(19,4,49)
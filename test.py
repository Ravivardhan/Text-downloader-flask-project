no_of=input('enter number of elements')
weights=[]
weights=input("enter size of element").split()


new=[]
colors=0
sol=True
while sol==True:
    high=weights[-1]
    low=weights[0]

    if low<=2*high:
        ele=low+high
        weights.remove(weights[-1])
        weights.remove(weights[0])
        new.append(ele)

        weights.append(ele)
        weights = sorted(weights)
        colors+=1

    if len(weights)==1:
        sol=False
print(colors)
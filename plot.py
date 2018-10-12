import matplotlib.pyplot as plt
import random
def textogram(points_label,values,labels):
    if(len(values)!=len(labels)):
        print("Error:Length of labels is not the same as values")
        return
    elif(len(points_label) != len(labels)):
        print("Error:Length of labels is not the same as points")
        return
    plt.axis([0,len(labels) + 1,0, max(values)+1])
    points=list(range(1, len(points_label) + 1))
    plt.xticks(points,points_label)
    plt.rcParams["figure.figsize"] =[6.4,4.8]
    yscale=89/(2*(max(values)+1)) #factor by which pixel related to font_size
    for index,text in zip(points,labels):
        plt.text(index,0,text,rotation=90,va = "bottom",ha = "center",fontsize = 10*values[index-1]*(yscale/len(text)),family='monospace',color=(random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)))
    plt.show()

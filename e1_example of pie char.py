import matplotlib.pyplot as plt


sizes = [34, 42, 56, 13]


labels = ['A', 'B', 'C', 'D']


colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

explode = (0, 0.1, 0, 0)

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=90)



plt.show()

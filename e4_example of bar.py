import matplotlib.pyplot as plt

num_list = [1.5, 0.6, 7.8, 6]


color = (0.8, 0.6, 0.8, 1.0)

plt.barh(range(len(num_list)), num_list, color=color)
plt.show()

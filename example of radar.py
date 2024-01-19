import numpy as np
import matplotlib.pyplot as plt


results = [{"var1": 87, "var2": 79, "var3": 95, "var4": 92, "var5": 85},
           {"var1": 80, "var2": 90, "var3": 91, "var4": 85, "var5": 88}]
data_length = len(results[0])

angles = np.linspace(0, 2*np.pi, data_length, endpoint=False)
labels = [key for key in results[0].keys()]
score = [[v for v in result.values()] for result in results]

score_a = np.concatenate((score[0], [score[0][0]]))
score_b = np.concatenate((score[1], [score[1][0]]))
angles = np.concatenate((angles, [angles[0]]))
labels = np.concatenate((labels, [labels[0]]))

fig = plt.figure(figsize=(8, 6), dpi=100)

ax = plt.subplot(111, polar=True)

ax.plot(angles, score_a, color='g')
ax.plot(angles, score_b, color='b')

ax.set_thetagrids(angles*180/np.pi, labels)

ax.set_theta_zero_location('N')

ax.set_rlim(0, 100)

ax.set_rlabel_position(270)

plt.show()
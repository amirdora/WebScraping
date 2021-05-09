import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
import mplcursors

with open('data.json', encoding="utf8") as f:
    data = json.load(f, encoding="utf8")

topic = []
category = []
pro_arg_count = []
con_arg_count = []

# pro vs con for top 5 popular debates

for i in range(0, 5):
    topic.append(data[i]["topic"])
    category.append(data[i]["category"])
    pro_arg_count.append(len(data[i]['pro_arguments']))
    con_arg_count.append(len(data[i]['con_arguments']))

# pro vs con for categories
tot_pro_arg_count = []
tot_con_arg_count = []
tot_category = []
for i in range(0, 5):
    if not tot_category:
        tot_category.append(category[i])
        tot_pro_arg_count.append(pro_arg_count[i])
        tot_con_arg_count.append(con_arg_count[i])

    elif category[i] in tot_category:
        index = tot_category.index(category[i])
        tot_pro_arg_count[index] = tot_pro_arg_count[index] + pro_arg_count[i]
        tot_con_arg_count[index] = tot_con_arg_count[index] + con_arg_count[i]

    else:
        tot_category.append(category[i])
        tot_pro_arg_count.append(pro_arg_count[i])
        tot_con_arg_count.append(con_arg_count[i])

# Bar chart for total pro and con arguments for each category

width = 0.35
fig, ax = plt.subplots()
tot_category_pro = []
tot_category_con = []
tot_category_label = []
for i in range(0, len(tot_category)):
    tot_category_pro.append(str(tot_category[i]) + " Pro")
    tot_category_label.append(str(tot_category[i]) + " Pro")
    tot_category_con.append(str(tot_category[i]) + " Con")
    tot_category_label.append(str(tot_category[i]) + " Con")

k1 = np.arange(len(tot_category_label))
for i in range(0, len(tot_category)):
    pro1 = ax.bar(tot_category_pro[i], tot_pro_arg_count[i], label=tot_category_pro[i], alpha=0.5)
    con1 = ax.bar(tot_category_con[i], tot_con_arg_count[i], label=tot_category_con[i], alpha=0.5)
    ax.bar_label(pro1, padding=3)
    ax.bar_label(con1, padding=3)

ax.set_ylabel('Count')
ax.set_title('Bar Chart: Total Category vs Argument Count (Pro & Con)')
ax.set_xticks(k1)
ax.set_xticklabels(tot_category_label)
ax.legend(loc=1, fontsize='x-small')
fig.tight_layout()
mplcursors.cursor(hover=True)
plt.show()

# Bar chart for total pro and con arguments for each topic

width = 0.35
fig, ax = plt.subplots()
tot_topic_pro = []
tot_topic_con = []
tot_topic_label = []
for i in range(0, len(topic)):
    tot_topic_pro.append(str(topic[i]) + " Pro")
    tot_topic_label.append(str(topic[i]) + " Pro")
    tot_topic_con.append(str(topic[i]) + " Con")
    tot_topic_label.append(str(topic[i]) + " Con")

k1 = np.arange(len(tot_topic_label))
for i in range(0, len(topic)):
    pro1 = ax.bar(tot_topic_pro[i], pro_arg_count[i], label=tot_topic_pro[i], alpha=0.5)
    con1 = ax.bar(tot_topic_con[i], con_arg_count[i], label=tot_topic_con[i], alpha=0.5)
    ax.bar_label(pro1, padding=3)
    ax.bar_label(con1, padding=3)

ax.set_ylabel('Count')
ax.set_title('Bar Chart: Total Category vs Argument Count (Pro & Con)')
ax.set_xticks(k1)
ax.set_xticklabels(tot_topic_label)
ax.legend(loc=1, fontsize='xx-small')
ax.bar_label(pro1, padding=3)
ax.bar_label(con1, padding=3)
fig.tight_layout()
plt.xticks(rotation=90)
mplcursors.cursor(hover=True)
plt.show()
exit()
# Histogram: Topics vs Total pro and con-arguments for each topic

tot_pro_log = []
tot_pro_log = np.log(tot_pro_arg_count)

for i in range(0, len(tot_category)):
    l1 = str(tot_category[i]) + " - " + str(tot_pro_arg_count[i])
    pyplot.hist(tot_pro_log[i], label=l1)

pyplot.xlabel("Total Pro-arguments (in log scale)")
pyplot.ylabel("Density")
pyplot.xticks(rotation=90)
pyplot.legend()
pyplot.title("Histogram for Pro-arguments (actual value specified inside the legend)")
pyplot.show()

tot_con_log = []
tot_con_log = np.log(tot_con_arg_count)

for i in range(0, len(tot_category)):
    l2 = str(tot_category[i]) + " - " + str(tot_con_arg_count[i])
    pyplot.hist(tot_con_log[i], label=l2)

pyplot.xlabel("Total Con-arguments (in log scale)")
pyplot.ylabel("Density")
pyplot.xticks(rotation=90)
pyplot.legend()
pyplot.title("Histogram for Con-arguments (actual value specified inside the legend)")
pyplot.show()

# Histogram: printing the pro vs con for each category

tot_pro_log = np.log(pro_arg_count)
tot_con_log = np.log(con_arg_count)

for i in range(0, len(topic)):
    l1 = str(topic[i]) + " - " + str(pro_arg_count[i])
    pyplot.hist(tot_pro_log[i], label=l1, bins=10)

pyplot.xlabel("Pro-arguments for each category (in log scale)")
pyplot.ylabel("Density")
pyplot.xticks(rotation=90)
pyplot.legend()
pyplot.title("Histogram for Pro-arguments (actual value specified inside the legend)")
pyplot.show()

for i in range(0, len(topic)):
    l2 = str(topic[i]) + " - " + str(con_arg_count[i])
    pyplot.hist(tot_con_log[i], label=l2)

pyplot.xlabel("Con-arguments for each category (in log scale)")
pyplot.ylabel("Density")
pyplot.xticks(rotation=90)
pyplot.legend()
pyplot.title("Histogram for Con-arguments (actual value specified inside the legend)")
pyplot.show()

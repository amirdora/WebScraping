import json
from matplotlib import pyplot

with open('data.json') as f:
    data = json.load(f)

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
# Topics vs Total pro and con-arguments for each topic

for i in range(0, len(tot_category)):
    l1 = tot_category[i]
    pyplot.hist(tot_pro_arg_count[i], label=l1)

pyplot.xlabel("total Pro-arguments")
pyplot.ylabel("Counts")
pyplot.xticks(rotation=90)
pyplot.legend()
pyplot.title("Histogram Pro-arguments")
pyplot.show()

for i in range(0, len(tot_category)):
    l2 = tot_category[i]
    pyplot.hist(tot_con_arg_count[i], label=l2)

pyplot.xlabel("total Con-arguments")
pyplot.ylabel("Counts")
pyplot.xticks(rotation=90)
pyplot.legend()
pyplot.title("Histogram Con-arguments")
pyplot.show()

# printing the pro vs con for each category
print("pros", pro_arg_count)
print("cons", con_arg_count)

for i in range(0, len(topic)):
    l1 = topic[i]
    pyplot.hist(pro_arg_count[i], label=l1)

pyplot.xlabel("Pro-arguments")
pyplot.ylabel("Counts")
pyplot.xticks(rotation=90)
pyplot.legend()
pyplot.title("Histogram Pro-arguments")
pyplot.show()

for i in range(0, len(topic)):
    l2 = topic[i]
    pyplot.hist(con_arg_count[i], label=l2)

pyplot.xlabel("Con-arguments")
pyplot.ylabel("Counts")
pyplot.xticks(rotation=90)
pyplot.legend()
pyplot.title("Histogram Con-arguments")
pyplot.show()

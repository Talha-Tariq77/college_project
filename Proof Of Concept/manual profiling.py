import matplotlib.pyplot as plt


results = open('results.txt', 'r')
sorted_results = {'select': [], '1sim': [], 'expand': [], '2sim': []}
for line in results.readlines():
    if 'select' in line:
        sorted_results['select'].append(line[7:-1])
    elif '1sim' in line:



print(sorted_results['select'])

# plt.plot(sorted_results['select'])
# plt.ylabel('Time taken for selection function per call')
# plt.show()
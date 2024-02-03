data_structure = [[1,2,3,45,67], [1,2,3,45,67], [1,2,3,45,67]]

def test_func(a):
    b = [[d for d in c] for c in a]
    b[1][0] = 55


test_func(data_structure)

print(data_structure)


test = []

print(test == True)
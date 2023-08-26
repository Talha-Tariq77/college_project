depth = [0]
def recursive(x):
    depth[0] += 1
    print(depth[0])
    if depth[0] <= 994:
        recursive(x)
    else:
        return x, depth

print(recursive(1))


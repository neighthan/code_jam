{{funcs}}

n_cases = int(input())
for case in range(1, n_cases + 1):
    inputs = input().split(' ')
    # GCJ doesn't use Py3.6 yet, so no fstrings
    print("Case #{}: {}".format(case, {{solve_func}}(*inputs)))

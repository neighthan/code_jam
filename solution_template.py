{{funcs}}

n_lines_per_case = {{n_lines_per_case}}

n_cases = int(input())
for case in range(1, n_cases + 1):
    lines = []
    for _ in range(n_lines_per_case):
        lines.append(input().split(' '))

    if len(lines) == 1:
        lines = lines[0]

    # GCJ doesn't use Py3.6 yet, so no fstrings
    print("Case #{}: {}".format(case, {{solve_func}}(*lines)))

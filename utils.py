import os
import pandas as pd
from typing import Optional, List, Tuple, Union, Callable


def write_example_file(year: str, problem_name: str, example_text: str) -> None:
    """
    Writes an example input file.
    :param problem_name: name of the problem (name of the example file will be data/{year}/{problem_name}_ex.in)
    :param example_text: text to write to the example file
    """

    # ensure necessary data directories are present
    try:
        os.mkdir('data')
    except FileExistsError:
        pass
    
    try:
        os.mkdir(f'data/{year}')
    except FileExistsError:
        pass    

    outfile_name = f'data/{year}/{problem_name}_ex.in'
    with open(outfile_name, 'w') as out_file:
        out_file.write(example_text)


def read_input(year: str, problem_name: str, size: str, raw: bool=False, col_names: Optional[List[str]]=None, verbose: bool=True)\
        -> Tuple[int, Union[List[str], pd.DataFrame]]:
    """
    Reads in input from the file data/{year}/{problem_name}_{size}.in
    It is assumed that the input file contains the number of cases on the first line and that all other lines 
    contain the same number of input data points with spaces delimiting columns.
    :param problem_name: name of the problem
    :param size: which file size to load (generally: ex, small, large)
    :param raw: if True, just return the list of strings from the input file: one per row (except n_cases ommitted)
    :param col_names: names to give to the columns of the inputs dataframe; should match in number the 
                      columns in the input data file (except the file's first line). if None, default names will be used.
    :param verbose: whether to print information such as the number of cases and the first few lines of the input
    :returns: (n_cases, inputs)
              - n_cases: number of cases for the problem
              - inputs: a list containing each row as a string if raw=True, otherwise a pd.DataFrame
    """

    input_file_name = f"data/{year}/{problem_name}_{size}.in"
    with open(input_file_name) as in_file:
        n_cases = int(in_file.readline())
        if raw:
            return n_cases, list(map(lambda x: x.strip(), in_file.readlines()))
    
    inputs = pd.read_csv(input_file_name, sep=" ", skiprows=1, header=None, names=col_names)
    
    if verbose:
        print("# cases: {}".format(n_cases))
        print(inputs.head())
    
    return n_cases, inputs

def write_raw_output(output: List[str], year: str, problem_name: str, size: str) -> None:
    write_output(pd.DataFrame(output), lambda x: x, year, problem_name, size)


def write_output(inputs: pd.DataFrame, solver: Callable, year: str, problem_name: str, size: str, expand_inputs: bool=False, verbose: bool=True) -> None:
    """
    Applies solver row-wise to inputs and writes to disk a file with the returned solution for each case.
    The format of the solutions file is, for each row: Case #x: y, where x is the row number (1-indexed)
    and y is the value returned by solver for that row. The name of the output file is 
    problem_name + '.output.' + extension.
    :param inputs: each row should contain all of the necessary inputs (properly named) for the solver function for that case.
                   Generally, inputs is the dataframe returned by read_input
    :param solver: a function that can be applied row-wise to inputs to produce the output Series
    :param problem_name: name of the problem
    :param size: which file size to load (generally: ex, small, large)
    :param expand_inputs: if True, instead of passing each row of inputs as a pd.Series to solver, pass them as individual elements (*Series)
    :param verbose: (bool) whether to print information such as the head of the outputs dataframe
    """

    if expand_inputs:
        output = pd.DataFrame(inputs.apply(lambda x: solver(*x), axis=1))
    else:
        output = pd.DataFrame(inputs.apply(solver, axis=1))

    output.insert(0, 'case', "Case")
    output.insert(1, 'number', output.index + 1)
    output.number = output.number.apply(lambda case_num: f"#{case_num}:")
    
    with open(f'data/{year}/{problem_name}_{size}.out', 'w') as f:
        out_string = '\n'.join(map(lambda row: ' '.join(str(e) for e in row), output.values))
        if verbose:
            print(out_string[:300)
        f.write(out_string)
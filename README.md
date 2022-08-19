# Controlling randomness
```
@pseudo_random(*, seed=0, evolutive=True, input_dependent=False, loop=0, make_key=repr)
```
Decorator Factory to control randomness of decorated function.
The random seed of `random` and `np.random` are set depending on the function name, it's input arguments, and the number of time it has been called.
Equality of calls is computed using `repr`. Inputs with different representations will be considered different.
When called on a class method, it must be decorated with `@method` decorator included in the package.
The parameters to `pseudo_random()` are:
  - `evolutive` (`bool`): random seed is incremented each time the function is called. The counter is different for each set of arguments.
  - `input_dependent` (`bool`): initial random seed depends on function's input.
  - `loop` (`int`): get repeating input every `loop` iteration when `evolutive` is `True`. Else, `loop` argument is ignored.
  - `make_key`: a function to compute the key based on the function name and it's arguments: `(f.__name__, args, kwargs)`. Default is the builtin `repr`.
            
### Example
Basic usage:
```
@pseudo_random(input_dependent=input_dependent, evolutive=evolutive)
def get_random_number(*args):
    return random.randint(0,9)
argument = '0'
print(" ".join([str(get_random_number(argument)) for _ in range(5)]))
```

Called 5 times with 5 different inputs will yield:
```
evolutive: True      input_dependent: True      (5 iterations)
-----------------------------------------------------------------
with argument='0':	3 0 4 2 5
with argument='1':	0 7 3 3 4
with argument='2':	8 3 3 4 9
with argument='3':	1 6 8 0 2
with argument='4':	4 0 2 9 1

evolutive: False     input_dependent: True      (5 iterations)
-----------------------------------------------------------------
with argument='0':	3 3 3 3 3
with argument='1':	0 0 0 0 0
with argument='2':	8 8 8 8 8
with argument='3':	1 1 1 1 1
with argument='4':	4 4 4 4 4

evolutive: True      input_dependent: False     (5 iterations)
-----------------------------------------------------------------
with argument='0':	6 2 0 3 3
with argument='1':	6 2 0 3 3
with argument='2':	6 2 0 3 3
with argument='3':	6 2 0 3 3
with argument='4':	6 2 0 3 3

evolutive: False     input_dependent: False     (5 iterations)
-----------------------------------------------------------------
with argument='0':	6 6 6 6 6
with argument='1':	6 6 6 6 6
with argument='2':	6 6 6 6 6
with argument='3':	6 6 6 6 6
with argument='4':	6 6 6 6 6
```

## Citation
If you use this repository, please consider citing my work.

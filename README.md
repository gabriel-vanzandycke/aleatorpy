# Controlling randomness of functions
Decorator Factory to control randomness of decorated function.
Randomness is controlled by the function name and input arguments. 
Equality is computed using builtin `hash()`. Two objets with two
different hash will be considered different.
When called on a class method, it must be decorated with `@method`.

### Arguments:
  - `evolutive` (`bool`): random seed is incremented each time the function is called. The counter is different for each set of arguments.
  - `input_dependent` (`bool`): initial random seed depends on function's input.
  - `loop` (`int`): get repeating input every `loop` iteration when `evolutive` is `True`. Else, `loop` argument is ignored.
            
### Example
Basic usage:
```
@pseudo_random(input_dependent=input_dependent, evolutive=evolutive)
def get_random_number(*args):
    return random.randint(0,9)
```

Called 5 times with 5 different inputs will yield:
```
evolutive: True	input_dependent: True	(5 iterations)
---------------------------------------------------------------
arguments='0':  0 3 2 2 4 
arguments='1':  5 8 6 8 6 
arguments='2':  3 7 7 9 8 
arguments='3':  5 3 8 3 8 
arguments='4':  0 1 4 0 6 

evolutive: False	input_dependent: True	(5 iterations)
---------------------------------------------------------------
arguments='0':  9 9 9 9 9 
arguments='1':  2 2 2 2 2 
arguments='2':  6 6 6 6 6 
arguments='3':  0 0 0 0 0 
arguments='4':  9 9 9 9 9 

evolutive: True	input_dependent: False	(5 iterations)
---------------------------------------------------------------
arguments='0':  6 2 0 3 3 
arguments='1':  6 2 0 3 3 
arguments='2':  6 2 0 3 3 
arguments='3':  6 2 0 3 3 
arguments='4':  6 2 0 3 3 

evolutive: False	input_dependent: False	(5 iterations)
---------------------------------------------------------------
arguments='0':  6 6 6 6 6 
arguments='1':  6 6 6 6 6 
arguments='2':  6 6 6 6 6 
arguments='3':  6 6 6 6 6 
arguments='4':  6 6 6 6 6 
```

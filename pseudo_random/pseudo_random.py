import random
import functools
import numpy as np


# Define a simple decorator, do nothing, just wrap the callable object into a function
def method(call):
    def wrapper(*args, **kwargs):
        return call(*args, **kwargs)
    return wrapper

def pseudo_random(seed=0, evolutive=True, input_dependent=False, loop=0):
    """ Decorator Factory to control randomness of decorated function.
        Randomness is controlled by the function name and input arguments.
        Equality is computed using builtin `hash()`. Two objets with two
        different hash will be considered different.
        When called on a class method, it must be decorated with `@method`.

        Arguments:
            evolutive (bool) - random seed is incremented each time the function
            is called. The counter is different for each set of arguments.
            input_dependent (bool) - initial random seed depends on function's
            input.
    """
    def decorator(f):
        class DecoratorFactory:
            def __init__(self, f, *, seed=0, evolutive=True, input_dependent=False, loop=0, make_key=repr):
                self.f = f
                self.seed = seed
                self.__history = {}
                self.__evolutive = evolutive
                self.__input_dependent = input_dependent
                self.__loop = loop
                self.make_key = make_key

            def reset_seed(self):
                self.__history = {}

            @functools.wraps(f)
            def __call__(self, *args, **kwargs):
                key = self.make_key((self.f, args, kwargs))
                history_seed = self.__history.setdefault(key, 0)

                # backup random state
                random_state = random.getstate()
                np_random_state = np.random.get_state()

                call_seed = history_seed + (0 if not self.__input_dependent else hash(key))

                # set random state
                random.seed(self.seed + call_seed)
                np.random.seed((self.seed + call_seed) & 0xFFFFFFFF)

                result = self.f(*args, **kwargs)

                # restore random state
                random.setstate(random_state)
                np.random.set_state(np_random_state)

                if self.__evolutive:
                    self.__history[key] += 1
                    if self.__loop:
                        self.__history[key] %= self.__loop

                return result
        return DecoratorFactory(f, seed=seed, evolutive=evolutive, input_dependent=input_dependent, loop=loop)
    return decorator
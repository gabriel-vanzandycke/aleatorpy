import functools
import hashlib
import random
import numpy as np


# Define a simple decorator, do nothing, just wrap the callable object into a function
def method(call):
    def wrapper(*args, **kwargs):
        return call(*args, **kwargs)
    return wrapper

def pseudo_random(seed=0, evolutive=True, input_dependent=False, loop=0, repeat=1, make_key=repr):
    """ Decorator Factory to control randomness of decorated function.
        Randomness is controlled by the function name and input arguments.
        Equality is computed using builtin `hash()`. Two objets with two
        different hash will be considered different.
        When called on a class method, it must be decorated with `@method`.

        Arguments:
            evolutive (bool) - random seed is incremented each time the function
                is called. The counter is different for each set of arguments.
            input_dependent (bool) - initial random seed depends on function's
                input arguments.
            seed (int) - base seed (should be kept constant for reproducible
                results)
            loop (int) - random seed counter is reset after `loop` iterations.
                `loop=0` means never. Only makes sense when `evolutive=True`.
                `loop=1` is equivalent of having `evolutive=False`.
            repeat (int) - random seed is incremented every `repeat` iterations.

        Note:
            It's necessary to have DecoratorFactory defined within
            `pseudo_random`'s `decorator` for `functools.wraps(f)` to work.
    """
    def decorator(f):
        class DecoratorFactory:
            def __init__(self, f, *, seed=0, evolutive=True, input_dependent=False, loop=0, repeat=1, make_key=repr):
                self.f = f
                self.seed = seed
                self.loop = loop
                self.__history = {}
                self.__evolutive = evolutive
                self.__input_dependent = input_dependent
                self.__repeat = repeat
                self.make_key = make_key

            def reset_seed(self):
                self.__history = {}

            @staticmethod
            def hash_func(string):
                return int(hashlib.md5(string.encode('utf-8')).hexdigest()[0:8], 16)

            @functools.wraps(f)
            def __call__(self, *args, **kwargs):
                key = self.make_key((args, kwargs))# self.f, args, kwargs))   <--- why is 'self.f' necessary ??!?
                history_seed = self.__history.setdefault(key, 0)//self.__repeat

                # backup random state
                random_state = random.getstate()
                np_random_state = np.random.get_state()

                call_seed = history_seed + (0 if not self.__input_dependent else self.hash_func(key))

                # set random state
                random.seed(self.seed + call_seed)
                np.random.seed((self.seed + call_seed) & 0xFFFFFFFF)

                result = self.f(*args, **kwargs)

                # restore random state
                random.setstate(random_state)
                np.random.set_state(np_random_state)

                if self.__evolutive:
                    self.__history[key] += 1
                    if self.loop:
                        self.__history[key] %= self.loop

                return result
        return DecoratorFactory(f, seed=seed, evolutive=evolutive, input_dependent=input_dependent, repeat=repeat, loop=loop, make_key=make_key)
    return decorator

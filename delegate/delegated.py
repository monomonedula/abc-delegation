from abc import ABCMeta


class DelegatingMeta(ABCMeta):
    def __new__(mcs, name, bases, dct):
        abstract_method_names = frozenset.union(*(base.__abstractmethods__
                                                  for base in bases))
        for name in abstract_method_names:
            if name not in dct:
                def delegator(self, *args, **kwargs):
                    return getattr(self._delegate, name)(*args, **kwargs)
                dct[name] = delegator

        return super(DelegatingMeta, mcs).__new__(mcs, name, bases, dct)


def delegate_metaclass(*delegates):
    class _DelegatingMeta(ABCMeta):
        def __new__(mcs, name, bases, dct):
            abstract_method_names = frozenset.union(*(base.__abstractmethods__
                                                      for base in bases))
            for amethod in abstract_method_names:
                if amethod not in dct:
                    dct[amethod] = make_delegated_method(delegates, amethod)
            return super(_DelegatingMeta, mcs).__new__(mcs, name, bases, dct)
    return _DelegatingMeta


def make_delegated_method(delegate_names, attr):
    def delegated_method(self, *args, **kwargs):
        for d in delegate_names:
            delegate_ = getattr(self, d)
            if hasattr(delegate_, attr):
                return getattr(delegate_, attr)(*args, **kwargs)
        AttributeError(f"None of delegates has method '{attr}'")
    return delegated_method

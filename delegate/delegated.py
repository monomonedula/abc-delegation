from abc import ABCMeta


def delegation_metaclass(delegate_attr="_delegate"):
    class _DelegatingMeta(ABCMeta):
        def __new__(mcs, name, bases, dct):
            abstract_method_names = frozenset.union(
                *(base.__abstractmethods__ for base in bases)
            )
            for name in abstract_method_names:
                if name not in dct:
                    dct[name] = _delegate_method(delegate_attr, name)

            return super(_DelegatingMeta, mcs).__new__(mcs, name, bases, dct)

    return _DelegatingMeta


DelegatingMeta = delegation_metaclass("_delegate")


def _delegate_method(delegate_name, method_name):
    def delegated_method(self, *args, **kwargs):
        return getattr(getattr(self, delegate_name), method_name)(*args, **kwargs)

    return delegated_method


def multi_delegation_metaclass(*delegates):
    class _DelegatingMeta(ABCMeta):
        def __new__(mcs, name, bases, dct):
            abstract_method_names = frozenset.union(
                *(base.__abstractmethods__ for base in bases)
            )
            for amethod in abstract_method_names:
                if amethod not in dct:
                    dct[amethod] = _make_delegated_method_multi(delegates, amethod)
            return super(_DelegatingMeta, mcs).__new__(mcs, name, bases, dct)

    return _DelegatingMeta


def _make_delegated_method_multi(delegate_names, attr):
    def delegated_method(self, *args, **kwargs):
        for d in delegate_names:
            delegate_ = getattr(self, d)
            if hasattr(delegate_, attr):
                return getattr(delegate_, attr)(*args, **kwargs)
        AttributeError(f"None of delegates has method '{attr}'")

    return delegated_method

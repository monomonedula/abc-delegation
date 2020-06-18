from abc import ABCMeta


def multi_delegation_metaclass(*delegates, validate=True):
    """
    A factory function for delegation metaclasses.
    :param delegate_attr: The name of the attribute to be used as the delegate object.
    :param validate: Whether to check if delegates have required attributes on the object creation. Default True.
    :return: metaclass
    """
    class _DelegatingMeta(ABCMeta):
        def __new__(mcs, name, bases, dct):
            abstract_method_names = frozenset.union(
                *(base.__abstractmethods__ for base in bases)
            ).difference(dct.keys())
            for amethod in abstract_method_names:
                if amethod not in dct:
                    dct[amethod] = _make_delegated_method_multi(delegates, amethod)
            if validate:
                dct["__init__"] = _wrap_init_multi(
                    dct["__init__"], delegates, abstract_method_names
                )

            return super(_DelegatingMeta, mcs).__new__(mcs, name, bases, dct)

    return _DelegatingMeta


def _make_delegated_method_multi(delegate_names, attr):
    def delegated_method(self, *args, **kwargs):
        for d in delegate_names:
            delegate_ = getattr(self, d)
            if hasattr(delegate_, attr):
                return getattr(delegate_, attr)(*args, **kwargs)
        AttributeError("None of delegates has method %r" % attr)

    return delegated_method


def _wrap_init_multi(init, delegate_attributes, abstract_method_names):
    def wrapped_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        delegates = [
            getattr(self, delegate_attr) for delegate_attr in delegate_attributes
        ]
        for name in abstract_method_names:
            for i, delegate in enumerate(delegates, 1):
                try:
                    getattr(delegate, name)
                except AttributeError:
                    if i == len(delegates):
                        raise TypeError(
                            "Can't instantiate %s: missing attribute %s in the delegate attributes %s"
                            % (type(self).__name__, name, delegate_attributes)
                        )
                else:
                    break

    return wrapped_init

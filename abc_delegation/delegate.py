from abc import ABCMeta


def delegation_metaclass(delegate_attr="_delegate", validate=True):
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
            for method_name in abstract_method_names:
                if method_name not in dct:
                    dct[method_name] = _delegate_method(delegate_attr, method_name)
            if validate:
                dct["__init__"] = _wrap_init(
                    dct["__init__"], delegate_attr, abstract_method_names
                )

            return super(_DelegatingMeta, mcs).__new__(mcs, name, bases, dct)

    return _DelegatingMeta


DelegatingMeta = delegation_metaclass("_delegate")
UnsafeDelegatingMeta = delegation_metaclass("_delegate", validate=False)


def _wrap_init(init, delegate_attr, abstract_method_names):
    def wrapped_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        delegate = getattr(self, delegate_attr)
        for name in abstract_method_names:
            try:
                getattr(delegate, name)
            except AttributeError:
                raise TypeError(
                    "Can't instantiate %s: missing attribute %s in the delegate attribute %s"
                    % (type(self).__name__, name, delegate_attr)
                )

    return wrapped_init


def _delegate_method(delegate_name, method_name):
    def delegated_method(self, *args, **kwargs):
        return getattr(getattr(self, delegate_name), method_name)(*args, **kwargs)

    return delegated_method

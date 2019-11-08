from abc import abstractmethod, ABCMeta

from abc_delegation.delegate import (
    DelegatingMeta,
    delegation_metaclass,
    multi_delegation_metaclass,
)


def test_basic_delegation():
    class A(metaclass=ABCMeta):
        @abstractmethod
        def bar(self):
            pass

        @abstractmethod
        def foo(self):
            pass

    class B:
        def bar(self):
            return "B bar"

        def foo(self):
            return "B foo"

    class C(A, metaclass=DelegatingMeta):
        def __init__(self, b):
            self._delegate = b

        def foo(self):
            return "C foo"

    c = C(B())
    assert c.foo() == "C foo"
    assert c.bar() == "B bar"


def test_multi_delegation():
    class A(metaclass=ABCMeta):
        @abstractmethod
        def bar(self):
            pass

        @abstractmethod
        def foo(self):
            pass

        @abstractmethod
        def baz(self):
            pass

    class B:
        def bar(self):
            return "B bar"

        def foo(self):
            return "B foo"

    class X:
        def baz(self):
            return "X baz"

    class C(A, metaclass=multi_delegation_metaclass("_delegate1", "_delegate2")):
        def __init__(self, d1, d2):
            self._delegate1 = d1
            self._delegate2 = d2

        def foo(self):
            return "C foo"

    c = C(B(), X())
    assert c.bar() == "B bar"
    assert c.foo() == "C foo"
    assert c.baz() == "X baz"


def test_custom_name_delegate():
    class A(metaclass=ABCMeta):
        @abstractmethod
        def bar(self):
            pass

        @abstractmethod
        def foo(self):
            pass

    class B:
        def bar(self):
            return "B bar"

        def foo(self):
            return "B foo"

    class C(A, metaclass=delegation_metaclass("my_delegate")):
        def __init__(self, b):
            self.my_delegate = b

        def foo(self):
            return "C foo"

    c = C(B())
    assert c.foo() == "C foo"
    assert c.bar() == "B bar"

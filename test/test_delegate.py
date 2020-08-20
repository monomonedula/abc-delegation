from abc import abstractmethod, ABCMeta

import pytest

from abc_delegation.delegate import (
    DelegatingMeta,
    delegation_metaclass, UnsafeDelegatingMeta,
)
from abc_delegation import multi_delegation_metaclass


@pytest.mark.parametrize("metaclass", [DelegatingMeta, delegation_metaclass("_delegate")])
def test_basic_delegation(metaclass):
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

    class C(A, metaclass=metaclass):
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


@pytest.mark.parametrize("metaclass", [DelegatingMeta, delegation_metaclass("_delegate")])
def test_raises(metaclass):
    class A(metaclass=ABCMeta):
        @abstractmethod
        def bar(self):
            pass

        @abstractmethod
        def foo(self):
            pass

    class B:
        pass

    class C(A, metaclass=metaclass):
        def __init__(self, b):
            self._delegate = b

        def foo(self):
            return "C foo"

    with pytest.raises(TypeError):
        C(B())


def test_raises_multi():
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

    with pytest.raises(TypeError):
        C(B(), X())


@pytest.mark.parametrize("metaclass", [DelegatingMeta, delegation_metaclass("_delegate")])
def test_partial_delegation(metaclass):
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

    class C(A, metaclass=metaclass):
        def __init__(self, b):
            self._delegate = b

        def foo(self):
            return "C foo"

    c = C(B())
    assert c.foo() == "C foo"
    assert c.bar() == "B bar"


@pytest.mark.parametrize("metaclass", [UnsafeDelegatingMeta, delegation_metaclass("_delegate", validate=False)])
def test_validation_turn_off(metaclass):
    class A(metaclass=ABCMeta):
        @abstractmethod
        def bar(self):
            pass

        @abstractmethod
        def foo(self):
            pass

    class B:
        pass

    class C(A, metaclass=metaclass):
        def __init__(self, b):
            self._delegate = b

        def foo(self):
            return "C foo"

    C(B())


def test_validation_turn_off_multi():
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
        def foo(self):
            return "B foo"

    class X:
        def baz(self):
            return "X baz"

    class C(A, metaclass=multi_delegation_metaclass("_delegate1", "_delegate2", validate=False)):
        def __init__(self, d1, d2):
            self._delegate1 = d1
            self._delegate2 = d2

        def foo(self):
            return "C foo"

    C(B(), X())


def test_exception_message():
    class A(metaclass=ABCMeta):
        @abstractmethod
        def foo(self):
            pass

    class B(A):
        def foo(self):
            return "B foo"

    b = B()
    with pytest.raises(AttributeError) as e:
        b.non_existent_method()

    assert e.value.args[0] == "'B' object has no attribute 'non_existent_method'"

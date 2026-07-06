from classmods import classproperty


class TestClass:
    _value = 1

    @classproperty
    def prop(cls):
        return cls._value

    _test = prop  # _test = 1


def test_property():
    """Access read-only class property via class and instance."""
    assert TestClass.prop == 1
    assert TestClass().prop == 1


def test_class_level_usage():
    """The descriptor can be assigned to another class attribute."""
    assert TestClass._test == 1
    assert TestClass()._test == 1


def test_metadata_preservation():
    """Ensure __doc__, __module__, __qualname__ are copied from the getter."""
    @classproperty
    def example(cls):
        """This is a docstring."""
        return 42

    assert example.__doc__ == "This is a docstring."
    assert example.__module__ == __name__  # the module of the decorated function
    # __qualname__ depends on where the function is defined; at top-level it's the function name
    assert "example" in example.__qualname__


def test_set_name_updates_name():
    """__set_name__ is called when the class is created, updating __name__."""
    class Foo:
        @classproperty
        def bar(cls):
            return 1

    # After class creation, __set_name__ sets __name__ to the attribute name
    prop = Foo.__dict__['bar']
    assert prop.__name__ == "bar"
    # Also check that the original function's __name__ is preserved? No, __set_name__ overrides.
    # Actually, property does this: it replaces __name__ with the attribute name.
    # So we test that it's "bar", not the function's original name (which would also be "bar" anyway).
    # To be thorough, let's define a function with a different name:

    def _helper(cls):
        return 1

    class Baz:
        prop = classproperty(_helper)

    prop2 = Baz.__dict__['prop']
    assert prop2.__name__ == "prop"  # __set_name__ has set it
    # The original function's __name__ was "_helper", but we override it.


def test_inheritance_and_overriding():
    """Subclasses inherit the property and can override it."""
    class Base:
        @classproperty
        def name(cls):
            return "Base"

    class Derived(Base):
        @classproperty
        def name(cls):
            return "Derived"

    assert Base.name == "Base"
    assert Derived.name == "Derived"


def test_assignment_replaces_descriptor():
    """Assigning to the class attribute overwrites the descriptor (no setter)."""
    class C:
        @classproperty
        def prop(cls):
            return 1

    assert C.prop == 1

    # Assign a new value – the descriptor is replaced
    C.prop = 42  # type: ignore
    assert C.prop == 42          # no longer a descriptor, just a plain attribute

    # Instances still see the class attribute (if not shadowed)
    assert C().prop == 42


def test_instance_shadowing():
    """Instances can shadow the class property, but the descriptor still works on the class."""
    class C:
        @classproperty
        def prop(cls):
            return 1

    obj = C()
    assert obj.prop == 1    # uses descriptor

    # creates an instance attribute
    obj.prop = 2  # type: ignore
    assert obj.prop == 2    # instance attribute shadows the descriptor
    assert C.prop == 1      # class still has the descriptor

    del obj.prop            # delete instance attribute
    assert obj.prop == 1    # falls back to descriptor

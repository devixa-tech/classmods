# `classproperty`

`classproperty` is a lightweight Python descriptor that lets you define **class‑level computed attributes** with a simple decorator syntax. It works like the built‑in `property`, but for the class itself – the getter receives the class (not an instance) as its first argument.

---

## Why `classproperty`?

The built‑in `@property` works on **instances** – its getter receives `self` (the instance). If you need an attribute that is computed from the **class** itself (e.g., a default configuration, a registry, or a derived class constant), `classproperty` gives you a clean, declarative way to define it.

---


## Usage

### 1. Basic Read‑Only Class Property

```python
from classmods import classproperty

class MyClass:
    _base_url = "https://api.example.com"

    @classproperty
    def api_url(cls):
        return cls._base_url + "/v1"

print(MyClass.api_url)          # "https://api.example.com/v1"
```

Access from an instance also works, but the getter always receives the **class**:

```python
obj = MyClass()
print(obj.api_url)              # same result
```

### 2. Dynamic Values Based on Class Variables

```python
from classmods import classproperty

class Circle:
    pi = 3.14159

    @classproperty
    def area_formula(cls):
        return f"π × r²  (π ≈ {cls.pi})"

print(Circle.area_formula)      # "π × r²  (π ≈ 3.14159)"
```

### 3. Inheritance and Overriding

Subclasses inherit the property and can override it by re‑defining the decorated method.

```python
from classmods import classproperty

class Base:
    @classproperty
    def name(cls):
        return "Base"

class Derived(Base):
    @classproperty
    def name(cls):
        return "Derived"

print(Base.name)                # "Base"
print(Derived.name)             # "Derived"
```

### 4. Async Getters

Because `classproperty` simply returns whatever the getter returns, it works with `async def` getters as well – the caller will receive a coroutine and must `await` it.

```python
import asyncio

class AsyncDemo:
    @classproperty
    async def data(cls):
        await asyncio.sleep(0.1)
        return 42

coro = AsyncDemo.data          # <coroutine object>
result = asyncio.run(coro)     # 42
```

---

## Important Limitations

- **Read‑only** – `classproperty` does **not** support setters or deleters. Assignment to the property on the class will **replace** the descriptor with the assigned value (just like a normal class attribute).
  
  ```python
  MyClass.api_url = "new"   # overwrites the descriptor, not calling a setter
  ```

- **No `__set__` or `__delete__`** – this is by design for a minimal read‑only implementation.

- **Class‑level assignment** – Python does not invoke the descriptor’s `__set__` when assigning to a class attribute; it simply replaces the attribute. This is consistent with how `property` behaves when assigned on the class. For writeable class properties, consider using classmethods.

---

## Comparison with `@property`

| Feature                     | `@property`                        | `classproperty`                 |
|-----------------------------|------------------------------------|---------------------------------|
| Getter receives             | instance (`self`)                  | class (`cls`)                   |
| Can be accessed from class? | No                                 | Yes                             |
| Supports setter/deleter     | Yes                                | No                              |
| Intended for                | instance‑level computed attributes | class‑level computed attributes |

---

## Use Cases

- Class constants that depend on other class attributes.
- Factory methods returning subclasses.
- Configuration defaults that can be overridden per subclass.
- Lazy‑loaded class‑level resources.

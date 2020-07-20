# Expecthon

python spec testing framework. This aims to help make tests as readable as
possible, by composing your tests in natural language.

## Install

TBA

## Examples

A very simple example

```python
expect(
   that(5+5).equal(10).and_.is_divisble_by(5)
   & that(7+4).equal(11).and_.isnt_divisble_by(5)
)
```

Lists and enumerators (like the `range` generator), have a whole bunch of
relevant helper methods, and by creating functions with readable names, it is
easy to create natural language tests.

```python

def is_divisble_by(value):
 return lambda element: element % value

def is_less_than(value):
  return lambda element: element < value

expect(
   that_list(range(0,10)).and_.any_(is_divisble_by(5)).and_.all_(is_less_than(10))
)
```


## Personal tips

If Django is installed then you can utilize the following bindings:

```python
expect(
   that_response(client.get(reverse('index'))).is_successful().and.contains("Hello World")
)
```

## extension

TBA

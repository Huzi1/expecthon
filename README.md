# expecthon
python spec testing framework. This aims to help make tests as readable as possible, by composing your tests in natural language. Highly extensible

## Install
TBA

## Examples
A very simple example
```python
expect(
   that(5+5).to_equal(10).and.be_divisble_by(5)
   & not that(7+4).to_equal(10).and.be_divisble_by(5)
)
```

If django is installed then you can utilize the following bindings:
```python
expect(
   that_response(client.get(reverse('index'))).is_successful().and.contains("Hello World")
)
```

## extension
TBA

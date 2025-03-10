# blind_signature
A test in python that aims to implement the blind signature algorithm

## Things to learn

* File system api for creating files: DONE
* Python program arguments: DONE
* OpenSSL interaction to create RSA keys
* Python socket api

### File system api

To create files we use

```python
file = open("path/to/file", "mode")
```

Where mode can be

* "r": Read
* "w": Write
* "a": Append
* "x": Create

And reading an writing modes we have:

* "t": For text
* "b": For binary data

### Python program arguments

Using `sys` module

```python
import sys

arguments = sys.argv
```

### OpenSSL interaction



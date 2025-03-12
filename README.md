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

Using `subprocess` module

```python
import subrocess as sub

gen_key_args = ["openssl", "genrsa", "-out", KEY_FILE, "2048"]
extract_pub_args = ["openssl", "rsa", "-in", KEY_FILE, "-outform", "PEM", "-pubout", "-out", PUBLIC_KEY_FILE]

sub.call(gen_key_args)
sub.call(extract_pub_args)
```

## Algorithm development

The client needs the following parameters at the beginning:

* RSA n parameter (public)
* RSA e parameter (public)
* Hash h (private)

The issuer needs the following parameters at the end

* RSA d parameter (private)
* RSA e parameter (public)

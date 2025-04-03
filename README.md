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

## Algorithm sequence

1. Client: Prepares the message to be signed by computing:

```python
input_msg = Prepare(msg)
```

2. Client: Initiates the blind signature protocol by computing:

```python
blinded_msg, inv = Blind(pk, input_msg)
```

3. Server: Receives the blinded message from the client and signs it:

```python
blind_sig = BlindSign(sk, blinded_msg)
```

4. Client: The client receives the signature and finalizes the protocol by computing:

```python
sig = Finalize(pk, input_msg, blind_sig, inv)
```

```mermaid
   Client(pk, msg)                      Server(sk, pk)
  -----------------------------------------------------
  input_msg = Prepare(msg)
  blinded_msg, inv = Blind(pk, input_msg)

                        blinded_msg
                        ---------->

                 blind_sig = BlindSign(sk, blinded_msg)

                         blind_sig
                        <----------

  sig = Finalize(pk, input_msg, blind_sig, inv)
```

## Implementation details

* This implementation uses the identity preparation function (skips the preparation step).

## Bibliography

* Original Chaum paper: <http://www.hit.bme.hu/~buttyan/courses/BMEVIHIM219/2009/Chaum.BlindSigForPayment.1982.PDF>
* RSA blind signature protocol: <https://www.rfc-editor.org/rfc/rfc9474.html#name-blind-signature-protocol>
* Python Cryptography documentation: <https://cryptography.io/en/latest/>

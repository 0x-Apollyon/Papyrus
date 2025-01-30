# Papyrus 
##### A comprehensive framework for python sourcecode obfuscation, evasion and anti analysis.
##### Papyrus makes use of many techniques to make python source code less readable and secure against static analysis.

## Modules
### Crypter
Basic obfuscation of functions, variables, objects and imports. Makes code less readable.
### Compression
Compression based obfuscation. Obfuscates code by running it through the LZMA compression algorithm
### Anti Analysis
Adds code which makes analysis difficult by detecting debuggers, VM environments and more.
### Encryption
XOR cipher based obfuscation. Obfuscates the code by encrypting it with a random key in a set keyspace
### Polymorphism and anti entropy
Makes the code polymorphic and also reduces Shanon entropy of the code by encoding parts with RLE (Run Length Encoding) and LZW (Lempel-Ziv-Welch)

## A more detailed description of techniques used will be out soon

## TODO
1) Make the obfuscated code more compact as the obfuscation processes leads to size explosion.
2) A post-compile module py2exe or pyinstaller executables
3) Control flow obfuscation
4) Better polymorphism by messing with the control flow itself (Rearrangements of the nodes of the CFG on runtime)


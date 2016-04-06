# Nopecrypt

An intersting idea I had to encrypt a file: divide it in chunks and use a chunk to XOR the next one ! 

I don't know much about cryptography but I wanted to try this out. These python script let you encrypt a file this way, the key is used only to encrypt the last chunk !

It actually is a CBC algorithm but without cipher ^^ (except that the IV is used at the end and not at the beginning).

I am sure it is simple to crack but it must still be a little challenging without any information about the original data.
Of course, it could be made more complicated by scrambling the chunks, overlapping the blocks and repeating the process multiple times...

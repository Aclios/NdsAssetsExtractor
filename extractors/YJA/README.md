# theresia -テレジア- Dear Emile (Aksys Games)

Most assets from the game can be exported, but:

- Some bg entries are skipped because the decompressed files (huffman) are not valid NCGR. Might be a decompression issue.

- Scripts are stored in a very annoying way: all the text for a script is concatened in one file with no terminator, meaning offsets and sizes (that are stored in the .adv script files) are required. Also there is no line breaks, each line is a text entry. So while all the text is extracted, it's not very convenient and additional work to reorganize it would be good. The japanese and NA versions also work a bit differently since the JP version uses common.txt files that contain the concatened strings for several scripts while the NA version has one txt file per script.

Also, there seems a bunch of unused text in the japanese version, between 0x3106d and 0x39d3b in the sub/common.txt file (after decompression). This text is dumped in an unknown_text.txt, however as explained above it's a concatenation of a lot of different entries that can't be automatically split.
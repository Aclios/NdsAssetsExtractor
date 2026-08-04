# theresia Dear Emile (Aksys Games)

Most assets from the game can be exported, but:

- Some bg entries are skipped because the decompressed files (huffman) are not valid NCGR. Might be a decompression issue.

- Scripts are stored in a very annoying way: all the text for a script is concatened in one file with no terminator, meaning offsets and sizes (that are stored in the .adv script files) are required. Also there is no line breaks, each line is a text entry. So while all the text is extracted, it's not very convenient and additional work to reorganize it would be good.
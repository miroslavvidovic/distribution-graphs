# distribution-graphs

## Synopsis
Wrapper for creating ASCII graphical histograms in the terminal with https://github.com/philovivero/distribution

## Requirements
- [distribution](https://github.com/philovivero/distribution)

## Why do we need it?
Because I am to lazy to type long commands and I prefer to have wrappers or aliases.

This is an example:
```bash
    du -s ~/Downloads/* 2>/dev/null | python distribution.py -g -v --color --char=ba --size=large
```

And this is the "wrapped" version:
```python
    dgraph.py space_usage ~/Downloads
```

## License

MIT

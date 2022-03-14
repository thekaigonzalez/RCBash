# Windows Contribution

## Limitations

When using the windows platform, here are somethings you might want to know about:

- Windows does not have as many commands or a PATH, you should be able to use Cygwin, but it hasn't been tested.
- As mentioned above, RCBash uses a lot of POSIX-based features, so Cygwin might serve correct, but on base windows NT, it doesn't work properly.


## Things to know

- Windows users can still use the base RCBash language features, it is a non-dependent programming language, with only around a max of **3** imports, for the base lexers, evaluator, and RCDocs.
- RCDoc is still 100% avilable, using the base APIs that Python provides.
ProtoBufCodeFormatter_Sublime
=============================

Sublime plugin that allows auto-formatting of Protocol Buffer Code.

Limitations
===========
1. Formatter cannot preserve order of structures

2. For comments, outer `extend' groups are logically grouped together, so inner comments are lost

3. Style of comments are not preserved (/* */ vs. //), so single-line comments are shown with `//` and multi-line comments with `/* */`.

4. Any comments not directly adjacent to a line of code, are not preserved.  Comments must be directly above or below a line of code (without newlines).


Installation
============
`ProtoBufCodeFormatter` is available via [Package Control][pkg-ctrl] and can be found as `ProtoBufCodeFormatter`.

[pkg-ctrl]: http://wbond.net/sublime_packages/package_control

*Important this plugin uses the `GOPATH`, please set it in `Settings - User`.


Requirements
============

- [Golang][go] v1.0 or higher
- Correctly set `PROTOPATH` and `GOBIN` in the `.sublime-settings file`.


In the package folder, edit the `CodeFormatter.sublime-settings` to contain the correct path information.  Under `GOBIN`, enter the location of your Go Binary.  Under `PROTOPATH`, enter any locations of Protocol Buffers that are imported by your protocol buffers.

 
[go]: http://golang.org/

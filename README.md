ProtoBufCodeFormatter_Sublime
=============================

Sublime-Text-2 plugin that allows auto-formatting of Protocol Buffer Code on save.

Installation
============
`ProtoBufCodeFormatter` is available via [Package Control][pkg-ctrl] and can be found as `ProtoBufCodeFormatter`.

[pkg-ctrl]: http://wbond.net/sublime_packages/package_control

*Important this plugin uses the `GOPATH`, please set it in `Settings - User`.


Requirements
============

- [Golang][go] v1.0 or higher
- Correctly set `PROTOPATH`, `GOROOT` and `GOBIN` in the `Settings - User`.


Open `Settings - User` under `Preferences/Package Settings` and edit to contain the correct path information.  Add variable `GOBIN` and enter the location of your Go Binary.  Add variable `PROTOPATH` and enter any locations of Protocol Buffers that are imported by your protocol buffers.  Optionally add a `GOROOT` variable to show the location of your Go workspace.  Look at `Settings - Default` as an example.

[go]: http://golang.org/


Limitations
===========
1. Formatter cannot preserve order of structures.  The order is pre-determined.

2. For comments, outer `extend' groups are logically grouped together, so inner comments are lost.

3. Style of comments are not preserved (/* */ vs. //), so both single-line and multi-line comments are shown with `//`.

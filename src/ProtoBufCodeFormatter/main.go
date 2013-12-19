package main

import (
	parser "./parser"
	"fmt"
	"os"
	"path"
	"path/filepath"
	"strings"
)

func main() {

	testFile := os.Args[1]
	var paths []string
	if len(os.Args) > 2 {
		paths = filepath.SplitList(os.Args[2])
	}
	os.Stdout.WriteString("paths joined: " + strings.Join(paths, ":") + "\n")
	os.Stdout.WriteString("filename: " + testFile + "\n")

	d, err := parser.ParseFile(testFile, paths)
	if err != nil {
		fmt.Println(err)
	} else {
		fo, _ := os.Create(testFile)

		formattedFile := d.Fmt(path.Base(testFile))

		fo.WriteString(formattedFile)
		fo.Close()
	}
}

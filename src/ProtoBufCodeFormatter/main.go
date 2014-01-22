package main

import (
	parser "ProtoBufCodeFormatter/parser"
	"errors"
	"fmt"
	"os"
	"path"
)

func main() {

	if len(os.Args) <= 1 {
		fmt.Println(errors.New("Not enough argument!"))
		os.Exit(1)
	}
	testFile := os.Args[1]
	var paths string
	if len(os.Args) > 2 {
		paths = os.Args[2]
	}
	os.Stdout.WriteString("paths joined: " + paths + "\n")
	os.Stdout.WriteString("filename: " + testFile + "\n")

	d, err := parser.ParseFile(testFile, paths)
	if err != nil {
		fmt.Println("Parse error:", err)
	} else {
		fo, _ := os.Create(testFile)

		formattedFile := d.Fmt(path.Base(testFile))

		fo.WriteString(formattedFile)
		fo.Close()
	}
}

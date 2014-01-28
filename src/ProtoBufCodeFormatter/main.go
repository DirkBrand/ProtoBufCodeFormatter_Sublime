package main

import (
	parser "ProtoBufCodeFormatter/parser"
	"errors"
	"fmt"
	"os"
	"path"
	"strings"
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

	d, err := parser.ParseFile(testFile, paths)
	if err != nil {
		os.Stderr.WriteString(fmt.Sprintf("%v", err))
	} else {
		fo, _ := os.Create(testFile)

		formattedFile := d.Fmt(path.Base(testFile))

		fo.WriteString(strings.TrimSpace(formattedFile))
		fo.Close()
	}
}

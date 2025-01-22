Document: flex
Title: flex
Author: various
Abstract: Fast LEXical analyzer generator
 Flex is a tool for generating programs that perform pattern-matching on
 text.  It generates "scanners": programs which recognized lexical
 patterns in text.  `flex' reads the given input files, or its
 standard input if no file names are given, for a description of a
 scanner to generate.  The description is in the form of pairs of
 regular expressions and C code, called "rules". `flex' generates as
 output a C source file, `lex.yy.c', which defines a routine
 `yylex()'.  This file is compiled and linked with the `-lfl' library
 to produce an executable.  When the executable is run, it analyzes
 its input for occurrences of the regular expressions. Whenever it
 finds one, it executes the corresponding C code.
Section: Programming

Format: info
Index: /usr/share/info/flex.info.gz
Files: /usr/share/info/flex.info-1.gz /usr/share/info/flex.info-2.gz

# C99 Headers Generator

# Installation
```bash
pip install headgen
pip3 install headgen
```
# Running
```bash
python -m headgen
```
# Ignoring files
You need to place file '.headignore' file in any sub directory
There you can place patterns patterns of ignoring files (same as gitignore patterns)
Example:
```
main.c
*hello.c
```
# Flags

| flag                    | using                                         | default           |
| ----------------------- | --------------------------------------------- | ----------------- |
| -a, --ask               | You wil be asked before doing anything        | False             |
| -h, --help              | Help message                                  |                   |
| -dp, --disable_printing | No output to a terminal                       | False             |
| -p, --pragma            | Sets protection with pragma                   | False             |
| -if, --ifndef           | Sets protection with ifndef                   | True              |
| -f, --file              | Sets the path to the file for creating header |                   |
| -d --dir                | Sets new directory for searching files        | Current directory |


# Organization

## Functions signatures and documentation
```c
/* 
This is an example in file main.c
Signature will be added automatically

Documentation can be placed anywhere.
*/



int sum_two(int a, int b){
	return a + b;
}


int sum_three(int a, int b, int c)
{
	return a + b + c;
}

/* headgen::link::sum_two
This is a documentation for sum_two function
It is very important to put headgen::link::<func_name> 
*/

```
This is a created header file
```c
/*
This file was generated automatically!
Header was created from file: 
    main.c
Generated at : 11 December 2019 (11.12.2019) At: 11:42:11
Functions amount     : 2
Functions fully documentated: True
Functions' names:
    1 > sum_two
    2 > sum_three
*/


#ifndef __MAIN_H__
#define __MAIN_H__

/* 
This is a documentation for sum_two function
It is very important to put headgen::link::<func_name>
*/
int sum_two(int a, int b);


int sum_three(int a, int b, int c);

#endif /* __MAIN_H__ */
```


## Includes
```c
/* headgen::includes::
std: stdio.h
std: string.h
loc: mylib.h
*/

// or if you want to sort imports

/* headgen::includes:: headgen::sort::enable
std: stdio.h
std: string.h
loc: mylib.h
*/
```
Created header: 
```c
/*
This file was generated automatically!
Header was created from file: 
    main.c
Generated at : 11 December 2019 (11.12.2019) At: 11:49:10
Functions amount     : 0
Functions fully documentated: True
Functions' names:


*/
#ifndef __MAIN_H__
#define __MAIN_H__


#include <stdio.h>
#include <stdio.h>
#include <string.h>
#include <string.h>
#include "mylib.h"
#include "mylib.h"



#endif /* __MAIN_H__ */
```

## Defines
All defines are placed after includes by default.

You can set some defines to be stored before includes

```
/* headgen::includes::
std: stdio.h
*/

// This define will not be added to a header
#define Hello 1 //headgen::no_add::

#define IM_PLACED_AFTER_INCLUDES 0

#define IM_PLACED_BEFORE_INCLUDES 1 //headgen::place_before::includes

```
Generated header
```c
/*
This file was generated automatically!
Header was created from file: 
    main.c
Generated at : 11 December 2019 (11.12.2019) At: 11:53:32
Functions amount     : 0
Functions fully documentated: True
Functions' names:


*/
#ifndef __MAIN_H__
#define __MAIN_H__

#define IM_PLACED_BEFORE_INCLUDES 1

#include <stdio.h>

#define IM_PLACED_AFTER_INCLUDES 0


#endif /* __MAIN_H__ */
```

## Structires and Enums
```

/* headgen::watch::struct
typedef struct{
	int x;
}i_am_added_to_header;
*/

/* headgen::watch::enum
enum{
	error, 
	no_error,
};
*/

```
Generated header
```c
/*
This file was generated automatically!
Header was created from file: 
    main.c
Generated at : 11 December 2019 (11.12.2019) At: 11:56:29
Functions amount     : 0
Functions fully documentated: True
Functions' names:


*/

#ifndef __MAIN_H__
#define __MAIN_H__

enum{
	error,
	no_error,
};


typedef struct{
	int x;
}i_am_added_to_header;

#endif /* __MAIN_H__ */
```
# ENJOY
# dirgen
Generate files and folders from structured JSON, Python, or text


## Installation
```bash
pip install dirgen 
```

## Dependencies
- Python: 3.12

See [requirements.txt](https://github.com/Justin-Morrison-github/DirGen/blob/master/requirements.txt)


## Usage

Run with set default mode and file:
```bash
dirgen 
```
Run with default python file:
```bash
dirgen -py
```
Run with default json file:
```bash
dirgen -j
```
Run with text provided:
- text must be surrounded with double qoutes `""` and folder/file names should be within single qoutes `''`
- text must be valid json syntax
```bash
dirgen -t "{'A':['test.py', 'test.c'], 'B': '$'}"
```
         
### Arguments
Arguements that can be passed

        -set, --set=OPTION VALUE
                set program options
              
        -get, --get=OPTION
                get program options

        -v, --verbose
                print message for each created file/folder

        -c, --cache=OPTION
                used in conjuction with -del and -clr

        -clr, --clear[=OPTION]
                clear the program (empty the cache...), or if OPTION specified then clear that OPTION
        
        -m, --mode[=MODE]
                print current operating mode, if MODE sepcified then set operating mode to MODE

        --context[=CTX]
                like -Z, or if CTX is specified then set the SELinux or
                SMACK security context to CTX

        --help display this help and exit

        --version
                output version information and exit

<!-- - `-m`, `--mode=Option New_Data` 
    <div style="margin-top: 10px;"></div>      
    flag to set_default
    <div style="margin-top: 10px;"></div>      

    Example:
    ```bash
        dirgen -m
        dirgen --mode
    ``` -->

-------

       -m, --mode=MODE
              set file mode (as in chmod), not a=rwx - umask

       -p, --parents
              no error if existing, make parent directories as needed,
              with their file modes unaffected by any -m option

       -v, --verbose
              print a message for each created directory

       -Z     set SELinux security context of each created directory to
              the default type

       --context[=CTX]
              like -Z, or if CTX is specified then set the SELinux or
              SMACK security context to CTX

       --help display this help and exit

       --version
              output version information and exit

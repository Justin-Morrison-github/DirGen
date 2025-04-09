# dirgen
Generate files and folders from structured JSON, Python, or text


## Installation
```bash
pip install dirgen 
```

## Dependencies
See [requiremnts.txt](https://github.com/Justin-Morrison-github/DirGen)



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

    Text here

- `-cache`, `--cache` 
    <div style="margin-top: 10px;"></div>      
    flag to access cache  
    <div style="margin-top: 10px;"></div>      


    Example:
    ```bash
        dirgen -cache
        dirgen --cache
    ```
        
- `-clr`, `--clear=[Option]` 
    <div style="margin-top: 10px;"></div>      
    flag to clear given option  
    <div style="margin-top: 10px;"></div>      


    Example:
    ```bash
        dirgen -clr
        dirgen --clear
    ```
        

- `-set`, `--set=Option New_Data` 
    <div style="margin-top: 10px;"></div>      
    flag to set options
    <div style="margin-top: 10px;"></div>      

    Example:
    ```bash
        dirgen -set
        dirgen --set
    ```

- `-m`, `--mode=Option New_Data` 
    <div style="margin-top: 10px;"></div>      
    flag to set_default
    <div style="margin-top: 10px;"></div>      

    Example:
    ```bash
        dirgen -m
        dirgen --mode
    ```

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

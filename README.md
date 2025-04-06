# DirGen
Generate files and folders from structured JSON, Python, or text


## Usage


```bash
DirGen 
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
        DirGen -cache
        DirGen --cache
    ```
        
- `-clr`, `--clear=[Option]` 
    <div style="margin-top: 10px;"></div>      
    flag to clear given option  
    <div style="margin-top: 10px;"></div>      


    Example:
    ```bash
        DirGen -clr
        DirGen --clear
    ```
        

- `-p`, `--print=[Option]` 
    <div style="margin-top: 10px;"></div>      
    flag to print, if no option given print ___
    <div style="margin-top: 10px;"></div>      

    Example:
    ```bash
        DirGen -p
        DirGen --print
    ```

- `-sd`, `--set_default=Option New_Data` 
    <div style="margin-top: 10px;"></div>      
    flag to set_default
    <div style="margin-top: 10px;"></div>      

    Example:
    ```bash
        DirGen -sd
        DirGen --set_default
    ```

- `-m`, `--mode=Option New_Data` 
    <div style="margin-top: 10px;"></div>      
    flag to set_default
    <div style="margin-top: 10px;"></div>      

    Example:
    ```bash
        DirGen -m
        DirGen --mode
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
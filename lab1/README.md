# Metaprograming lab1 
Code formatter

## Requirements
**Python 3.4+** is required

## How to run
```
python main.py -h
 ```
for get help  

```
python main.py FORMAT P_D_F PATH 
python main.py FORMAT TEMPLATE_NAME P_D_F PATH 
```
for work, where
```
    FORMAT          format of work; in ('-f', '--format', '-v', '--validate')
    TEMPLATE_NAME   name of template file
    P_D_F           select it will be file or diractory; in ('-p', '-d', '-f')
    PATH            path to file/directory
```

## Examples
```
python main.py -v -f test.java
```

```
python main.py -f template.json -d examples
```
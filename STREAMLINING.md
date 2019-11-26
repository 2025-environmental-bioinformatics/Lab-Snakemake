# Streamlining Snakemake
@(Teaching)

If you take a look at the `Snakefile` we have built during class you should notice that is fairly redundant. It has a lot of duplication. 

For example, the names of text files and data files are repeated in many places throughout the `Snakefile`. Just as with coding in python or the like-- it is better to try to reduce duplication or long verbose code that could be simplified. Think of each rule as a function that we define in python-- it is better to have one function that can work with many inputs rather than lots of copies of the same code. 

## Wildcards
Let's try to clean up our code a bit. We can start with fixing our `rule results`. 

Currently you probably have something like:

```python
rule results:
    input:
        'siddartha.dat', 
        'five.dat', 
        'sign.dat'
    output:
        'results.txt'
    shell:
        '''
        python compare_books.py siddartha.dat five.dat sign.dat > results.txt
        '''
```

We are actually able to call input and output directly in our shell commands so that we don't have to type out file names. This can be done with `{input}` and  `{output}` wildcards. `{input}` and `{output}` stand in automatically for the values that we specified within that rule for input and output. 

This makes it much easier to write. So, the above rule can become:

```python
rule results:
    input:
        'siddartha.dat', 
        'five.dat', 
        'sign.dat'
    output:
        'results.txt'
    shell:
        '''
        python compare_books.py {input} > {output}
        '''
```
Copy this rule and see if it still works! You might want to run `snakmake clean` beforehand... 

Run `snakemake -np` what happens? What does it print? 

> Stop and think: Which files would be recalculated by snakemake if you ran:
> ``` bash
> touch *.dat
>snakemake results.txt
>```

## Multiple inputs and outputs

For many rules, we may want to treat some dependencies differently, or have multiple different sorts of dependencies. 

Our `word_count*` rules currently use their first (and only) dependency specifically as the input file to `wordcount.py`. 

If we add additional dependencies then we don’t want all of the inputs to be passed as input files to `wordcount.py` as it expects only one input file to be named when it is invoked. 

Let's try to add `wordcount.py` as a dependency. 

> What are some reasons having the custom script you wrote be an input or dependency in Snakemake? 

There are several ways to do this: 

###  1. Indexing the input wildcard
```
rule count_words:
    input:  'wordcount.py', 'novels/siddartha.txt'
    output: 'siddartha.dat'
    shell:  'python {input[0]} {input[1]} {output}'
```

### 2. Naming dependencies

```
rule count_words_five:
    input: 
        novel = 'novels/five.txt', 
        script = 'wordcount.py'
    output: 'five.dat'
    shell:
        '''
        python {input.script} {input.novel} {output}
        '''
```







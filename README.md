# Snakemake and automation
@(Teaching)

## Exercise to motivate class

In the beginning of class, we will make a conda environment: 
```
mamba create -n snakemake-class -c bioconda snakemake=7.32.4 fastqc multiqc trimmomatic plotnine matplotlib
```

and clone the GitHub repo:

```
git clone git@github.com:2019-MIT-Environmental-Bioinformatics/Lab-Snakemake.git

```

![Groundhog Day](./images/groundhog.gif)

We will assemble into groups where each group examines a separate coding approach, stored in `group-exercises`. These data are from [kaggle](https://www.kaggle.com/datasets/groundhogclub/groundhog-day/), and they display the decision of the Groundhog to either celebrate the beginning of Spring or declare 6 more weeks of winter. 

Aggregate and regional mean temperature data for the months of February and March are also included, which serve to determine whether the Groundhog was right in its 2 February prediction for the next 6 weeks. 

### What is the objective of this code?

We want to calculate the mean of air temperatures in the event that the groundhog sees their Full Shadow vs Partial Shadow vs No Shadow. We also want to calculate the change in temperature - does the Groundhog correctly predict how fast temperatures will change, if not by how much?

### What are we trying to do in teams?

You have fifteen minutes to do this - this is a hard cutoff! Use the time wisely and try to get to executing the scripts right away.

1. Navigate to `group-exercises` and find the `group-n.py` file that corresponds to the `n` that your group was assigned.
2. Read through the Python code used for this calculation and see if you can spot any errors right away.
3. Check for syntax errors by executing `python group-n.py`; address these first
4. After you get the code working properly, navigate to `inclass-solutions/group-exercises` and execute `python group-n.py` with your group number.
5. Compare `inclass-solutions/results` to `results` by checking the printed output block when you execute each script (hint: use a `tmux` session rather than trying to scroll).
6. When you're satisfied, `scp` the images from `results` to your local computer - as long as your code matched the solutions, this is the real answer for whether empirical data supports the validity of the Groundhog Method. (Hint: use `scp <username>@poseidon-l1.whoi.edu:/vortexfs1/omics/env-bio/users/<username>/Lab-Python/results <local location desired>`; this is executed from your _local computer_).
7. Brainstorm ways that you might improve this code. Jot down some notes as a group if you get this far! 

## What are makefiles

You may have run into Makefiles before while installing a bioinformatic (before the advent of conda). The `make` utility requires a file generally called `Makefile` (or `makefile`), which defines set of tasks to be executed or the installation instructions. Let's take a look at an example. Go to: http://hmmer.org/ and click `Download source`. Once it is has downloaded unzip the file and take a look at the Install instructions. [conda install can be found [here](https://anaconda.org/bioconda/hmmer)]. If you take a look at the install instructions you see something like this:

```
Starting from a source distribution, hmmer-3.3.tar.gz:
   uncompress hmmer-3.3.tar.gz  
   tar xf hmmer-3.3.tar
   cd hmmer-3.3
   ./configure
   make
   make check                        # optional: automated tests
   make install                      # optional: install HMMER programs and man pages
   (cd easel; make install)          # optional: install Easel tools too
```
More generally, makefiles and make can be used to specify a set of instructions for the creation of a file or set of files. For example, I made a [simple makefile](https://github.com/halexand/MIT_Latex/blob/master/Makefile) that streamlined the compilation of my Thesis in Latex. 

## What is Snakemake? 

Snakemake is a Python-based workflow management tool that is based on GNU Make. Snakemake requires a build file which for Snakemake is called `Snakefile`. 

Snakemake is distinct from other text-based workflow systems in that it seamlessly allows you to hook into the Python interpreter. This means that you can define rules as an extension of Python ... if you can code in Python you can easily learn Snakemake. This allows you to combine the flexibility of a plain scripting language with a Pythonic workflow definition. 

Generally speaking, Snakemake is a **workflow** that contains a set of **rules** that describe the task that needs to be done. 

Within `Snakemake`: 
- A workflow contains a set of rules
- A rule describes how to create output files/patterns from input files/pattern
- The workflow file runs like a Python script

`Snakemake` can:
- Import  Python libraries
- Write and integrate functions from python
- Call external programs
- Associate individual rules with specific conda environment and build those environments for you
- Run the submission of jobs to an HPC
- Simplify your bioinformatic life (<span style="font-variant:small-caps;">Results may vary</span>)
 
## A simple example

Today, I am going to be pulling a bit from the `Carpentries` snakemake tutorial. Feel free to go give it a look!

In your copy of `Lab-Snakemake` make a directory called `novels`. Navigate into novels and copy this chunk of code to download a free copy of *Siddartha* by Herman Hesse from project gutenberg. 

```
curl -L https://www.gutenberg.org/cache/epub/2500/pg2500.txt -o siddartha.txt
```

Now, let's make a simple snakemake file! Navigate into your copy of `Lab-Snakemake` and create a new empty file called `Snakefile`. Copy and paste this rule into the snakefile. 

```
rule count_words:
    input: 'novels/siddartha.txt'
    output: 'siddartha.dat'
    shell:
        '''
        python wordcount.py novels/siddartha.txt siddartha.dat
        '''
```

Now, we can execute it just by typing `snakemake`. Snakemake (like make) looks automatically for a file locally called `Snakefile`. Note, while many / all snakefiles are called `Snakefile` they don't have to. You can call it whatever you want and use the flag `-s` to specify the name of your alternative snakefile. 

By default, Snakemake should print a lot of text to let you know what it is doing:

```
Building DAG of jobs...
Using shell: /usr/bin/bash
Provided cores: 1
Rules claiming more threads will be scaled down.
Job counts:
        count   jobs
        1       count_words
        1

[Tue Nov 26 11:21:32 2019]
rule count_words:
    input: novels/siddartha.txt
    output: siddartha.dat
    jobid: 0

[Tue Nov 26 11:21:33 2019]
Finished job 0.
1 of 1 steps (100%) done

```

### What is Snakemake doing? 

**Line by line:**
- `#` is a comment -- just like in python -- and is ignored
- `rule` defines the name of the rule and ends with a `:` as with other blocks defining words (e.g. `for`)
- `input` defines the *dependency* for the rule. This file is required for the running of this rule. In this case it is `fortunes/fortune9`. 
- `output`defines the *target* for the rule-- this is the file that needs to be created or built. In this case, snakemake will look for the file `counts/fortune9.dat' to be created at the end of the running. 
- Note: as with python-- this relies on indentation. Everything after the rule line needs to be indented. 

### How does Snakemake work?

Generally, Snakemake will look at the final output files required by your `Snakefile` and figure out the rules that are required to create them. 
 - The rule will specify the required input files.
 - If the input files exist, then we are good to run the commands
 - If some input does not exist but there are rules to generate them, use those rules to find the required input files
 - Repeat the process until all outputs can be generated from existing files
 - Snakemake will start running the corresponding commands

Dependencies between the rules are determined automatically, creating a DAG (directed acyclic graph) of jobs that can be automatically parallelized.

In our simple example, we only have *one* rule... which is simple! Why even bother with snakemake? Well, in this particular case, there is no real reason. But what if we had 100s of files that we wanted to run through a pipeline that had 10s of steps? 



## It's all about the timing... 

Now, try running it again! Run `snakemake`. 

> What happened? Why? How does this compare to if we were running a script directly? 

Here, our target file, `siddartha.dat` already existed, and Snakemake knows it. Snakemake will not create a file again if it already exists. You can see how this type of functionality is *fantastic* especially if you are working with some sort of program that is resource-intensive. 

Let's dig into this a bit more: to see how this works. 

First, run `ls -l *dat */*txt` to see the time stamp on each of our files:

```
-rw-rw-r-- 1 halexander sg-envbio-mgr 241143 Nov 26 11:15 novels/siddartha.txt
-rw-rw-r-- 1 halexander sg-envbio-mgr 123793 Nov 26 11:43 siddartha.dat
```

Here, we can see that the target file `siddartha.dat` is *newer* than the dependency `siddartha.txt`. Let's change that. Use nano to make some change to `novels/siddartha.txt` (or you can just use `touch`). If you run `ls -l` again, you should see that `novels/siddartha.txt` is now older. 

Now, if we run `snakemake` again, it will recreate `siddartha.dat`. 

Why?

When it is asked to create a target, Snakemake checks the ‘last modification time’ of both the target and its dependencies. If any dependency has been updated since the target, then the actions are re-run to update the target. Using this approach, Snakemake knows to only rebuild the files that, either directly or indirectly, depend on the file that changed. This is called an *incremental build*.

## Adding more rules

Alright, now let's add another rule to our snakemake. But, before we do that, let's grab some more books. 

We will symbolically link some data that we are going to be using today. `ln` is a useful command for linking data to your working directory that you don't want to copy (imagine if you were working with really large files). `ln` works similarly to copy or mv -- you have to specify a file (or set of files) and a target location. Navigate into `novels/` and run:

```bash
ln -fs /vortexfs1/omics/env-bio/collaboration/books/*txt .
```

This will symbolically link the Sherlock Holmes stories we worked with for the first homework into the novels directory. Type 

> Type `ls -l`. What do you see? How are these different from siddartha.txt? 

Now, let's add another rule. Note, rules cannot have the same name so we can call this one `count_words_five`. Copy this into your `Snakefile`.  
```python
rule count_words_five:
    input: 'novels/five.txt'
    output: 'five.dat'
    shell:
        '''
        python wordcount.py novels/five.txt five.dat
        '''
```

Now, again, let's try running `snakemake`. What we expect-- is that it should build our new file right? But instead you probably got some sort of output like this:

```bash
Building DAG of jobs...
Nothing to be done.
``` 

Nothing happens because Snakemake attempts to build the first target it finds in the Snakefile. These first targets, the default target, here (`siddartha.dat`) is already up-to-date. However, we can explicitly tell snakemake that we want it to build the dat file for our new rule:

```bash
snakemake five.dat
```

Give us:

```

[Tue Nov 26 13:00:25 2019]
rule count_words_five:
    input: novels/five.txt
    output: five.dat
    jobid: 0

[Tue Nov 26 13:00:25 2019]
Finished job 0.
1 of 1 steps (100%) done
```

Let's add one more rule that helps us clean up after ourselves by removing all the .dat files. Add the following to your Snakefile.

```python
rule clean:
    shell: 'rm -f *.dat'
```
This rule has now inputs or outputs! It won't automatically be run (as you might have guessed). However, we can call it with `snakemake clean`. 

> Give it a try!  Type ls. What happened? 

## Rule all

As mentioned above, snakemake generally looks for the first targets within a snakefile and automatically makes sure that those targets are built. All other targets go by the wayside. 

As such, it is common practice to include a `rule all:` at the top of your `Snakefile` that lists all the files that should be created with your workflow. 

Add this to your `Snakefile`:

```python
rule all:
    input: 
    'siddartha.dat', 
    'five.dat'
```
Now what happens?  [I might have tried to build in an error here ;) ]

Since we ran `snakemake clean` above it should now be prompting you to make two files. 

We can actually ask Snakemake to visualize the rules that we have just written and how the interact with each other. 

```
snakemake --forceall --dag |dot -Tpdf > dag.pdf
```

> Take a look at dag.pdf. What does it show? 

## Some useful commands in running

It is often important to see what snakemake is doing behind the scenes. Some useful flags for execution are : 
- `-p` prints all commands it is about to run 
- `-n`runs a dry run. Basically-- when combined with `-p` you can print all the steps about to be run without asking snakemake to calculate them for you. 

> Try running snakemake with these flags. Run clean and then run these again. 

## Exercise Break! 

1. Write a new rule that calculates `sign.dat` from `sign.txt`.
2. Write a new rule called `results` that takes all the `.dat` files as input and runs `python compare_books.py *dat > results.txt`. 
3. Update clean so that it removes the targets we just made (`results.txt` and `sign.dat`)
    

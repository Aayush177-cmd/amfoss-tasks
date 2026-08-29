# LEVEL 6 — THE GREAT MERGE WAR AT LAUGH TALE

## Repository
Laugh-Tale-Merge-War

## Target Path
~/Laugh-Tale-Merge-War/

## Objective

The main objective of this level was to resolve the Git merge conflicts between two distinct branches and recover the final key required to successfully complete the task.

## My Approach

First, I checked all the available branches using:

    git branch -a

After identifying the required branch, I merged the `pirate_king_path` branch into the current branch using:

    git merge origin/pirate_king_path

After running the merge command, Git reported conflicts in the following files:

    treasure/key_part_1.txt
    treasure/key_part_2.txt

I then navigated into the `treasure` directory:

    cd treasure/

I opened both text files one by one and inspected the conflicting sections. I manually removed the Git conflict markers and kept the correct key fragments from the two branches.

After resolving the conflicts in both files, I staged the modified files using:

    git add treasure/key_part_1.txt treasure/key_part_2.txt

I then committed the resolved merge:

    git commit

After the commit was completed, I checked the two `.txt` files again to obtain the final fragmented key. Combining the fragments gave the Pirate King's password.

Finally, I executed the victory script:

    ./victory.sh

The script asked for the Pirate King's Password. I entered the recovered password, which successfully completed the task.

## Commands Used

    git branch -a
    git merge origin/pirate_king_path
    cd treasure/
    cat key_part_1.txt
    cat key_part_2.txt
    git add treasure/key_part_1.txt treasure/key_part_2.txt
    git commit
    cat key_part_1.txt
    cat key_part_2.txt
    cd ..
    ./victory.sh

## Pirate King's Password

    TheGrandLineRemembers

## Result

Successfully resolved the Git merge conflicts, recovered the Pirate King's password, and completed the final level of the task.

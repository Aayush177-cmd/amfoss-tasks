# LEVEL 3 — THE WAX LABYRINTH OF LITTLE GARDEN

## Repository
Terminal-Voyage-User-Edition

## Target Path
~/Terminal-Voyage-User-Edition/GrandLine/Wax_Jungle/

## Objective

We need to find the hidden branch `little_garden`, switch to that branch using `git checkout`, and then locate a specific file among plenty of decoy files. After finding the file containing the required search string, we need to read it to pass this level.

## My Approach

First, I used the following command to find all the branches available in the repository:

    git branch -a

From the list of branches, I found the hidden branch:

    little_garden

I then switched to the branch using:

    git checkout little_garden

After switching to the required branch, I navigated to the `Wax_Jungle` directory:

    cd GrandLine/
    cd Wax_Jungle/

The directory contained many files and directories, so I needed to search for a specific string.

The flag obtained from Level 2 was:

    BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}

I encoded the Level 2 flag into Base64 format to obtain the search string.

The encoded string was then searched throughout the directory using `grep -r`:

    grep -r "QkFST1FVRV9ESUFMe1NQTElUX1RJTUVMSU5FX01JU0RJUkVDVElPTn0K"

After running the command, I found the location of the file containing the required string.

I then used the `cat` command to read the contents of the file:

    cat <file_path>

The file contained the clearance information and the required fragment for Level 3.

## Commands Used

    git branch -a
    git checkout little_garden
    cd GrandLine/
    cd Wax_Jungle/
    echo -n "BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}" | base64
    grep -r "QkFST1FVRV9ESUFMe1NQTElUX1RJTUVMSU5FX01JU0RJUkVDVElPTn0K"
    cat <file_path>

## Level 2 Flag Used

    BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}

## Fragment Obtained

    PONEGLYPH_FRAGMENT_1=KjY2MjF4bW01KzYqNyBsIS0vbTAtJIcnL

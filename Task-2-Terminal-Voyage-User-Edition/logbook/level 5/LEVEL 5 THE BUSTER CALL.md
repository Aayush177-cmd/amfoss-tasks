# LEVEL 5 — THE BUSTER CALL TIMELINE RECOVERY

## Repository
Terminal-Voyage-User-Edition

## Target Path
~/Terminal-Voyage-User-Edition/GrandLine/Enies_Lobby/.cp9_secure_vault/

## Objective

The objective of this task is to recover a deleted challenge file. We need to find the correct branch, inspect the Git commit history, move to the required commit, and locate the Python script inside the hidden directory. After running the script, we need to provide the required key fragments to unlock the next stage of the challenge.

## My Approach

First, I checked all the available branches using:

    git branch -a

From the available branches, I switched to the `alternate_timeline` branch using:

    git checkout alternate_timeline

After switching to the required branch, I checked the Git commit history using:

    git log --oneline

This command displays the Git commit history in a compact format, with each commit shown on a single line.

From the commit history, I identified the commit corresponding to Level 5, which was:

    d4e7bf5

I then switched to that specific commit using:

    git checkout d4e7bf5

After moving to the required commit, I navigated through the directories:

    cd GrandLine/
    cd Enies_Lobby/

Inside `Enies_Lobby`, I searched for the hidden directory:

    .cp9_secure_vault

I then entered the hidden directory:

    cd .cp9_secure_vault/

Inside the directory, I found the Python script:

    poneglyph.py

I ran the script using:

    python3 poneglyph.py

The script prompted me with:

    Enter code:

I entered the key fragments obtained from the previous levels as the required input.

After providing the correct fragments, the script successfully completed the level and provided a link directing to a Git repository containing the details for Level 6.

## Commands Used

    git branch -a
    git checkout alternate_timeline
    git log --oneline
    git checkout d4e7bf5
    cd GrandLine/
    cd Enies_Lobby/
    ls -la
    cd .cp9_secure_vault/
    ls
    python3 poneglyph.py

## Commit Used

    d4e7bf5

## Prize

https://github.com/rogueone-x/Laugh-Tale-Merge-War

## Result

Successfully completed Level 5 and obtained the repository link for Level 6.

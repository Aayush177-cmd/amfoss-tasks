# LEVEL 1 — AWAKENING AT LOGUETOWN REEF

## Repository
Terminal-Voyage-User-Edition

## Target Path
~/Terminal-Voyage-User-Edition/GrandLine/Loguetown_Reef/

## Objective

After ripping off the One Piece part, we could understand that there is a target file hidden amongst several hidden decoy files. The objective of this task is to find the hidden folder among the given sub-directories.

## My Approach

After I got into the needed repository, I navigated to the target directory:

    cd ~/Terminal-Voyage-User-Edition/GrandLine/Loguetown_Reef/

I individually went through all the sub-directories and searched for the hidden file using:

    ls -ls

After checking the different sectors, I spotted a unique file inside the `sector_C` directory:

    sector_C/devil_fruit_6.txt

After finding the unique file, I ran the `eat.sh` script on the target file:

    ./eat.sh sector_C/devil_fruit_6.txt

The script processed the file and revealed the flag.

## Commands Used

    cd ~/Terminal-Voyage-User-Edition/GrandLine/Loguetown_Reef/
    ls
    cd sector_A/
    ls -ls
    cd ../sector_B/
    ls -ls
    cd ../sector_C/
    ls -ls
    ./eat.sh sector_C/devil_fruit_6.txt

## Flag Obtained

    ONE_PIECE{GITO_GITO_NO_AWAKENING}

## Note

The  sector_C/devil_fruit_6.txt which is highlighted in green may not visible properly as my terminal text is also in green

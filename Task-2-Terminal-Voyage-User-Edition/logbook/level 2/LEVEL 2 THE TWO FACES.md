# LEVEL 2 — THE TWO FACES OF WHISKEY PEAK

## Repository
Terminal-Voyage-User-Edition

## Target Path
~/Terminal-Voyage-User-Edition/GrandLine/Whiskey_Peak/.baroque_works_cache/

## OBJECTIVE

We need to find the hidden branch and investigate the hidden directory in Whiskey Peak. Then, run the unlock script using the flag obtained from Level 1 and follow the steps given in the script to progress further in the task.

## MY APPROACH

After completing Level 1, I had to change the branch as the task required me to access another branch. I first used:

    git branch -a

This displayed the available branches, including the hidden investigation branch. I then switched to it using:

    git checkout whiskey_peak_investigation

After switching branches, I navigated to the Whiskey Peak directory and used:

    ls -a

This allowed me to see the hidden files and directories. Among them, I found the hidden directory:

    .baroque_works_cache

I entered the directory and inspected its contents. The important file found there was:

    unlock.sh

Instead of directly executing the script, I opened it using:

    nano unlock.sh

Inside `unlock.sh`, there was an expected target hash that needed to match the hash generated from the Level 1 flag.

The script contained the following command:

    INPUT_HASH=$(echo -n "$AWAKENING_SIGNATURE" | sha256sum | awk '{print $1}')

I used the Level 1 flag as the `AWAKENING_SIGNATURE`:

    ONE_PIECE{GITO_GITO_NO_AWAKENING}

The SHA-256 hash generated from this value was then compared with the expected hash present in `unlock.sh`.

After the hash matched, I followed the remaining instructions in the script.

The Level 2 flag was encrypted and had to be decrypted using the Level 1 flag as the password. The script used the following command:

    REAL_FLAG=$(echo "$ENCRYPTED_FLAG" | openssl enc -aes-256-cbc -d -a -pbkdf2 -iter 100000 -pass pass:"$AWAKENING_SIGNATURE" 2>/dev/null)

The encrypted flag value was supplied to `ENCRYPTED_FLAG`, while the Level 1 flag was used as the `AWAKENING_SIGNATURE`.

After executing the required commands, the encrypted Level 2 flag was successfully decrypted.

## COMMANDS USED

    git branch -a
    git checkout whiskey_peak_investigation
    cd GrandLine/
    cd Whiskey_Peak/
    ls -a
    cd .baroque_works_cache/
    ls
    nano unlock.sh
    ./unlock.sh

## LEVEL 1 FLAG USED

    ONE_PIECE{GITO_GITO_NO_AWAKENING}

## FLAG OBTAINED

    BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}

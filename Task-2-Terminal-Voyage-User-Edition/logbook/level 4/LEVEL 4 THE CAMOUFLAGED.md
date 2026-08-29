# LEVEL 4 — THE CAMOUFLAGED BLUEPRINTS OF WATER 7

## Repository
Terminal-Voyage-User-Edition

## Target Path
~/Terminal-Voyage-User-Edition/GrandLine/Water_7/galley_la_company/

## Objective

The objective of this task is to decrypt the corrupted blueprint file present in the `galley_la_company` directory. We need to identify the true format and identity of the file instead of relying on its given filename or missing file extension. After identifying the correct format, we need to extract the contents layer by layer to obtain the next key fragment.

## My Approach

First, I switched to the required branch, `canonical-timeline`, using:

    git branch -a
    git checkout canonical-timeline

After switching to the correct branch, I navigated to the `Water_7` directory and then to the `galley_la_company` directory:

    cd GrandLine/
    cd Water_7/
    cd galley_la_company/

Inside the directory, I found a file named:

    puffing_tom_blueprints

Since the file did not have a proper extension, I used the `file` command to identify its actual format:

    file puffing_tom_blueprints

The command showed that the file was actually a GZIP compressed file. I then renamed the file with the correct `.gz` extension:

    mv puffing_tom_blueprints puffing_tom_blueprints.gz

I then decompressed the GZIP file using:

    gunzip puffing_tom_blueprints.gz

After decompression, I used the `file` command again to identify the format of the resulting file. The file was identified as a TAR archive.

I listed the contents of the TAR archive using:

    tar -tf puffing_tom_blueprints

After checking the contents, I extracted the files using:

    tar -xf puffing_tom_blueprints

This resulted in another compressed file:

    step1_blueprints.zip

I then extracted the ZIP file using:

    unzip step1_blueprints.zip

After unzipping it, I navigated into the extracted directory and found the file:

    secret_link.txt

I read the contents of the file using:

    cat secret_link.txt

The file contained the next key fragment required for the task.

## Commands Used

    git branch -a
    git checkout canonical-timeline
    cd GrandLine/
    cd Water_7/
    cd galley_la_company/
    ls
    file puffing_tom_blueprints
    mv puffing_tom_blueprints puffing_tom_blueprints.gz
    ls
    file puffing_tom_blueprints.gz
    gunzip puffing_tom_blueprints.gz
    file puffing_tom_blueprints
    tar -tf puffing_tom_blueprints
    tar -xf puffing_tom_blueprints
    ls
    unzip step1_blueprints.zip
    ls
    cd blueprints_extracted/
    ls
    cat secret_link.txt

## Fragment Obtained

    PONEGLYPH_FRAGMENT_II="SwnbzptDiM3JSpvFiMuJ2BPjzAlJ28ViZA="

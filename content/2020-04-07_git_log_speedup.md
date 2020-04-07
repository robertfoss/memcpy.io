Title: Speed up `git log --graph` 18x times
Date: 2020-04-07 15:06
Category: developer
Tags: git, lg, log, format, pretty, slow, speed up, commit, graph
Description: For large repositories 'git log --graph' can be slow, but for git v2.20+ it can be sped up.

    $ time git lg
    git lg  13.34s user 0.87s system 84% cpu 16.845 total

    # True by default as of git v2.24
    git config --global core.commitGraph true
    git config --global gc.writeCommitGraph true

    # Command added in git v2.20
    git commit-graph write

    $ time git lg
    git lg  0.72s user 0.14s system 74% cpu 1.154 total

This is a speed up of ~18x, compared to the older versions.

The way this works is that the [commit-graph](https://git-scm.com/docs/commit-graph)
file stores the commit graph structure along with some extra metadata to
speed up graph in the `.git/objects/info` directory.

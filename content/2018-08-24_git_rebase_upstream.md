Title: git reset upstream
Date: 2018-08-24 12:32
Category: git
Tags: collabora, git, reset, upstream, pull, synchronize
Canonical: https://www.collabora.com/news-and-blog/blog/2018/08/27/quick-hack-git-reset-upstream/
Description: Working with a git based project that has a defacto upstream repository means that you perioducally want to fetch the canonical master branch. This can be simplified with a .gitconfig alias.

    robertfoss@xps9570 ~/work/libdrm $ git ru
    remote: Counting objects: 234, done.
    remote: Compressing objects: 100% (233/233), done.
    remote: Total 234 (delta 177), reused 0 (delta 0)
    Receiving objects: 100% (234/234), 53.20 KiB | 939.00 KiB/s, done.
    Resolving deltas: 100% (177/177), completed with 36 local objects.
    From git://anongit.freedesktop.org/mesa/drm
       cb592ac8166e..bcb9d976cd91  master     -> upstream/master
     * [new tag]                   libdrm-2.4.93 -> libdrm-2.4.93
     * [new tag]                   libdrm-2.4.94 -> libdrm-2.4.94

The idea here is that we by issuing a single short command can fetch the
latest master branch from the upstream repository of the codebase we're
working on and set our local master branch to point to the most recent
upstream/master one.

This works by looking for a remote called `upstream` (or falling back to
`origin` if it isn't found). And resetting the local master branch to point at
the upstream/master branch.


## ~/.gitconfig
Add this snippet under the `[alias]` section of your `~/.gitconfig` file.

    [alias]
        ru = "!f() { \
            REMOTES=$(git remote); \
            REMOTE=\"origin\"; \
            case \"$REMOTES\" in \
                *upstream*) \
                    REMOTE=\"upstream\"; \
                    ;; \
           	esac; \
            git fetch $REMOTE; \
            git update-ref refs/heads/master refs/remotes/$REMOTE/master; \
            git checkout master >/dev/null 2>&1; \
            git reset --hard $REMOTE/master >/dev/null 2>&1; \
            git checkout - >/dev/null 2>&1; \
        }; f

If you have a closer look, you'll notice that the `upstream` remote is used if
has been added, otherwise the `origin` remote is used. This selection is
done using git running a shell script.

## Example
This is what `git ru` might look like when used.

    robertfoss@xps9570 ~/work/libdrm $ git remote -v
    origin	git@gitlab.collabora.com:robertfoss/libdrm.git (fetch)
    origin	git@gitlab.collabora.com:robertfoss/libdrm.git (push)
    upstream	git://anongit.freedesktop.org/mesa/drm (fetch)
    upstream	git://anongit.freedesktop.org/mesa/drm (push)

    robertfoss@xps9570 ~/work/libdrm $ git log --pretty=log --abbrev-commit
    cb592ac8166e - (HEAD -> master, upstream/master, tag: libdrm-2.4.92) bump version for release (4 months ago) <Rob Clark>
    c5a656818492 - freedreno: add fd_pipe refcounting (4 months ago) <Rob Clark>
    1ac3ecde2f2c - intel: add support for ICL 11 (4 months ago) <Paulo Zanoni>
    bc9c789073c8 - amdgpu: Deinitialize vamgr_high{,_32} (4 months ago) <Michel Dänzer>
    [snip]

    robertfoss@xps9570 ~/work/libdrm $ git ru
    remote: Counting objects: 234, done.
    remote: Compressing objects: 100% (233/233), done.
    remote: Total 234 (delta 177), reused 0 (delta 0)
    Receiving objects: 100% (234/234), 53.20 KiB | 939.00 KiB/s, done.
    Resolving deltas: 100% (177/177), completed with 36 local objects.
    From git://anongit.freedesktop.org/mesa/drm
       cb592ac8166e..bcb9d976cd91  master     -> upstream/master
     * [new tag]                   libdrm-2.4.93 -> libdrm-2.4.93
     * [new tag]                   libdrm-2.4.94 -> libdrm-2.4.94

    robertfoss@xps9570 ~/work/libdrm $ git log --pretty=log --abbrev-commit
    cb9d976cd91 - (HEAD -> master, upstream/master) xf86drm: fallback to normal path when realpath fails (4 hours ago) <Emil Velikov>
    8389c5454804 - (tag: libdrm-2.4.94) Bump to version 2.4.94 (19 hours ago) <Kristian H. Kristensen>
    f0c642e8df41 - libdrm: add msm drm uapi header (25 hours ago) <Tanmay Shah>
    [snip]


## Thanks

This post has been a part of work undertaken by my employer [Collabora](http://www.collabora.com).

And thanks [@widawsky](https://twitter.com/widawsky) for pointing out some
improvements.

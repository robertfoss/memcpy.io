Title: Fixing .zsh_history corruption
Date: 2018-02-13 20:20
Category: linux
Status: draft
Tags: linux, shell, zsh, history, .zsh_history, corruption, fix, how, to, how-to
Description: .zsh_history getting corrupted happens far too often, and losing you shell history is actually quite painful. Here's how to fix it.

    zsh: corrupt history file /home/$USER/.zsh_history

Most zsh user will have seen the above line at one time or another.  
And it means that re-using your shell history is no longer possible.

Maybe some of it can be recovered, but more than likely some has been lost.
And even if nothing important has been lost, you probably don't want to spend any time dealing with this.

## Make zsh maintain a backup
Run this snippet in the terminal of your choice.

    cat <<EOT>> ~/.zshrc

    # Backup and restore ZSH history
    strings ~/.zsh_history | sed ':a;N;$!ba;s/\\\\\n//g' | sort | uniq -u > ~/.zsh_history.backup
    cat ~/.zsh_history ~/.zsh_history.backup | sed ':a;N;$!ba;s/\\\\\n//g'| sort | uniq > ~/.zsh_history

    EOT

### What does this actually do?
The snippet runs on every terminal open and copies your current .zsh_history into a backup file, creatively called .zsh_history.backup.  
The backup file is cleaned up and duplicated lines are removed.  
Lastly the backup is appended to your actual .zsh_history file.

## Conclusion
Hopefully this guide will have helped you avoid one of the more annoying aspects of zsh.

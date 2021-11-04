Title: Git Alias function syntax
Date: 2021-11-04 20:10
Category: linux
Tags: linux, shell, git, alias, b4, gitconfig, linux, mbox, am, kernel, mailing, list, mailinglists
Description: Git aliases are an easy way to customize commands, however it is tempting to be more expressive and use shell script functions. This is supported, but the syntax and escaping can be hard to overcome.

A basic example of the git alias function syntax looks like this.

    [alias]
    	shortcut = "!f() \
    	{\
    		echo Hello world!; \
    	}; f"

This syntax defines a function `f` and then calls it. These aliases are executed in a `sh` shell,
which means there's no access to Bash / Zsh specific functionality.

Every command is ended with a `;` and each line ended with a `\`. This is easy enough
to grok. But when we try to clean up the above snippet and add some quotes to
`"Hello world!"`, we hit this obtuse error message.

    }; f: 1: Syntax error: end of file unexpected (expecting "}")

This syntax error is caused by quotes needing to be escaped. The reason for this
comes down to how git tokenizes and executes these functions. If you're curious
about how it's managed internally, have a look at
[git/run-commands.c](https://git.kernel.org/pub/scm/git/git.git/tree/run-command.c?h=v2.31.0-rc1#n267).


[Tom Hale](https://gist.github.com/HaleTom) wrote this
[script](https://gist.github.com/HaleTom/61e2c94dc4d76b58c9f38fc8b6cec3ae)
for doing automatic escaping.

    quote() {
        printf %s "$1" | sed -r 's/(["\\])/\\\1/g';
    }

    IFS=$(printf '\n')
    printf '\n!"'
    read -r previous

    while read -r line; do
        quote "$previous"
        printf ' \\n\\\n'
        previous="$line"
    done

    quote "$previous"
    printf " #\"\n";

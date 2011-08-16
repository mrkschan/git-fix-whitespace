git-config core.whitespace has a list of whitespace problems. This project aims to maintain a set of script to resolve those whitespace problems one-by-one. This project also includes bash_completion script such that you can simply use `git fix-whitespace` with option prompt in bash.

Why not pre-commit hooks?  
Sometimes, you may intent to leave trailing space for any reason. For instance, markdown uses two trailing spaces for newline. Pre-commit hooks may not simply fit your needs sometimes. Anyway, the scripts in this project could also be used as pre-commit hooks as you wish.

Dependency:
- GitPython

# Error-Proneness of github Java repositories
> Update: its a sad sad satuation.....
 Recompiling Java repos on github with error-prone to analyse typical bugs
 
 The main idea was to clone repositories on github that use Java, and recompile the code using the error-prone plugin to find out what issues error prone catches in the real world.
 
 However, as it stands, the vast majority of projects are built using gradle and maven, and often each repository requires considerable manual effort in order to get it to compile at all. Simply running the build scripts often fails and so this process is hard to automate.
 
 As it stands, this repo contains some python scripts to automate the adding of error-prone to repositories, however given my difficulty in even getting projects to compile without any modification, I may give up on this.

> Update: Haven't given up yet
oh well, I will try again another day, having now compiled a large list of repositories to try and have managed to get a few to compile and even got error prone working on them, so finally seeing some results, with extra warnings being produced when error prone is used.

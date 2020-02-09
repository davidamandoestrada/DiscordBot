## Discord Bot
![](https://i.imgur.com/LIHO8e6.png)

### --- Maintainers --
- *Raul Lanuza*
- *David Estrada*

### --- Commands ---
+ !Playback: Will playback all messages from all users who have spoken in a channel that the bot is in.
![](https://i.imgur.com/mszo2bl.png "Playback example")

+ !Image: Will generate an avatar for the user who makes the command.
![](https://i.imgur.com/erXaZGQ.png "Image example")

## --- Features ---
+ Profanity and politics filter, will monitor a channel for profanity or politics.
![](https://i.imgur.com/CSJ2FEh.png "Making sure no one is profane!")

### --- How to Host Locally ---
1. Make sure you have Docker (https://www.docker.com/products/docker-desktop) installed locally. If you don't have it installed, install it.
2. Navigate to the directory to which you have cloned this repo.
3. Type 'docker-compose build'. This could take a while, as many of the layers of the images will have to be built.
4. Type 'docker-compose up'. This should take approximately 1 minute the first time you do it (the migration scripts will wait 1 minute before running).
5. Talk to Allied Mastercomputer! Every time you say something to it, it will store that message under your username. Type "!Playback" in chat to see what you, and others, have been typing.

### --- High Level Architecture ---
![](https://i.imgur.com/M2BN5ua.png "High-level Architecture")

### --- WIP ---
Make avatar image look better.

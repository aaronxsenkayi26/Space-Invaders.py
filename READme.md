# How to play:

> Move with the left and right arrow keys, A and D, or hold the on-screen LEFT and RIGHT buttons.

> Hold Space or the on-screen FIRE button to shoot.

> Press P or click the pause icon to pause. Press P or click the play icon to resume.

> Click the gear button or press G to open settings. Choose a background map, preview a music track, adjust the main and music volume, and set music on or off. Click SAVE ALL to apply the selected options together.

> Laser, achievement, game-over, and countdown sounds play during their matching game events. Settings pause gameplay and use the same 3-second resume countdown when closed.

> Click the gear button or press G to open audio settings. Choose one of three original chiptune tracks, adjust main and music volume independently, or switch music off and on.

> Laser, achievement, game-over, and countdown sounds play during their matching game events. Settings pause gameplay and use the same 3-second resume countdown when closed.

> Click CATALOG or press C to open the Jets, Blasters, Fire Rate, Bullet Amount, Bullet Colors, and Achievements catalogs. Reach the listed score thresholds to unlock gear, then click an unlocked item to equip it. Bullet Colors are all available from the start.

> Achievements unlock automatically when you reach their score goals, including "The Wide Receiver - Reach 1500 pts".

> Opening a catalog pauses the game. Click X or press Escape to close it; a 3-second countdown plays before the game resumes.

> Clear each alien wave to start the next, harder wave. The fleet moves and fires faster each wave, and an extra row joins every two waves up to seven rows. Aliens flap their limbs as the formation marches. Top-row aliens are worth 30 points, second-row aliens 20, and the other rows 10.

> You have three lives. Alien shots cost a life, and shields can absorb shots until they are worn away. If the invaders reach the bottom, the game ends.

> After game over, press R or click PLAY AGAIN to restart.

> Closing the game window opens an exit confirmation. Choose NO to return to the game or YES to exit; exiting loses this session's achievements and awards.

# Requirements (To run on the desktop version on file)

> Python Pygame ( If your PC doesn't have it, running the game will automatically install pygame for you.)

> A Windows, Linux, or Mac OS

# 2 ways to run Space Invaders:

 Command Prompt / Powershell:

> First, run this to install pygame: py -3.12 -m pip install pygame

> Second, run this to run the actual game: py -3.12 game.py

File Explorer or in Desktop:

> Double-click the file named run_game.bat & wait for Command Prompt to finish loading everything for you. If an error message pops up, follow its instructions, and if it tells you to download pygame, either run this in Command Prompt / Powershell: py -3.12 -m pip install pygame | or you can run the file amd64.exe file inside of the Backup Python 3.12.10 folder.

# Browser version

> Install Pygbag with Python 3.12: py -3.12 -m pip install pygbag

> From this folder, run: py -3.12 -m pygbag .

> Open http://localhost:8000 in a browser to play the game.

> To build browser files without starting the preview server, run: py -3.12 -m pygbag --build --PYBUILD 3.12 . The files are created in build/web.

# Automatic GitHub Pages deployment

> In the GitHub repository, open Settings > Pages and set the build and deployment source to GitHub Actions.

> The deploy-github-pages.yml workflow builds and deploys the browser game whenever code is pushed to main. It can also be run manually from the Actions tab.

> After the first successful deployment, play at https://aaronxsenkayi26.github.io/Space-Invaders.py/.

# 210,479 lines of code!
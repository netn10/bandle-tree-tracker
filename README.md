# bandle-tree-tracker
A Vanilla JS + Flask tracker for Legends of Runterra's The Bandle Tree win condition

## Instructions:
#### Setup
1. Create a virtual environment or install the packages globally (not recommended). Open a terminal in the directory and run the command `python -m venv .`. (If that doesn't work you might not have venv which can be installed with `sudo pip install virtualenv` on Unix/Linux or `pip install virtualenv` on Windows).
2. Enter the environment with `source myvenv/bin/activate` on Linux or `.\Scripts\activate` on Windows
3. Install the necessary packages with `pip install -r requirements.txt`
#### Usage
1. Open app.py with `python app.py`.
2. Enter "http://127.0.0.1:5000" in your favorite web browser.
3. Enter a game of Legends of Runterra. The client should be full screen in order to work. You should see the region's icons appear in the web page.
4. Every time you will play a follower, the icons will update!
5. Enjoy!

## Known bugs/issues:
1. Landmarks count as followers.
2. The app will work only on full screen because it calculates the distance between the player's hand and board.

## Disclaimer:
1. The project was build with free assets, all rights reserved to Riot Games. I am not affiliated with Riot Games in any shape or form.
2. This project is for educational proposes. I do not take responsibility for any harm done.
3. Any help would be appreciated!

import sys, time, random

tutorial = """Hello there! Welcome to the world of POKEMON!
This world is inhabited by creatures called POKEMON!
My name is OAK! People call me the POKEMON PROF!
For some people, POKEMON are pets
Others use them for fights.
Myself...
I study POKEMON as a profession.
But first, whats your name?
This is my grandson.
He's been your rival since you were a baby.
...Erm, what is his name again?
Your very own POKEMON legend is about to unfold!
A world of dreams and adventures with POKEMON awaits!
Let's go!"""

livingRoomDialog = """Right. All boys leave home one day
It said so on TV.
PROF OAK, next door is looking for you."""


randomMessages = [
    """Technology is incredible! 
    You can now store and recall items 
    and Pokemon as data via PC!""",
    """ Im rasing pokemon too!
    When they get strong they can protect me!""",
]


mysteriousPathDialog = """HEY WAIT, DON'T GO OUT 
Whew, That was close!
Wild pokemon live in tall grass"""


def slow_type(t):
    typing_speed = 500  # wpm
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / typing_speed)
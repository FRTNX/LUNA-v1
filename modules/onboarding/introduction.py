

class Introduction(object):

    def run(self):
        intro = """\nHere's how it is. You and I going to be partners on an adventure. It seems only
                   fair to inform you that there are things I dont have the time for. I dont want to put
                    ideas in your head so I'll let you discover them as you go. The things I will always make
                    time for are

                        * A normal everyday discussion.
                        * Informing you of the weather at your current or another location.
                        * Sharing whatever I can find on most subjects, from politics to physics and a little beyond.
                        * Giving you access to a ghost terminal where everything you type is between you and me.
                        * Showing you images of something.
                        * Showing you how to get to one location to another.
                        * Telling you where you are.
                        * Informing you on the meaning of a word.
                        * Translating any word to the language of your choice,
 
                   and a few more things that you will soon discover.

                   For a full menu and how to make special commands simply enter 'help' at any point 
                   on this journey.

                   Happy researching."""

        x = intro.split('\n')
        y = []
        for i in x:
            y.append(i.strip().replace('*', '    *'))
        z = '\n'.join(y)
        return z            

        
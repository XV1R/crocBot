
import os
import requests
import urllib.request
import sys, getopt

# artist = str(input("artist to parse?"))
# song = str(input("song to parse?"))
# url = "hhttps://www.azlyrics.com/lyrics/{}/{}.html".format(artist,song)
# response = requests.get(url)
INPUTFILE = 'index.html' 
OUTPUTFILE = 'lyrics.txt'



def load_data():
        try:
                fh = open(INPUTFILE)
        except:
                linesInFile = None
        else: # Only gets executed if no exception was raised
                linesInFile = fh.readlines()
                fh.close()
        return linesInFile



def write_results(lyricfile):
        outFH = open(OUTPUTFILE, 'w')
        for char in lyricfile:
                if char is '<':
                        char = '\n'
        outFH.write(lyricfile)


def main():

        listoflines = load_data()
        if listoflines is None:
                print('ERROR: Could not open {}!'.format(INPUTFILE))
                exit()

        parse = False;
        lyrics = ''
        for line in listoflines:
                if line.startswith('<!-- Usage of'):
                        parse = True;
                        continue
                if line.startswith('</div'):
                        parse = False
                        continue
                elif(parse):
                        line = line[0:line.find('<br>')]
                        lyrics += line + '\n'
                        print(line)
                       
                else:
                        continue
        write_results(lyrics)


if __name__ == '__main__':
	main()





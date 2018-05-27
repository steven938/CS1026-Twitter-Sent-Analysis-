# Tweet sentiment analysis by Steven Chen
# This program first processes a keywords text file by sorting the keywords into list based on their happiness score.
# Then, the program processes a tweet text file.

from happy_histogram import drawSimpleHistogram  # importing the function used to display smiley faces in the results at end of program
import requests
import time

try:
    keywordsFile = input("What is the name of the keywords file?")
    keywords = open(keywordsFile, "r", encoding="utf-8")
    score1 = []  # Creating blank list used to store the keywords based on their happiness score
    score5 = []
    score7 = []
    score10 = []
    listOfWords = keywords.readlines()  # turns the keywords text file into a list whereby each element in listOWords is a line in the keywords text file
    for line in listOfWords:
        line = line.split(",")  # separates the keyword from the score for each line
        if line[1].strip("\n") == "1":  # the if and elif statements determines which list the keywords belongs in based on score which is the second element of the line
            score1.append(line[0])  # appends the keywords to the list
        elif line[1].strip("\n") == "5":
            score5.append(line[0])
        elif line[1].strip("\n") == "7":
            score7.append(line[0])
        elif line[1].strip("\n") == "10":
            score10.append(line[0])
except IOError:  # if IOError occurs, the lines below execute
    print("Error: File does not exist.")
    exit(code=0)  # exits the program if IOError occurs


def calc():  # This function is used to process each tweet, assuming the tweet is in the form a list
    Score = 0  # initiating the score count for the tweet, the count of the tweet itself (1 if counted, 0 if not), and number of keywords
    Count = 0
    numOfKeywords = 0
    for i in range(len(
            tweet)):  # this nested for loop goes through each character in each element of the tweet list and if it's not alphabetic, the character is removed
        for char in tweet[i]:
            if not char.isalpha():
                tweet[i] = tweet[i].replace(char, "")
    for i in range(len(tweet)):  # this loop converts all remaining elements (containing alphabetical characters only) to lower case
        tweet[i] = tweet[i].lower()
    tweetCounted = False  # variable stores whether the tweet is counted - it is initially assumed that tweet isn't counted
    for i in range(len(tweet)):  # the following loop determines if elements in the tweet matches words in any of our keyword lists
        if tweet[i] in score1:
            Score = Score + 1  # the score of the keyword is added to the score counter
            numOfKeywords = numOfKeywords + 1  # keeps track of number of keywords in tweet
            tweetCounted = True  # if the element is a keyword, the tweet wil be counted
        elif tweet[i] in score5:
            Score = Score + 5
            numOfKeywords = numOfKeywords + 1
            tweetCounted = True
        elif tweet[i] in score7:
            Score = Score + 7
            numOfKeywords = numOfKeywords + 1
            tweetCounted = True
        elif tweet[i] in score10:
            Score = Score + 10
            numOfKeywords = numOfKeywords + 1
            tweetCounted = True
        else:
            if tweetCounted == True:  # ensures even if the current element in the iteration is not a keywords, the tweet is still counted if previous elements were keywords
                tweetCounted = True
            else:
                tweetCounted = False  # if no previous elements were keywords and the current element in the iteration is also not a keyword, the tweet is not counted
    if tweetCounted == True:  # if the tweet is counted (ie. tweet contains keywords), the count is 1 and the score of tweet is the raw score divided by number of keywords in the tweet
        Count = 1
        Score = Score / numOfKeywords
    return Score, Count  # returns a list: the score of the tweet and the count (1 if the tweet is counted, 0 if not)


def printResults():  # function used at the end to display results
    EasternScore = EasternTotal / EasternTweets  # formula for each region's score is the total score divided by total tweets
    CentralScore = CentralTotal / CentralTweets
    MountainScore = MountainTotal / MountainTweets
    PacificScore = PacificTotal / PacificTweets
    print("The happiness score of the Eastern time zone is", round(EasternScore, 3), "and the total number of tweets counted is", EasternTweets)
    print("The happiness score of the Central time zone is", round(CentralScore, 3), "and the total number of tweets counted is", CentralTweets)
    print("The happiness score of the Mountain time zone is", round(MountainScore, 3), "and the total number of tweets counted is", MountainTweets)
    print("The happiness score of the Pacific time zone is", round(PacificScore, 3), "and the total number of tweets counted is", PacificTweets)
    drawSimpleHistogram(EasternScore, CentralScore, MountainScore, PacificScore)  # calls the function that displays the emojis


try:
    tweetsFile = input("What is the name of the tweets file?")
    tweets = open(tweetsFile, "r", encoding="utf-8")
    listOfTweets = tweets.readlines()  # converts the tweet file into a list

    EasternTotal = 0  # initiating variables used to store number of total score count and number of tweets for each region
    CentralTotal = 0
    MountainTotal = 0
    PacificTotal = 0
    EasternTweets = 0
    CentralTweets = 0
    MountainTweets = 0
    PacificTweets = 0
    for tweet in listOfTweets:
        time.sleep(0.8)
        tweet = tweet.split()  # for each line which is a tweet in the list, it is split with the delimiter being the space
        # the the non-numerical characters attached the longitude and latitude are striped and tested to determine if it belongs in one of the timezones
        lat = (tweet[0].strip("[ ,"))
        lng = (tweet[1].strip("] ,"))
        url = "http://api.timezonedb.com/v2/get-time-zone?key=IV4FMOJBP3GD&format=json&by=position" + "&lat=" + lat + "&lng=" + lng
        resp = requests.get(url)
        dct = resp.json()
        zone = dct["abbreviation"]
        ID = zone[0]


        if ID == "E":
            tweetInfo = calc()  # stores the list returned from the calc function
            EasternTotal = EasternTotal + tweetInfo[
                0]  # The total score of the region is the current score plus the score from the tweet
            EasternTweets = EasternTweets + tweetInfo[
                1]  # The total tweets counted in the region is the current tweet count plus count of the tweet (1 if counted, 0 if not)
        elif ID == "C":
            tweetInfo = calc()
            CentralTotal = CentralTotal + tweetInfo[0]
            CentralTweets = CentralTweets + tweetInfo[1]
        elif ID == "M":
            tweetInfo = calc()
            MountainTotal = MountainTotal + tweetInfo[0]
            MountainTweets = MountainTweets + tweetInfo[1]
        elif ID == "P":
            tweetInfo = calc()
            PacificTotal = PacificTotal + tweetInfo[0]
            PacificTweets = PacificTweets + tweetInfo[1]
    printResults()
except IOError:
    print("Error: File does not exist")

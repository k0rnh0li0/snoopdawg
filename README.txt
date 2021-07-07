
    ======================================
    =====         SNOOP DAWG         =====
    =====       K0RNH0LI0 2021       =====
    =====                            =====
    =====  CATCH MOFUCKAS LACKIN!!!  =====
    ======================================


This script scans recent page(s) of the GitHub 
event stream for commits containing 
"interesting" regexes as specified in 
lists/patterns.txt.

Be sure to send a PR if you have any juicy
regexes to share.

File names/extensions can be excluded from
searching by adding them to blacklists.txt.

For additional help with usage, please see the
APPENDIX section.

SNOOPDAWG is Free Software, licensed under the
terms of the GNU GPLv2. See LICENSE.txt for
more information.


 === SETUP ===

1. Clone this repository.

2. Create a file called auth.priv that contains 
   your GitHub username on the first line and
   your OAuth token on the second line. And then
   don't commit it to version control ;)

   The OAuth token should have permission to read
   public repos.

3. Run ./snoopdawg.py

4. The script will scan the event stream for your
   regexes. Results for matches will be stored in
   results.json in the following format:

     {
       "<FILE HASH>": {
         "raw_url": "<URL>",
         "match": "<expression that matched>"
       },
       [...]
     }

   Files/diffs will be saved to downloads/, and
   will be named by their file hash.

   To not download files, and only create a
   results.json file, start the script with the
   flag: --no-dl

   By default, the script will only run one scan.
   To continue scanning until the script is
   interrupted, use the flag: --loop

5. Catch em lackin


 === APPENDIX ===

  A)
    IT'S THE BOW TO THE WOW
    CREEPIN AND CRAWLIN
    YIGGY YES YALLIN
    SNOOP DAWGGY DAWG IN
    THE MOTHAFUCKIN HOUSE

  B)
    IT'S A HACKER BAZAAR
    IT'S A MARKETPLACE FOR *.*
    EXPLOITS, VULNS, AND CARDS
    FULL DUMPS AND ACCOUNTS
    AND ARRAYS OF CHARS    

  C)
    CAUSE WHAT YOU SEE YOU MIGHT NOT GET
    AND WE CAN BET, SO DON'T YOU GET SOUPED YET
    SCHEMING ON A THING, THAT'S A MIRAGE
    I'M TRYNA TELL YOU NOW IT'S SABOTAGE

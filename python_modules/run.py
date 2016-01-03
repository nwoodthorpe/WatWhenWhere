'''
Takes multi-user schedule info (tokens) and returns open times for users to meetup when they don't have class
Blame iPage for this being done in py v2.5

Here is what a token looks like, there is one for each user: "TTh14301550&W10301120&MW16001720&"

TESTS, enter these commands in the cmd line in the WatWhenWhere/python_modules path:
python2.5 run.py "MWF830AM-920AM&F930AM-1020AM&TTh1000AM-1120AM&TTh230PM-350PM&MW1130AM-1220PM&F130PM-220PM&MWF230PM-320PM&W530PM-620PM" "F1030AM-1120AM&TTh830AM-950AM&MWThF230PM-320PM&MWF930AM-1020AM&Th1030AM-1120AM&MW100PM-220PM&F330PM-450PM&TTh1230PM-220PM" "F930AM-1020AM&TTh100PM-220PM&TTh1000AM-1120AM&MWF1130AM-1220PM&MWF1030AM-1120AM&W530PM-620PM&MW1230PM-220PM" "F930AM-1020AM&MWF1130AM-1220PM&TTh1130AM-1250PM&TTh100PM-220PM&F130PM-220PM&MWF830AM-920AM&MWF1030AM-1120AM&Th1030AM-1120AM"
python2.5 run.py "M1000AM-1100AM&M1200PM-200PM" "M1100AM-1200PM"
python2.5 run.py "TTh14301550&W10301120&MW16001720&MWF08300920&W09301020&MWF12301320&Th12301320&TTh10001120&F15301650&"

Sarth, Nat(23), Ed(20) test:
python2.5 run.py "TTh1000AM-1120AM&Th130PM-220PM&WF930AM-1020AM&T230PM-420PM&M130PM-420PM&MW830AM-920AM&W130PM-220PM&F130PM-420PM&MWF1030AM-1120AM&Th230PM-420PM&MTWF1230PM-120PM&T1130AM-1220PM" "W1630-1720&TTh1600-1720&TTh1000-1150&MWF1130-1220&MWF1430-1520" "TTh1130AM-1250PM&W130PM-220PM&TTh230PM-350PM&MWF1130AM-1220PM"
python2.5 run.py "TTh1000AM-1130AM&Th130PM-230PM&WF930AM-1030AM&T230PM-430PM&M130PM-430PM&MW830AM-930AM&W130PM-230PM&F130PM-430PM&MWF1030AM-1130AM&Th230PM-430PM&MTWF1230PM-130PM&T1130AM-1230PM" "W1630-1730&TTh1600-1730&TTh1000-1200&MWF1130-1230&MWF1430-1530" "TTh1130AM-100PM&W130PM-230PM&TTh230PM-400PM&MWF1130AM-1230PM"

'''

import cmdparser #Import the locally cloned argparse module (iPage doesn't have argparse so we needed to keep the argparse code locally)
import collision #Import the collision module created to do this processing

parser = cmdparser.ArgumentParser() #Create a parser object
parser.add_argument("tokens", nargs="+", help="enter apostrophe contained tokens deliminated by spaces") #Add a schedule tokens argument to the parser
args = parser.parse_args() #Parse argument strings to produce an args object containing the tokens in a list
print collision.collide(args.tokens) #Apply collision processing to the token list and print the result for the backend to read
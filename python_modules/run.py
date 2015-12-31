import argparse

parser = argparse.ArgumentParser()
parser.add_argument("tokens", nargs="+", help="enter non apostrophe contained tokens deliminated by spaces")
args = parser.parse_args()
print args.tokens
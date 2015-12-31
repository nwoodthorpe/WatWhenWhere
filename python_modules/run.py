import argparse
import collision

parser = argparse.ArgumentParser()
parser.add_argument("tokens", nargs="+", help="enter non apostrophe contained tokens deliminated by spaces")
args = parser.parse_args()
print collision.collide(args.tokens)
import puzzle
import sys, argparse
import cPickle as pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse a file with a list of words into a pickle file that can be later read by Trie')
    parser.add_argument('-i', '--input', help="Input text file", required=True)
    parser.add_argument('-o', '--output', help="Output pickle file", required=True)
    args = parser.parse_args()

    print "Creating Trie from", args.input
    trie = puzzle.Trie(args.input)
    print "Serializing to", args.output
    pickle.dump(trie.root, open(args.output, "wb"))
    print "Done"

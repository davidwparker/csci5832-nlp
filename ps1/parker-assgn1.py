import inspect

#TARGETS = "targets.txt"
#SOURCES = "sources.txt"
TARGETS = "2012testSet.txt"
#SOURCES = "NONE.txt"
SOURCES = "2012sourceSet.txt"
#COMPUTE_WER = False
COMPUTE_WER = True

#########################################
## Shared
#########################################
class Newfile(file):
    '''
    Allows for easy writing to a file with a newline
    '''
    def writeln(self,out):
        super(Newfile,self).write(out)
        self.write("\n")

def get_clean_corpus():
    '''
    Gets and cleans the corpus file
    '''
    fi = open("bigwordlist.txt","r")
    data = fi.readlines()
    fi.close()
    # clean up
    # strip newlines
    data = [item.rstrip('\n') for item in data]
    # split on frequencies for KV pairs (even though we don't use Frequencies)
    data = [item.split() for item in data]
    # trim to get first 75,000 entries
    data = data[:75000]
    # convert to dictionary
    return dict(data)

#########################################
# Part 1
#########################################
# Algorithms: max_match
def max_match(word, corpus):
    '''
    MaxMatch algorithm, as described on page 70 of the book.
    '''
    word = word.lstrip("#").lower() # remove the hash and lower case
    length = len(word) # how far to iterate
    start_i = 0 # starting index
    matched_words = [] # word array to return
 
    # loop while we still have an index that is less than our entire word length
    while start_i < length:
        match_found = False
        # start at full length, end of word and decrement by 1 until index is at 0
        for i in range(length, 0, -1):
            # check if word from starting (initially 0 to end of word) is in corpus
            if (word[start_i:i] in corpus):
                # append from where the starting index to current index is
                matched_words.append(word[start_i:i])
                # found a match, not a single character
                match_found = True
                # increment to new starting position
                start_i = i
                break
        # We don't have a match, increment our starting point and add single character
        if not match_found:
            matched_words.append(word[start_i])
            start_i += 1
    return matched_words

class part1:
    '''
    Part 1: Implement and explore the behavior of MaxMatch algorithm
    '''
    def __init__(self,out1,out):
        '''
        Initialize part 1 by setting up the word corpus and the hashtags
        '''
        self.final_out = out1
        self.out = out
        self.out.writeln("")
        self.out.writeln("------------")
        self.out.writeln(inspect.getdoc(self))

        # QUESTIONS:
        # Analyze MaxMatch behavior
        self.out.writeln("When it fails, what is the source of the failure?")
        self.out.writeln("  There are a few things that could cause the failure.")
        self.out.writeln("  1) There may be words in the dictionary (corpus) that shouldn't be there.")
        self.out.writeln("  2) There may be words that aren't in the dictionary (corpus) that should be.")
        self.out.writeln("  3) There may be compound words- that is words that can be broken into multiple pieces.")
        self.out.writeln("  4) There may be words that end in s d or r that may be able to be part of the previous word as well as the next word.")
        self.out.writeln("  5) Unicode is a problem (as well as other non-alphanumeric).")
        self.out.writeln("How many different kind of failures are there?")
        self.out.writeln("  There are probably an unlimited different kinds of failure, depending on the language used, the dictonary provided, and what the users want. For example, there are five very simple examples listed above.")

        # word corpus
        self.dct = get_clean_corpus()

        # word hashtags
        fi = open(TARGETS,"r")
        self.hashtags = fi.readlines()
        fi.close()
        # clean up - strip newlines
        self.hashtags = [item.rstrip('\n') for item in self.hashtags]

    def run(self):
        '''
        Runs MaxMatch algorithm for every hashtag provided in hashtags-dev.txt
        '''
        for word in self.hashtags:
            self.final_out.writeln(' '.join(max_match(word,self.dct)))

#########################################
# Part 2
#########################################
# Algorithms: MinimumEditDistance
def min_edit_dist(target, source):
    ''' 
    Computes the min edit distance from target to source. Figure 3.25 in the book. Assume that
    insertions, deletions and (actual) substitutions all cost 1 for this HW. Note the indexes are a
    little different from the text. There we are assuming the source and target indexing starts a 1.
    Here we are using 0-based indexing.
    '''
    n = len(target)
    m = len(source)
    distance = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + insert_cost(target[i-1])

    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + delete_cost(source[j-1])

    for i in range(1,n+1):
        for j in range(1,m+1):
            distance[i][j] = min(distance[i-1][j] + insert_cost(target[i-1]),
                                 distance[i][j-1] + insert_cost(source[j-1]),
                                 distance[i-1][j-1] + subst_cost(source[j-1],target[i-1]))
    return distance[n][m]

# Costs of insert, delete, and substitution
def insert_cost(arg):
    '''
    Insert is a fixed cost of 1
    '''
    return 1

def delete_cost(arg):
    '''
    Delete is a fixed cost of 1
    '''
    return 1

def subst_cost(arg1,arg2):
    '''
    Substitution is a fixed cost of 1 only if the args are different
    '''
    if arg1 != arg2:
        return 1
    else:
        return 0

def get_final_sources(sources):
    final_sources = []
    word_count = 0
    for source in sources:
        source_words = []
        words = source.split()
        for word in words:
            word_count += 1
            source_words.append(word.lower())
        final_sources.append(source_words)
    return final_sources, word_count
            
class part2():
    '''
    Part 2: Computing WER
    The first step in computing WER is to compute the minimum number of edits
    (deletions, insertions and substitutions) to get from the system's hypothesis to the actual correct reference answer.
    WER is then just the length normalized minimum edit distance 
    (i.e, minimum edit distance divided by the length of the reference in terms of words).
    '''
    def __init__(self,out,t,s):
        '''
        Initialize part2 by setting up the target and source files
        '''
        self.out = out
        self.out.writeln("")
        self.out.writeln("------------")
        self.out.writeln(inspect.getdoc(self))

        # word corpus
        self.dct = get_clean_corpus()

        # import targets and clean up newlines
        f = open(t,"r")
        self.targets = list([item.rstrip('\n') for item in f.readlines()])
        # import sources and clean up newlines
        f = open(s,"r")
        self.sources = list([item.rstrip('\n') for item in f.readlines()])
        f.close()

    def run(self):
        '''
        Computes WER
        '''
        # Get max_match lists from targets
        final_targets = []
        for target in self.targets:
            final_targets.append(max_match(target,self.dct))

        # Convert sources to lists
        final_sources, final_word_count = get_final_sources(self.sources)

        # Compute WER
        sources_count = len(final_sources)
        wer_total = 0
        min_edit_total = 0
        for target,source in zip(final_targets,final_sources):
            min_edit = min_edit_dist(target,source)
            wer = float(min_edit) / len(source)
            wer_total += wer
            min_edit_total += min_edit
        
        print "By averaged WERs =", wer_total/float(sources_count), wer_total, sources_count 
        print "By totalling WER =", min_edit_total/float(final_word_count), min_edit_total, final_word_count
        self.out.writeln("Calculated WER based on the input set using regular MaxMatch algorithm:")
        self.out.writeln(''.join(["By averaged WERs =", str(wer_total/float(sources_count)), str(wer_total), str(sources_count)]))
        self.out.writeln(''.join(["By totalling WER =", str(min_edit_total/float(final_word_count)), str(min_edit_total), str(final_word_count)]))

#########################################
# Part 3
#########################################
# Algorithms: modified_max_match, mini_max_match
def modified_max_match(word, corpus, rcorpus, longest):
    '''
    Modified Max Match algorithm.
    '''
    word = word.lstrip("#").lower() # remove the hash and lower case
    length = len(word) # how far to iterate
    all_matches = []

    # TODO: perform for both forward and backwards for the string
    #    for k in range(0,2):
    #        current_matches = []
    #        if k == 1:
    #            word = word[::-1]
    # loop while we still have an index that is less than our entire word length
    # O(n)*O(n^2) => O(n^3)
    for j in range(0,length):
        matched_words = []
        current_i = 0
        start_i = j
        # IMPROVEMENT #4
        # We now do the MaxMatch algorithm 2x
        # First one against words before the start, Second one against words after the start
        #        if k == 0:
        matched_words = mini_max_match(current_i,start_i,word,corpus,matched_words,longest)
        matched_words = mini_max_match(start_i,length,word,corpus,matched_words,longest)
        #            else:
        #                matched_words = mini_max_match(current_i,start_i,word,rcorpus,matched_words,longest)
        #                matched_words = mini_max_match(start_i,length,word,rcorpus,matched_words,longest)
        #                matched_words = [item[::-1] for item in matched_words[::-1]]

        # Only add them once
        if matched_words not in all_matches:
            all_matches.append(matched_words)
            #        if matched_words not in current_matches:
            #                current_matches.append(matched_words)

        # clean up current matches
        #        print matched_words

        #        if current_matches not in all_matches:
        #            all_matches.append(current_matches)

    return all_matches

# TODO: TRY REVERSING THE WORD
def mini_max_match(current, start, word, corpus, matched_words, longest):
    while current < start:
        match_found = False
        # start at full length, end of word and decrement by 1 until index is at 0
        for i in range(start, 0, -1):
            # check if word from starting (initially 0 to end of word) is in corpus
            # IMPROVEMENT #4 if the current one is a digit
            # IMPROVEMENT #5 only if word is shorter/equal to longest word in corpus

            if (((word[current:i] in corpus) or word[current:i].isdigit())
                and (len(word[current:i]) <= longest)):
                # append from where the starting index to current index is
                matched_words.append(word[current:i])
                # found a match, not a single character
                match_found = True
                # increment to new starting position
                current = i
                break
        # We don't have a match, increment our starting point and add single character
        if not match_found:
            matched_words.append(word[current])
            current += 1
                   
    return matched_words

def compare_matches(matches):
    '''
    Compares the matches of words returned by modified_max_match
    1) Finds the match with the fewest number of words. This means it has the longest length words (or several mid-length).
    2) Compares lengths of words, those with the longest words win.
    '''
    # first find the one with fewest number of words
    fewest_words = []
    min_length = len(min(matches,key=len))
    for words in matches:
        if len(words) == min_length:
            fewest_words.append(words)

    # only 1 element- return immediately
    if len(fewest_words) == 1:
        return fewest_words
    
    # next, if tie, then compare lengths of words
    longest_word = 0
    return_list = []
    for words in fewest_words:
        length = len(max(words,key=len))

        # new longest word
        if length > longest_word:
            longest_word = length
            return_list = []
            return_list.append(words)
        # there is a tie, add them both
        elif length == longest_word:
            return_list.append(words)

    return return_list

def compute(out,final_targets,final_sources,final_word_count):
    sources_count = len(final_sources)
    wer_total = 0
    min_edit_total = 0
    for target,source in zip(final_targets,final_sources):
        min_edit = min_edit_dist(target[0],source)
        wer = float(min_edit) / len(source)
        wer_total += wer
        min_edit_total += min_edit
#            self.final_out.writeln(''.join([str(target[0]), " => ", str(source), " = distance= ", str(min_edit)]))

    print "By averaged WERs =", wer_total/float(sources_count), wer_total, sources_count 
    print "By totalling WER =", min_edit_total/float(final_word_count), min_edit_total, final_word_count
    out.writeln("\nCalculated WER based on the input set using modified MaxMatch algorithm:")
    out.writeln(''.join(["By averaged WERs =", str(wer_total/float(sources_count)), str(wer_total), str(sources_count)]))
    out.writeln(''.join(["By totalling WER =", str(min_edit_total/float(final_word_count)), str(min_edit_total), str(final_word_count)]))

class part3():
    '''
    Part 3: Improving MaxMatch
    Tweak the original algorithm or alter the lexicon or both
    Limit yourself to considerations such as:
    (1) changing the MaxMatch strategy, 
    (2) changing the greedy nature of its heuristic, or 
    (3) manipulations to your lexicon.

    Improvements made:
    1) Manipulate Lexicon. Clean up the corpus by removing single character words.
    2) Manipulate Lexicon. Clean up two character words.
    3) Changing MaxMatch Strategy. Keep current max length word, then forward look 
       to see if we can build a longer one. If we can, then add rest as shorter words 
       or single characters
    4) Changing MaxMatch Strategy. Check to see if the string is a digit (positive numbers only)
    5) Changing MaxMatch Strategy. We know the longest length word in the corpus- don't
       search for something longer than that.
    6) Something to do with Unicode???

    '''
    def __init__(self,out1,out):
        '''
        Initialize part3 - get word corpus
        '''
        self.final_out = out1
        self.out = out
        self.out.writeln("")
        self.out.writeln("------------")
        self.out.writeln(inspect.getdoc(self))

        # word corpus
        self.dct = get_clean_corpus()

        # sources for WER)
        if COMPUTE_WER:
            f = open(SOURCES,"r")
            self.sources = list([item.rstrip('\n') for item in f.readlines()])
            f.close()

        # IMPROVEMENT #1 and 2
        newdata = []
        valid_two_chars = ["ab","ad","ah","an","as","at","ax","be","by","do","go","ha","he","hi",
                           "if","in","is","it","me","my","no","of","oh","on","or","ow","ox","pi",
                           "so","to","up","us","we"]
        for key in self.dct:
            # IMPROVEMENT #1: remove 1 char words
            if len(key) > 1:
                # IMPROVEMENT #2: only have valid two char words
                if len(key) == 2:
                    if key in valid_two_chars:
                        newdata.append([key,self.dct[key]])
                else:
                    newdata.append([key,self.dct[key]])

        # make a reverse direction copy of the corpus
        #        rnewdata = [[k[::-1],v] for k,v in newdata]
        # re-convert to dictionary
        self.dct = dict(newdata)
        self.rdct = dict(newdata) # change to rnewdata once figure that out

        # word hashtags
        fi = open(TARGETS,"r")
        self.hashtags = fi.readlines()
        fi.close()
        # clean up - strip newlines
        self.hashtags = [item.rstrip('\n') for item in self.hashtags]
        
    def run(self):
        '''
        Run improvements
        '''
        longest = len(max(self.dct,key=len))
        final_targets = []
        for word in self.hashtags:
            max_words = modified_max_match(word,self.dct,self.rdct,longest)
            #            print max_words
            max_word = compare_matches(max_words)
            #            max_word = compare_matches(max_words[0])
            final_targets.append(max_word)
            self.final_out.writeln(' '.join(max_word[0]))

        # Get the final sources
        if COMPUTE_WER:
            final_sources, final_word_count = get_final_sources(self.sources)
            # Compute WER
            compute(self.out,final_targets,final_sources,final_word_count)

def main():
    '''
    David Parker
    CSCI5832 - NLP
    Assignment 1: Deterministic English Segmentation
    September 16, 2012
    ------------------------------------------------
    '''
    out1 = Newfile("parker-out-assgn1-part1.txt","wb")
    out2 = Newfile("parker-out-assgn1-part3.txt","wb")
    out3 = Newfile("parker-desc-assgn1.txt","wb")
    out3.writeln(inspect.getdoc(main))
    p1 = part1(out1,out3)
    p1.run()
    if COMPUTE_WER:
        p2 = part2(out3,TARGETS,SOURCES)
        p2.run()
    p3 = part3(out2,out3)
    p3.run()
    out1.close()
    out2.close()
    out3.close()

if __name__ == '__main__':
    main()

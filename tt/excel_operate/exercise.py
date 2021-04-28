wordstring = """
Time teaches all things to him who lives forever but I have not the luxury of eternity. Yet within my allotted time I must practice the art of patience for nature acts never in haste. To create the olive, king of all trees, a hundred years is required. An onion plant is old in nine weeks. I have lived as an onion plant. It has not pleased me. Now I wouldst become the greatest of olive trees and, in truth, the greatest of salesman.
"""
wordstring = wordstring.replace('.','')
wordlist = wordstring.split()
wordseq = []
for i in wordlist:
    wordseq.append(wordlist.count(i))
d = zip(wordlist,wordseq)
print(d)
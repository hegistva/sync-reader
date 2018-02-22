
import nltk
from nltk.corpus import comtrans

nltk.data.path.append("/home/yourusername/whateverpath/")

algnsent = comtrans.aligned_sents()[54]

print(algnsent.words)
print(algnsent.mots)
print(algnsent.alignment)
# -*- coding: cp950 -*-
from conceptnet.models import *
from simplenlp import get_nl    #輸入自然語言處理工具
import os
import nltk                     #輸入自然語言處理工具

def parser(txt):
    # append the result into "output" and return it
    # then, remove the debug code in Step 8.
    output = []
    en_nl = get_nl('en')            # specify language
    #en = Language.get('en')         # specify language
    if os.name == 'nt':
        openfile = open('C:\\博士班一般\\06_課程\\0992_高等人工智慧\\07_ConceptNetTutorial\\in.txt', 'r')
    if os.name == 'posix':
        import sys
        sys.path.append('/home/chsiensu/.conceptnet/nltk-2.0.1rc1')
    #    openfile = open('/home/chsiensu/.conceptnet/intext.txt', 'r')
    
    #raw = openfile.read()
    # input text from the web-page
    raw = txt

    print '===>step 1: extract_concepts'
    concepts = en_nl.extract_concepts(raw, max_words=2, check_conceptnet=True)
    print concepts
    ##print concepts.pop([1])

    ##conceptList =[]
    ##for x in concepts:
    ####    print type(x)
    ##    conceptList.append(x[0:])
    ##print conceptList

    print '===>step 2: bigram collocation'
    baseForm, Residue = en_nl.lemma_split(raw)
    ##print baseForm              # reason  ve crave cobb salad lately...
    tokens = baseForm.split()
    ##print tokens                # [u'reason', u've', u'crave', u'cobb', u'salad',...]
    text = nltk.Text(tokens)
    ##print text                  # <Text: reason ve crave cobb salad...>
    labels = text.collocations()
    print labels

    print '===>step 3: bigram collocation2'
    from nltk.collocations import *
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    ##finder = BigramCollocationFinder.from_words(
    ##   nltk.corpus.genesis.words('C:\\博士班一般\\06_課程\\0992_高等人工智慧\\07_ConceptNetTutorial\\in.txt'))
    finder = BigramCollocationFinder.from_words(text)
    # only bigrams that appear 2+ times
    A = finder.apply_freq_filter(2)
    print A
    # return the 5 n-grams with the highest PMI(Pointwise mutual information)
    B = finder.nbest(bigram_measures.pmi, 5)  
    print B

    print '===>step 4: get Part-of-Speech tags'
    remainTags = ['FW','JJ','JJR','JJT','NN','NN$','NNP','NNS','NP','NP$','NPS','NPS$','NR','RB'
                  ,'RBR','RBT',]
    tokenizedRaw = nltk.word_tokenize(raw)
    posTag = nltk.pos_tag(tokenizedRaw)
    tags = []
    for tag in posTag:
        if tag[1] in remainTags:
            print tag[0],tag[1]
            tags.append(tag[0])
    print tags
        
    print '===>step 5: SVD + similarity'
    print '===>step 6: Category'
    import divisi2
    newCategory = divisi2.category(*tags)
    cnet= divisi2.network.conceptnet_matrix('en')
    newCategoryFeatures = divisi2.aligned_matrix_multiply(newCategory, cnet)
    # reconstruct similarity matrix U*Sigma2*UT
    concept_axes, axis_weights, feature_axes= cnet.svd(k=100)
    sim= divisi2.reconstruct_similarity(concept_axes, axis_weights, post_normalize=True)
    # find top 20 similar concepts to a category
    top20 = sim.left_category(newCategory).top_items(n=20)
    for x in top20:
        print x

    print '===>step 7: Frequency distribution'
    from nltk.book import *
    tokenizedRaw = nltk.word_tokenize(baseForm)
    fdist1 = FreqDist(tokenizedRaw)
    vocabulary1 = fdist1.keys()
    print vocabulary1

    print '===>step 8: Output file'
    output = ['keyword1','keyword2']
    print output
    return output


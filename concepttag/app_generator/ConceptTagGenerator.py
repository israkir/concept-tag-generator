# -*- coding: utf-8 -*-
from conceptnet.models import *         # import ConceptNet modules
from nltk.corpus import wordnet as wn   # import WordNet
from simplenlp import get_nl            # import natural language processing tools
import copy                             # for deepcopy
import divisi2                          # import divisi2
import nltk                             # import natural language toolkit(nltk)
import os                               # for confirming operating system name
import time                             # for calculate the execution time

def parser(txt):
    # append the result into "output" and return it
    # then, remove the debug code in Step 8.
    output = []
    en_nl = get_nl('en')            # specify language
    #en = Language.get('en')         # specify language

    # load articles from file
    #if os.name == 'nt':
    #    openfile = open('./in.txt', 'r')
    #if os.name == 'posix':
    #    import sys
    #    sys.path.append('/home/chsiensu/.conceptnet/nltk-2.0.1rc1')
    #    openfile = open('/home/chsiensu/.conceptnet/intext.txt', 'r')
    
    #raw = openfile.read()
    
    # input text from the web-page
    raw = txt

    '''
        raw: the original, unprocessed blog paragraph text
    '''
    tStart = time.time()
    '''
        record start time
    '''
    articleLengthCheck = 1
    print '\n===>step 1: extract_concepts'
    bigram = []
    concepts = en_nl.extract_concepts(raw, max_words=2, check_conceptnet=True)
    '''
        extract_concepts:
        Extract a list of the concepts that are directly present in text.
        max_words specifies the maximum number of words in the concept.
        If check_conceptnet is True, only concepts that are in ConceptNet for this
        language will be returned.
    '''
    if len(concepts) < 20:
        articleLengthCheck = 0
    if articleLengthCheck:
        print '=> concepts:'
        for x in concepts:
            print x
            if len(x.split()) == 2:
                bigram.append(x.split()[0]+ '_'+ x.split()[1])
                '''
                    Reform "ice cream" into "ice_cream" and push "ice_cream" onto bigram
                '''
        print '=> size(concepts):',len(concepts)
        print '\n=> bigram:'
        for x in bigram:
            print x
        print '=> size(bigram):',len(bigram)
    
        print '\n===>step 2: get Part-of-Speech(POS) tags'
        remainTags = ['NN','NNP','NNS']
        '''
            remainTags:
            Only remain tags that appear in
            ['NN','NNP','NNS']
            see Brown Corpus
            http://en.wikipedia.org/wiki/Brown_Corpus
            
            original version of remainTags:
            remainTags = ['FW','JJ','JJR','JJT','NN','NN$','NNP','NNS','NP','NP$',
            'NPS','NPS$','NR','RB','RBR','RBT']
        '''
        raw2 = en_nl.tokenize(raw)
        '''
            en_nl.tokenize(raw):
            Inserts spaces in such a way that it separates
            punctuation from words, splits up contractions
        '''
    
        tokenizedRaw = nltk.word_tokenize(raw2)
        '''
            word_tokenize:
            Tokenizers divide strings into lists of substrings
            word_tokenize divide strings into lists of words
        '''
    
        posTag = nltk.pos_tag(tokenizedRaw)
        '''
            nltk.pos_tag:
            Use NLTK's currently recommended part of speech tagger to
            tag the given list of tokens.
        '''
    
        tags = []
        count = 0
        tagDepth = 8
        print '=> (token, normalized token, tag):'
        for tag in posTag:
            '''
                posTag:
                (friends, NNS)
                (Parking, NNP)
                ...
            '''
            if tag[1] in remainTags and len(tag[0]) > 2:
                try:
                    wnTag = wn.synset(tag[0]+'.n.01')
                    if len(wnTag.hypernym_distances()) > tagDepth:
                        count += 1
                        stemmedTag = en_nl.word_split(tag[0])
                        print tag[0], stemmedTag[0].lower(), tag[1], len(wnTag.hypernym_distances())
                        tags.append(stemmedTag[0].lower())
                        '''
                            stemmedTag:
                            normalized tokens, for example,
                            friends -> friend
                            Parking -> park
                        '''
                except:
                    pass
        print '=> size((token, normalized token, tag)):', count
    
        print '\n===>step 3: intersecttion of ( POS tag && extract_concepts )'
        '''
            In step 3,
            1) keywords = intersection of sets from (Part-of-Speech tags) and
               (extract_concepts)
            2) Classify these keywords into categories with desired distribution 
               (the largest category should not contained almost all the
               keywords)
        '''
        intersectTags = [x for x in tags if x in concepts]
        for x in bigram:
            try:
                wn.synset(x+'.n.01')
                intersectTags.append(x)
                '''
                    append bigrams on intersectTags
                '''
            except:
                pass
        print '=> intersectTags:'
        for x in intersectTags:
            print x
        print '=> size(intersectTags):', len(intersectTags)
        intersectTagsCopy = intersectTags
        intersectTags = list(set(intersectTags))
        category = []
        for x in intersectTags:
            category.append([[x] * intersectTagsCopy.count(x)])
        i = 0
        for x in intersectTags:
            category[i] = category[i][0]
            i += 1
        '''
            category:
            The set that the occurrences of the keywords is remained.
            [['dog', 'dog', dog'],
             ['cat', 'cat']
             ...
            ]
            
            intersectTags:
            The set that the occurrences of the keywords is NOT remained.
            [['dog'],
             ['cat']
             ...
            ]
        '''
    
        iteration = 1
        threshold = 1.4
        categoryRatio = 1.0
        categoryCopy = copy.deepcopy(category)
        '''
            threshold:
            we started the threshold  from 1.4 (through trial and error) of the
            Leacock-Chodorow Similarity, two keywords that their similarity is
            below 1.4 is discarded. however, if the threshold is too low to
            appropriate classify the keywords, then we will increase threshold
            by 0.1 at next iteration.
            
            categoryRatio:
            After categorize keywords into n seperated categories c(1),c(2)...
            c(n), we calculate the ratio of the largest categories by c(1) /
            ( c(1) + c(2) + c(3) ), where c(1) is the largest category, c(2)
            is the 2nd largest category and c(3) is the 3rd largest category.
    
            If the ratio is above 0.8, that means there are too many keywords
            in c(1), so we should reduce the keywords in c(1) and increase
            keywords in c(2) and c(3) (through increase the threshold by 0.1)
            to make the top 3 largest categories more evenly distributed
    
            categoryCopy:
            For restoring the category at next iteration
            
        '''
        outerCount = 0
        innerCount = 0
        tagSimilarity = []
        for tag1 in intersectTags:
            outerCount +=1
            for tag2 in intersectTags[outerCount:]:
                try:
                    '''
                        Why use try?
                        Some words(ex: adj, adv) will incorrect classified into nouns
                        and cause an error here: (tag1+'.n.01') and (tag2+'.n.01')
                        can only deal with nouns.
                    '''
                    wnTag1 = wn.synset(tag1+'.n.01')
                    wnTag2 = wn.synset(tag2+'.n.01')
                    if wnTag1.lch_similarity(wnTag2) > threshold:
                        tagSimilarity.append([wnTag1.lch_similarity(wnTag2), tag1, tag2])
                        '''
                            lch_similarity:
                            Leacock-Chodorow Similarity, returns a score denoting how similar 
                            two word senses are, based on the shortest path that connects
                            the senses (as above) and the maximum depth of the taxonomy in
                            which the senses occur. The relationship is given as -log(p/2d)
                            where p is the shortest path length and d the taxonomy depth.
                        '''
                        innerCount +=1
                except:
                    pass
        while (categoryRatio > 0.8):
            category = copy.deepcopy(categoryCopy)
            tagSimilarity = [x for x in tagSimilarity if x[0] > threshold]
            sortedTagSimilarity = sorted(tagSimilarity, key=lambda tag: tag[0], reverse=True)
            print '\n=> sortedTagSimilarity:'
            for s in sortedTagSimilarity:
                '''
                    sortedTagSimilarity:
                    (           s[0]             ,s[1], s[2])
                    (similarity of tag1 and tag4 ,tag1, tag4) ## largest similarity
                    (similarity of tag3 and tag5 ,tag3, tag5) ## 2nd largest similarity 
                    ...
    
                    In this FOR loop, we:
                    1) Pop a set that contain s[1] from the 'categories'
                    2) Pop a set that contain s[2] from the 'categories'
                    3) Merge sets from 1) and 2) to make a bigger set, so
                       the cardinality of which is the sum of 1) and 2)
                    4) Push it back to 'categories'
                '''
                count = 0
                list1 = []
                for x in category:
                    if s[1] in x:
                        list1 = category.pop(count)
                        break
                    count += 1
                count = 0
                list2 = []
                for x in category:
                    if s[2] in x:
                        list2 = category.pop(count)
                        break
                    count += 1
                for x in list2:
                    list1.append(x)
                category.append(list1)
                print s
            print '=> size(sortedTagSimilarity):', len(sortedTagSimilarity)
            sortedCategory = []
            for a in category:
                sortedCategory.append([len(a),a])
            sortedCategory = sorted(sortedCategory, key=lambda tag: tag[0], reverse=True)
            categorySum = sortedCategory[0][0] + sortedCategory[1][0] + sortedCategory[2][0]
            categoryRatio = float(sortedCategory[0][0]) / categorySum
    
            print '\n=> category:'
            for x in category:
                print x
            print '=> number of category           : ', len(category)
            print '=> threshold                    : ', threshold
            print '=> size of largest category     : ', sortedCategory[0][0]
            print '=> size of 2nd largest category : ', sortedCategory[1][0]
            print '=> size of 3rd largest category : ', sortedCategory[2][0]
            print '=> categoryRatio                : ', categoryRatio
            print '=> End of iteration             : ', iteration
            print '=> ' * 10
            iteration += 1
            threshold += 0.1
    
    
        print '\n===>step 4: category prediction'
        '''
            Find similar concepts of top largest 3 categories:
            *sortedCategory[0][1] (at most 4 concepts)
            *sortedCategory[1][1] (at most 4 concepts)
            *sortedCategory[2][1] (at most 2 concepts)
    
            Uniformity is also concerned. For example, if one category is
            ['dog', 'dog', 'dog', 'dog', 'cat', 'cat', 'cat', 'cat'],
            then at most 2 concepts will extract from this category,
            even if it has 8 elements
            
        '''
        category0 = divisi2.category(*sortedCategory[0][1])
        category1 = divisi2.category(*sortedCategory[1][1])
        category2 = divisi2.category(*sortedCategory[2][1])
        cnet= divisi2.network.conceptnet_matrix('en')
        '''
            reconstruct similarity matrix U*(Sigma^2)*(U^T)
        '''
        concept_axes, axis_weights, feature_axes= cnet.svd(k=100)
        sim = divisi2.reconstruct_similarity(concept_axes, axis_weights, post_normalize=True)
        category0_top4 = sim.left_category(category0).top_items(n=4)
        category1_top4 = sim.left_category(category1).top_items(n=4)
        category2_top2 = sim.left_category(category2).top_items(n=2)
        outputTemp = []
        uniformity0 = len(set(sortedCategory[0][1]))
        uniformity1 = len(set(sortedCategory[1][1]))
        uniformity2 = len(set(sortedCategory[2][1]))
        print '=> category0:'
        for x in category0_top4[ : min(uniformity0 , 4)]:
            outputTemp.append(x)
            print x
        print '=> category1:'
        for x in category1_top4[ : min(uniformity1 , 4)]:
            outputTemp.append(x)
            print x
        print '=> category2:'
        for x in category2_top2[ : min(uniformity2 , 2)]:
            outputTemp.append(x)
            print x
    
        print '\n===>step 5: output file and calculate execution time'
        '''
            output = ['keyword1','keyword2',...]
        '''
        print '=> statistics     :'
        print '=> words count    : ', len(tokenizedRaw)
        print '=> # of concepts  : ', len(concepts)
        print '=> # of tags      : ', len(tags)
        print '=> # of category  : ', len(category)
        output = []
        print '\n=> output:'
        for x in outputTemp:
            print x[0]
            output.append(x[0])
        tStop = time.time()
        '''
            record stop time
        '''
        print '\n=> execution time: ',(tStop - tStart), 'secs'
    else:
        output = 'The article is too short for me to extract concept'
        print output
        output = []

    return output

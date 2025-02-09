import random
from itertools import combinations
U = [x for x in 'abcde']
pop = 10
freq = 0.4
sigma_threshold = int(freq*pop)
#Forgot to hash itemset support :(
itemset_support = {}

print(f"Script running with:\nDatabase size: {pop}\nSigma: {sigma_threshold}\n")

###HELPER FUNCTIONS FOR VISUAL AID###
def pretty_printer(iterable):
    #'pretty'
    if not iterable:
        print("NONE")
    for no_elem in range(len(iterable)):
        if type(iterable[no_elem]) == tuple:
            n_con, con, conf = iterable[no_elem]
            print(f"{n_con} -> {con}, with confidence {conf}")
        else:
            print(f"{no_elem+1}: {iterable[no_elem]}")
    print()
#####################################


###DEDICATED TO GENERATING TRANSACTION DATABASE AND FINDING FREQUENT ITEMSETS###
def gen_trans(U:set,n=pop):
    print("TRANSACTIONS")
    no_elem = len(U)
    transactions = []
    for _ in range(n):
        k_itemset = random.randint(1,no_elem)
        transactions.append(sorted(set(random.sample(U,k_itemset))))
    return transactions

trans = gen_trans(U)

def S_1(U:set,transactions:list,sigma=sigma_threshold):
    print("FREQUENT 1-ITEMSETS")
    s_1 = []
    for elem in U:
        elem_count = 0
        for trans in transactions:
            if elem in trans:
                elem_count += 1
        if elem_count>=sigma:
            itemset_support[str(list(elem))] = elem_count
            s_1.append(list(elem))
    return s_1

def S_2(s_1:list,transactions:list,sigma=sigma_threshold):
    print("FREQUENT 2-ITEMSETS")
    s_2 = []
    combs = combinations(s_1,2)
    for i_set in combs:
        as_set = set(i_set)
        set_count = 0
        for trans in transactions:
            if as_set.issubset(set(trans)):
                set_count += 1
        if set_count>=sigma:
            itemset_support[str(list(i_set))] = set_count
            s_2.append(list(i_set))
    return s_2

def gen_from_cand(s:list,n:int):
    cand_n = []
    for prim in range(len(s)-1):
        cand1 = s[prim]
        for sec in range(prim+1,len(s)):
            cand2 = s[sec]
            if cand1[:-1] == cand2[:-1]:
                cand3 = cand1[:n-2]+list(cand1[-1])+list(cand2[-1])
                combs = combinations(cand1[:-1],len(cand1)-2)
                filtering = [list(comb)+list(cand1[-1])+list(cand2[-1]) for comb in combs]
                checking = [True if cand in s else False for cand in filtering]
                if not (False in checking):
                    cand_n.append(cand3)
            else:
                break
    return cand_n

def check_if_freq(transactions:list,candidates:list,sigma=sigma_threshold):
    print(f"FREQUENT {len(candidates[0])}-ITEMSETS")
    frequent = []
    for i_set in candidates:
        as_set = set(i_set)
        set_count = 0
        for trans in transactions:
            if as_set.issubset(set(trans)):
                set_count += 1
        if set_count>=sigma:
            itemset_support[str(list(i_set))] = set_count
            frequent.append(list(i_set))
    pretty_printer(frequent)
    return frequent

def freq_itemsets(U:set,transactions:list,sigma=sigma_threshold):
    pretty_printer(transactions)
    s_1 = S_1(U,transactions,sigma)
    pretty_printer(s_1)
    s_2 = S_2(U,transactions,sigma)
    pretty_printer(s_2)
    if len(s_2)<=3:
        return s_1+s_2
    freq_items = s_1+s_2
    n = 3
    cand = gen_from_cand(s_2,3)
    while cand:
        s_n = check_if_freq(transactions,cand)
        freq_items = freq_items+s_n
        n += 1
        cand = gen_from_cand(s_n,n)
    return freq_items

################################################################################
def find_confidence(n_cons:list,cons:list):
    return itemset_support[str(sorted(n_cons))]/itemset_support[str(cons)]

def third(t:tuple):
    x,y,z = t
    return z

def find_assc_rules(F:list,U:list,c:float):
    ass_rules = []
    sorted_F = sorted(F,key=len,reverse=True)
    for itemset1 in sorted_F:
        as_set = set(itemset1)
        for itemset2 in F:
            if itemset1 != itemset2 and set(itemset2).issubset(as_set):
                conf = find_confidence(itemset1,itemset2)
                if conf > c:
                    ass_rules.append((itemset2,itemset1,conf))
                else:
                    for itemset in sorted_F:
                        if set(itemset).issubset(itemset1):
                            sorted_F.remove(itemset)
                    break
    return ass_rules  

c = 0.6
F = freq_itemsets(U,trans)
assc_rules = find_assc_rules(F,U,c)
assc_rules.sort(key=third,reverse=True)

print(f"ASSOCIATION RULES WITH CONFIDENCE ABOVE {c}:")
pretty_printer(assc_rules)

#Target strings:
#"n(paq)", "n(poq)", "piq"
#n: not, a: and, o: or, b: bi-implication, i: implication, ^:xor
from itertools import product

#Auxiliary functions to be called when evaluating.
def And(p:bool,q:bool):
    return p and q

def Or(p:bool,q:bool):
    return p or q

def Not(p:bool):
    return not p

def XOR(p:bool,q:bool):
    return p ^ q

def Imply(p:bool,q:bool): #p->q
    return (not p or q)

def Bi_Imply(p:bool,q:bool): #p<->q
    return ((not p or q) and (not q or p))

log_symbols = ['n','o','a','b','i','^']
symb_func = {'n':Not,'o':Or,'a':And,'b':Bi_Imply,'i':Imply,'^':XOR}

#Puts all the variables in a dictionary.
def var_to_dic(log_exp:str)->dict:
    variables = {}
    for char in log_exp:
        if char in log_symbols or char in "()":
            pass
        else:
            variables[char] = True
    return variables

#Stores all different combinations of truth values for the
#variables in a list.
def truth_combs(length:int)->list:
    perms = [list(pair) for pair in product([True,False], repeat=length)]
    return perms

#Sets new truth value to each variable.
def init_dic(dic:dict,truth:list)->dict:
    counter = 0
    new_dic = {key:True for key in dic}
    for key in new_dic:
        new_dic[key] = truth[counter]
        counter += 1
    return new_dic

#Determines the max depth to determine priority in evaluation order
#and what operation accompanied by its location in the expression.
def prior_op_ind(exp_list:list)->int:
    def fst(tup:tuple)->int:
        return tup[0]
    Max = 0
    cur = 0
    ind = 0
    attr = []
    for char in exp_list:
        if char == "(":
            cur += 1
            if Max < cur:
                Max = cur
        elif char == ")":
            cur -= 1
        elif char in log_symbols and char != "n":
            attr.append((cur,char,ind))
        ind += 1
    attr.sort(reverse=True,key=fst)
    return attr[0] if attr else None

#Removes filter tags and reverts bools with not in front of them.
def filter_and_not(exp_list:list,dic:dict)->list:
    for ind in range(len(exp_list)):
        char = exp_list[ind]
        if char == "n" and (exp_list[ind+1] in dic or type(exp_list[ind+1])==bool):
            exp_list[ind+1] = not exp_list[ind+1]
            exp_list[ind] = "F"
    return [c for c in exp_list if c != "F"]

#Substitute the variables with the truth values.
def substitute_vals(exp_list:list,dic:dict)->list:
    for ind in range(len(exp_list)):
        if exp_list[ind] in dic:
            t_val = dic[exp_list[ind]]
            exp_list[ind] = t_val
    new_list = filter_and_not(exp_list,dic)
    return new_list

#Evaluates simple expression based on location and operator.
def evaluate(exp_list:list,attr:tuple,dic:dict):
    prior, op, ind = attr
    operation = symb_func[op]
    left, right = exp_list[ind-1], exp_list[ind+1]
    if ind > 1 and exp_list[ind-2] == "(":
        exp_list[ind-2] = "F"
    if ind < len(exp_list)-2 and exp_list[ind+2] == ")":
        exp_list[ind+2] = "F"
    new_t_val = operation(left,right)
    exp_list[ind] = new_t_val
    exp_list[ind-1], exp_list[ind+1] = "F", "F"
    return filter_and_not(exp_list,dic)

#Evaluates the whole expression and returns the truth
#value.
def evaluator(exp:str,truths:list):
    dic = var_to_dic(exp)
    for truth in truths:
        new_dic = init_dic(dic,truth)
        ret_list = substitute_vals(list(exp),new_dic)
        while len(ret_list)>1:
            attr = prior_op_ind(ret_list)
            if attr != None:
                ret_list = evaluate(ret_list,attr,new_dic)
            else:
                ret_list = filter_and_not(ret_list,new_dic)
        print(f"{exp} is {ret_list[0]} when,")
        for key in new_dic:
                print(f"{key}:{new_dic[key]}")

#Evaluates if the two logical expressions are the same.
def comparer(exp1:str,exp2:str)->bool:
    dic = var_to_dic(exp1)
    truths = truth_combs(len(dic))
    for truth in truths:
        new_dic = init_dic(dic,truth)
        ret_list1 = substitute_vals(list(exp1),new_dic)
        ret_list2 = substitute_vals(list(exp2),new_dic)
        while len(ret_list1)>1:
            attr1 = prior_op_ind(ret_list1)
            if attr1 != None:
                ret_list1 = evaluate(ret_list1,attr1,new_dic)
            else:
                ret_list1 = filter_and_not(ret_list1,new_dic)
        while len(ret_list2)>1:
            attr2 = prior_op_ind(ret_list2)
            if attr2 != None:
                ret_list2 = evaluate(ret_list2,attr2,new_dic)
            else:
                ret_list2 = filter_and_not(ret_list2,new_dic)
        if ret_list2[0] != ret_list1[0]:
            return False
    return True

target = "npaq" #(not p) AND q
variable = "n(piq)" #not (p -> q)

print(comparer(target,variable)) #The two expressions are the same, returns true.
print()
evaluator("paq",truth_combs(2))


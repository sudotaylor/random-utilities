# buildDelegateLists.py
#   Inputs:
#       Two .csv files:
#           input_relationships = [employeeID,supervisorID]
#           input_linkedusers = [employeeID,employeeUserAlias]
#               (note: 'employeeUserAlias' above may be an email address or some other alternate ID unique to employee)
#       top_positions = (a list of employeeIDs corresponding to the top(s) of the hierarchies)
#   Output:
#       output_file = [employeeUserAlias,chainOfCommandUserAliases]
#           (chainOfCommandUserAliases is a ';'-delimited list of employeeUserAliases up to one of the top_positions)

import csv

# Change these as necessary:
input_relationships: str = "position_relationships.csv"
input_linkedusers: str = "position_linkedusers.csv"
output_file: str = "delegateList.csv"
top_positions: list[str] = ["1001", "1002"]
directorID = "1001"
deputyID = "1002"


data = csv.reader(open(input_relationships, 'r'))
data.__next__() # remove header
position_relationships: dict[str,str] = dict(data)

data = csv.reader(open(input_linkedusers, 'r'))
data.__next__() # remove header
position_linkedusers: dict[str,str] = dict(data)

# these could be used to potentially improve readability below if desired
#directorAlias: str = position_linkedusers[directorID]
#deputyAlias: str = position_linkedusers[deputyID]

# Checks all records with linked users by deafult - set this to some other list instead, if desired
positions: list[str] = position_linkedusers.keys()
#positions: list[str] = list()

output_content: list[str] = []

for p in positions:
    # Add user themself (as employeeUserAlias)
    list_tree:list[str] = [position_linkedusers[p] if (p in position_linkedusers) else ""]
    # Add user themself (as original employeeID, not employeeUserAlias)
    #list_tree:list[str] = [position_linkedusers[p] if (p in position_linkedusers) else ""]
    while p not in top_positions:
        try:
            p: str = position_relationships[p]
            list_tree.append(position_linkedusers[p] if (p in position_linkedusers) else "")
        except:
            #list_tree.append(None) # can change this to add an error message in the actual output, but adjust deputy/director section below to handle error message properly if so
            print("ERROR ('" + p + "') - DID NOT REACH A TOP POSITION (GAP FOUND IN HIERARCHY)")
            break
    # Case of single or multiple-independent chain(s) of command:
    #output_content.append([list_tree[0], ';'.join(list_tree[1:])])
    # Case of single chain of command with leader + deputy:
        # (add conditional to handle error message if added above)
        # (currently will add deputy and director even if hierarchy is broken, but not if the hierarchy is completely empty - change if needed)
    if len(list_tree)>1:
        if (list_tree[-1] == position_linkedusers[deputyID]):
            list_tree.append(position_linkedusers[directorID])
    else:
        # (may want to print a message, or output some indication other than a blank field -- if so, do that here)
        pass
    if len(list_tree)>2:
        if (list_tree[-1] == position_linkedusers[directorID]):
            if (list_tree[-2] != position_linkedusers[deputyID]):
                list_tree.insert(-1, position_linkedusers[deputyID])
        else:
            list_tree.append(position_linkedusers[deputyID])
            list_tree.append(position_linkedusers[directorID])
    

    output_content.append([list_tree[0], ';'.join(list_tree[1:])])

writer = csv.writer(open(output_file, 'w'))
writer.writerows(output_content)

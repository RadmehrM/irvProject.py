# Instant Runoff Vote program
# Program takes input of a csv file which contains different vote ballots. (each row is a voting ballot)
# Based on the ranking of each candidate on each ballot the program declares a winner.


def voteFunction(fileName):
    """
    This function takes in a file and returns list of lists of voters votes for candidates.
    :param fileName: any csv file
    :return: a list that contains many lists each representing the vote of one voter.
    """
    voterList = []
    for line in fileName:
        line = line.replace('\n', '')  # takes out all the new lines characters and replaces them with nothing.
        line = line.split(',')
        while '' in line:
            line.remove('')
        line = [int(numbers) for numbers in line]  # turns each string number into an integers.
        voterList.append(line)

    return voterList


def voteDict(voterList):
    """
    This function takes in a list of lists of votes and returns a dictionary of voterID as keys and
    percentage votes as values.
    :param voterList: List of lists of voters votes for candidates.
    :return: a dictionary that shows the percentage of first place votes for each candidate.
    """
    candidates = dict()

    for numberList in voterList:
        if int(numberList[0]) not in candidates:
            candidates[int(numberList[0])] = 1
        # if the first number in the list (which is the most preffered candidate) is not in the dictionary,
        # then a key is added to that dictionary with the value 1
        elif int(numberList[0]) in candidates:
            candidates[int(numberList[0])] += 1
        # if the first candidate exists in the dictionary the key corresponding to the candidate increases by 1.

    s = sum(candidates.values())
    for keys, values in candidates.items():
        candidates[keys] = (values / s) * 100
    # Turns the values in the dictionary into percentages.

    return candidates


def elimination(candidates):
    """
    This function takes in a dictionary of candidates and returns the candidate with the lowest votes and if more than
    two candidates have the lowest, the one with the highest ID is returned.
    :param candidates: dictionary with each value being the percentage of first place votes for each candidate.
    :return: The candidate ID with the lowest votes.
    """
    if max(candidates.values()) < 50:
        minVal = 49
        for k, v in sorted(candidates.items()):  # Sorting the items of the dictionary will allow for the candidate with
            # highest ID be eliminated first if there are more than one candidates with the lowest amount of votes.
            if v <= minVal:
                minVal = v
                eliminatedCandidate = []
                eliminatedCandidate.append(k)
                eliminatedCandidate.sort(reverse=True)  # Sorts the candidates from highest ID to lowest.




    elif max(candidates.values()) >= 50 and max(candidates.values()) < 100:
        eliminatedCandidate = []
        for k, v in candidates.items():
            if v < 50:
                eliminatedCandidate.append(k)
            elif all(v == 50.0 for v in
                     candidates.values()):  # this means that if all the values in the dictionary are 50
                eliminatedCandidate.append(k)
                eliminatedCandidate.sort(reverse=True)


    elif max(candidates.values()) == 100.0:
        eliminatedCandidate = []
        for k, v in candidates.items():
            if v == 100.0:
                eliminatedCandidate.append(k)

    return eliminatedCandidate


def updateVote(VoteList):
    """
    This fucntion takes a list of voterLists and removes all the votes for the candidate with the lowest votes.
    :param VoteList: list of voterList
    :return: list of voterList excluding the candidate with the lowest votes.
    """
    eliminatedVote = elimination(voteDict(VoteList))

    for numberList in VoteList:
        for number in eliminatedVote:
            if number in numberList:
                numberList.remove(number)
            # if the candidateID with the lowest votes is in the ballet of any voter, remove the vote from the
            # voters ballet

    for numberList in VoteList:
        while '' in numberList:
            numberList.remove('')

    while [] in VoteList:
        VoteList.remove([])  # removes any empty voterList in the main list.

    return VoteList


def elimOrder(voteList):
    """
    This function takes a list of voter ballet and returns a list of eliminated candidates in the order that they
    were eliminated from.
    :param voteList: list of voter ballet
    :return: list of eliminated candidates in order.
    """
    elimList = []
    while len(voteList) != 0:
        voteDiction = voteDict(voteList)
        elimNum = elimination(voteDiction)
        elimList.append(elimNum)
        voteList = updateVote(voteList)

    elimOrder = []
    for numberList in elimList:
        for number in numberList:
            if number not in elimOrder:
                elimOrder.append(number)
                # avoids any repitiion in the list.
    if ' ' in elimOrder:
        elimOrder.remove(' ')
        # avoids any empty values from appearing in the list.

    return elimOrder


def main():
    fileInpName = input('Enter the name of the file: ')
    fileHandle = open(fileInpName, 'r',
                      encoding='utf-8-sig')  # utf-8-sig prevented from any unnecessary characters from
    # appearing from the file

    round1 = voteFunction(fileHandle)
    # print(voteDict(round1))
    elimOrd = elimOrder(round1)
    strElimOrder = [str(ltr) for ltr in elimOrd]  # takes each number from the list that turns them into a string.
    round1str = ', '.join(strElimOrder)  # joins the list of numbers into a string.
    print('Elimination order: {}'.format(round1str))
    print(f"candidate {strElimOrder[-1]} is the winner!!")


main()

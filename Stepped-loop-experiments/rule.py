import numpy as np


class Rule():
    def __init__(self, input_pattern, output_pattern, state, deterministic=False, symmetry="12345678", rtype="one", density=None):

        # store rule shape
        self.m, self.n = np.array([list(row) for row in input_pattern.split("/")]).shape

        # define input and output strings
        self.input = input_pattern.replace("/", "")
        self.output = output_pattern.replace("/", "")

        # store size of grid
        self.i, self.j = state['grid'].shape

        # deterministic or random match selections
        self.deterministic = deterministic

        # density function
        self.density = density

        # field: log-weight over grid according to density function
        self.field = np.zeros((self.i, self.j))

        # symmetries of input allowed
        self.symmetry = symmetry

        # rule type
        self.rtype = rtype

    def compute_field(self, state):
        pass

    def neighbour_indices(self, i, j):
        '''
        Compute the list of indices of m x n grid with corner (i, j) for all 8
        symmetries, with ordering row by row with respect to original orientation

        Symmetries are labelled in clockwise order, starting with the original
        orientation with top-left corner of rule in (i, j)
        '''
        # original
        symm_1 = [(i + p, j + q) for p in range(self.m) for q in range(self.n)]
        # reflection in y = -x
        symm_2 = [(i + p, j + q) for q in range(self.m) for p in range(self.n)]
        # 90 deg. clockwise
        symm_3 = [(i + p, j - q) for q in range(self.m) for p in range(self.n)]
        # ref. in y-axis
        symm_4 = [(i + p, j - q) for p in range(self.m) for q in range(self.n)]
        # ref. in x and y axes
        symm_5 = [(i - p, j - q) for p in range(self.m) for q in range(self.n)]
        # reflection in y = x
        symm_6 = [(i - p, j - q) for q in range(self.m) for p in range(self.n)]
        # 90 def. anti-clockwise
        symm_7 = [(i - p, j + q) for q in range(self.m) for p in range(self.n)]
        # ref. in x-axis
        symm_8 = [(i - p, j + q) for p in range(self.m) for q in range(self.n)]

        # possible options
        options = [symm_1, symm_2, symm_3, symm_4, symm_5, symm_6, symm_7, symm_8]

        # select according to numbers in self.symmetry
        selected = []
        for num in list(self.symmetry):

            # select
            choice = options[int(num) - 1]

            # check if in bounds of grid
            valid = True
            for x, y in choice:
                if (x < 0) or (y < 0) or (x >= self.i) or (y >= self.j):
                    valid = False
                    break

            # if valid: add to selection
            if valid:
                selected.append(choice)

        return selected

    def match_distribution(self, matches):
        '''
        Given a list of "matches" (each a list of indices in the grid) compute a
        normalised distribution over them

        Probabilities are sums over those of each index in the match, which are
        given by the "field" (log-weights) computed by the rule's "distribution
        function" applied to the current grid state
        '''
        # helper function for log-weight computation
        def logsumexp(v):
            v_max = np.max(v)
            return np.log(np.sum(np.exp(v - v_max))) + v_max

        # find log-weights of each match
        match_weights = []
        for match in matches:

            # log-weights of indices in match
            index_log_weights = np.array([self.field[idx] for idx in match])

            # combine to overall log-weight of match
            match_weight = logsumexp(index_log_weights)

            match_weights.append(match_weight)

        # normalised distribtion from log-weights over matches
        match_weights = np.array(match_weights)
        w_max = np.max(match_weights)
        dist = np.exp(match_weights - w_max) / np.sum(np.exp(match_weights - w_max))

        return dist

    def find_matches(self, state):
        '''
        Search for all matching instances of the rule input in the grid,
        return a list containing list of indices for each match
        '''
        # list containing lists of indices for each match
        matches = []

        # select indices with letters matching the top-left letter of rule input
        initial_letter = self.input[0]
        if initial_letter == '*':
            # select all indices if * character used
            indices = [(i, j) for i in range(self.i) for j in range(self.j)]
        else:
            indices = state['dict'][initial_letter]

        # 1 letter rule: end
        if len(self.input) == 1:
            # change each index to list for consistency
            indices = [[idx] for idx in indices]
            return indices

        # otherwise: examine each selected index
        for idx in indices:

            # get neighbouring index lists (using symmetry conditions)
            neighbouring_indices = self.neighbour_indices(*idx)

            # examine each neighbour
            for nb_idx in neighbouring_indices:

                # check if all indices match rule
                matching_flag = True
                for k, (i, j) in enumerate(nb_idx):
                    if not ((state['grid'][i, j] == self.input[k]) or (self.input[k] == '*')):
                        matching_flag = False
                        break
                
                # valid matching: add to list
                if matching_flag:
                    matches.append(nb_idx)

        return matches

    def replace(self, state, matches):
        '''
        Given a list of matches, choose those to replace according to rule type

        "one": choose a single match
        "all": choose "maximal" set of non-conflicting matches
        "prl": choose all matches regardless of overlap (parallel)

        Return list of all indices that were changed
        '''

        # random generator
        rng = np.random.default_rng()

        # update field
        self.compute_field(state)

        # compute probability distribution over matches
        p = self.match_distribution(matches)

        # chosen matches
        matches_chosen = []

        # changed indices
        changed_indices = []

        # one: choose a single match
        if self.rtype == "one":

            # deterministic: most probable match
            if self.deterministic:
                k = np.argmax(p)

            # random: sample once from match distribution
            else:
                k = rng.choice(len(matches), p=p)
            
            matches_chosen.append(matches[k])

        # all: choose "maximal" set of non-conflicting matches
        elif self.rtype == "all":
            
            # while matches remaining
            while matches:

                # re-normalise distribution
                p = p / np.sum(p)

                # choose from remaining matches (sample / take most probable)
                if self.deterministic:
                    k = np.argmax(p)
                else:
                    k = rng.choice(len(matches), p=p)

                # test for conflicts with previously chosen matches
                valid = True
                for chosen in matches_chosen:

                    # common index in previously chosen match and current match
                    if set(chosen) & set(matches[k]):
                        valid = False
                        break

                # no conflicts: add to list of chosen matches
                if valid:
                    matches_chosen.append(matches[k])

                # remove match (regardless of validity)
                matches.pop(k)
                p = np.delete(p, k)

        # prl: choose all matches in "parallel"
        elif self.rtype == "prl":
            
            # sort matches by increasing probability: higher probability matches will overwrite lower (painters algorithm)
            '''may be wrong order'''
            sorted_indices = p.argsort() 
            for k in sorted_indices:
                matches_chosen.append(matches[k])

        # for each chosen match, apply rule
        for match_indices in matches_chosen:

            # for each index in match
            for k, (i, j) in enumerate(match_indices):

                # if not special character
                if not (self.output[k] == '*'):

                    # get old letter
                    old_letter = state['grid'][i, j]

                    # update grid to new letter
                    state['grid'][i, j] = self.output[k]

                    # update dict
                    state['dict'][old_letter].remove((i, j))
                    state['dict'][self.output[k]].append((i, j))

                    # add index to list of changes
                    changed_indices.append((i, j))

        return changed_indices

    def run(self, state):
        
        # find matches of the rule input in the current state
        matches = self.find_matches(state)

        # if at least one match is found
        if matches:

            # replace matches according to rule type: return changes
            changed_indices = self.replace(state, matches)

            # draw new colours for the changed indices
            #state['game'].draw(state, changed_indices)

            # return state, changd indices and flag
            return state, changed_indices, True

        # no changes: return unchanged state, empty index list and flag
        else:
            return state, [], False
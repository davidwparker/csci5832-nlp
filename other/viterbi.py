def viterbi(obs,state):
    ''' 
    Based on figure 5.17 page 147
    '''
    a = obs
    b = state
    T = len(a)
    N = len(b)
    vit = [[0 for i in range(N+2)] for j in range(T)]
    back = [[0 for i in range(N+2)] for j in range(T)]
    
    # Initialization
    for s in range(1,N-1):
        print s, a[0][s], b[s][1]
        vit[s][1] = a[0][s] * b[s][1]
        back[s][1] = 0

    # Recursion
    for t in range(2,T):
        for s in range(1,N):
            vit[s][t] = max(vit[sp][t-1]) * a[sp][s] * b[s][t]
            back[s][t] = max(vit[sp][t-1]) * a[sp][s]

    # Termination
    qf = 5
    vit[qf][T] = max(vit[s][T]) * a[s][qf]
    back[qf][T] = max(vit[s][T]) * a[s][qf]
    return back

def do_max(matrix):
    '''
    return max from a matrix
    '''
                      # can use max() here?
    for i in range(len(matrix)):
        n = 0
                          

def main():
    '''
    do it
    '''
    tag_transitions = [[0.019, 0.0043, 0.041, 0.067],
                       [0.0038, 0.035, 0.047, 0.0070],
                       [0.83, 0, 0,00047, 0],
                       [0.004, 0.016, 0.087, 0.0045],
                       [0.23, 0.00079, 0.0012, 0.00014]]
    print tag_transitions
    observations = [[0, 0.0093, 0, 0.00012],
                    [0, 0, 0.99, 0],
                    [0, 0.000054, 0, 0.00057],
                    [0.37, 0, 0, 0]]
    print observations
    print viterbi(observations,tag_transitions)
    

if __name__ == '__main__':
    main()

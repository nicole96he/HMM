from filter import filter

'''
This part provides all needed information for this problem,
including a sequence of sensor readings, knowledge of maze,
and colors of each location of the maze. I also provide ground truth 
here to help display correct motions.
'''
maze = ['#..#','...#','..##','####']
sensors = ['yellow',' blue ','  red ',' green']
colors = {(0,1):'  blue  ', (0,2):'   red  ', (1,0):'  blue  ',
          (1,1):'  blue  ', (1,2):' yellow ', (2,0):'  green ',
          (2,1):'   red  '}
ground_truth = [(1,2),(1,1),(2,1),(2,0)]

'''
Show original maze
'''
print ('Display the maze:')
for i in range(len(maze)):
    for j in range(len(maze[0])):
        if maze[i][j] == '#':
            print ('    #   ', end = '')
        else:
            print (colors[(i,j)],end = '')
    print ('')

'''
Call filtering and get a sequence of probability distributions 
describing the possible locations of the robot at each step.
'''
solution = filter(sensors, maze, colors)
dis = solution.markov_filter()


'''
Show actual state at each step
'''
print ('Begin to move:')
for move_index in range(len(sensors)):
    print ('Actual state after step ', move_index+1,':')
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                print ('    #    ',end = '')
            elif (i,j) == ground_truth[move_index]:
                print ('  Robot  ',end = '')
            else:
                print (colors[(i,j)],end = ' ')
        print ('')

    print ('Distribution after step', move_index+1,':')
    cur_dis = dis[move_index].tolist()[0]

    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                print ('    #    ',end = '')
            else:
                print ('%f'%cur_dis.pop(0),end = ' ')
        print ('')
    print ('')





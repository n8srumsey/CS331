from agent import BF, MT, CB, NA, a_star_search
from board import Board

def test(heuristic):

    optimal_solutions = {
        "10:21":['left', 'up', 'up', 'left', 'down', 'down', 'right', 'up', 'up', 'left'],
        "20:77":['down','right','up','up','left','down','down','right','up','left','left','up','right','down','down','left','up','up'],
        "30:39":['right','right','up','up','left','left','down','down','right','up','up','right','down','down','left','up','up','left'],
        "40:8":['right','up','left','down','left','up','right','down','down','left','up','up','right','down','right','down','left','left','up','up','right','right','down','down','left','up','up','left'],
        "50:402":['up','up','left','down','down','right','up','left','left','up','right','right','down','left','down','right','up','left','left','up']
    }

    for i, (m, s) in enumerate(zip([10,20,30,40,50], [21, 77, 39, 8, 402])):

        board = Board(m,s)

        solution = a_star_search(board, heuristic)
        correct = board.check_solution(solution)

        if correct:
            if len(solution) == len(optimal_solutions[f"{m}:{s}"]):
                print(f"Optimal soultion for problem {i} where m={m} and s={s}")
            else:
                print(f"Suboptimal soultion for problem {i} where m={m} and s={s}")
        else:
            if solution == []:
                print(f"Solution Timed Out for problem {i} where m={m} and s={s}")
            else:
                print(f"Incorrect soultion for problem {i} where m={m} and s={s}")


import time

print(" Tests for BF Heuristic")
start_time = time.time()
try:
    test(BF)
except Exception as e:
    print("The following Error has occurred")
    print(e)
end_time = time.time()
print("Time elapsed: ", end_time - start_time, "seconds")
print()



print("Tests for MT Heuristic")
start_time = time.time()
try:
    test(MT)
except Exception as e:
    print("The following Error has occurred")
    print(e)
end_time = time.time()
print("Time elapsed: ", end_time - start_time, "seconds")
print()



print("Test for CB Heuristic")
start_time = time.time()
try:
    test(CB)
except Exception as e:
    print("The following Error has occurred")
    print(e)
end_time = time.time()
print("Time elapsed: ", end_time - start_time, "seconds")
print()



print("Test for NA Heuristic")
start_time = time.time()
try:
    test(NA)
except Exception as e:
    print("The following Error has occurred")
    print(e)
end_time = time.time()
print("Time elapsed: ", end_time - start_time, "seconds")
print()



            



from ortools.linear_solver import pywraplp
from datetime import datetime
import pandas as pd
import time

def Requirements(C_Buffet, I_Buffet, I_Reserve):
    Req = []
    for i in range(7):
        Req.append([[4, 4, 1], [1, 3, 1],  [0, 0, 0]])

    for i in range(7):
        if C_Buffet[i]:
            Req[i][1][0] += 1
            Req[i][1][1] += 1
        if I_Reserve[i]:
            Req[i][2][0] += 1
            Req[i][2][1] += 2
            Req[i][2][2] += 1
        if I_Buffet[i] and I_Reserve[i]:
            Req[i][2][1] += 1

    return Req

def day_state(PH, Day):
    day_status = []
    for i in range(len(PH)):
      if not pd.isna(PH[i]):
        day_status.append(2)
      elif Day[i] == 'Saturday' or Day[i] == 'Sunday':
        day_status.append(1)
      else:
        day_status.append(0)

    return day_status


def smart_Schedule(input):

    Chinese = input['Chinese_Buffet_Busy'].tolist()
    Indian = input['Indian_Buffet_Busy'].tolist()
    Indian_R = input['India_Reservation'].tolist()
    PH = input['Public Holiday'].tolist()
    Day = input['Day'].tolist()

    req = Requirements(Chinese, Indian, Indian_R)
    day_status = day_state(PH, Day)

    def kitchen_Schedule(req, day_status):

        kitchen_req = [[], [], [], [], [], [], []]
        for i in range(7):
            for j in range(3):
                if j == 0: kitchen_req[i].append(req[i][j][0])
                elif j == 1: kitchen_req[i].extend([req[i][j][0] for k in range(2)])
                else: kitchen_req[i][2] += req[i][j][0]

        Rank = [kitchen_req[i][2] for i in range(7)]
        info = [i[0] for i in sorted(enumerate(Rank), key=lambda x:x[1])]
        lst = []
        for i in range(7):
            for j in range(7):
                if i == info[j]: lst.append(j)

        Shifts = [6.5, 1, 2]

        solver = pywraplp.Solver.CreateSolver('SCIP')
        variables = [solver.IntVar(0, 1, f'x{i}') for i in range(1, 106)]

        # Minimum hours
        for i in range(5):
            constraint = solver.Constraint(40, solver.infinity())
            for j in range(7):
                key = (i * 21) + (j * 3)
                constraint.SetCoefficient(variables[key], Shifts[0])
                constraint.SetCoefficient(variables[key+1], Shifts[1])
                constraint.SetCoefficient(variables[key+2], Shifts[2])

        # Schedule meets requirements for the week
        for i in range(21):
            constraint = solver.Constraint(kitchen_req[i//3][i%3], solver.infinity())
            for j in range(5):
                constraint.SetCoefficient(variables[i+(j*21)], 1)

        # At least one day off
        # Idea: A1 off on least bziest day, A2 off on 2nd least bziest day, ..., A5 off on 5th least bziest day
        for i in range(5):
            constraint = solver.Constraint(0, 0)
            key = (i*21) + (lst[i]*3)
            for j in range(key, key+3):
                constraint.SetCoefficient(variables[j], 1)

        # Cost function
        objective = solver.Objective()
        for i in range(5):
            for j in range(7):
                key = (i * 21) + (j * 3)
                tmp = 15 + day_status[j]
                objective.SetCoefficient(variables[key], tmp*Shifts[0])
                objective.SetCoefficient(variables[key+1], tmp*Shifts[1])
                objective.SetCoefficient(variables[key+2], tmp*Shifts[2])
        objective.SetMinimization

        # Solve
        status = solver.Solve()
        lst = []
        if status == pywraplp.Solver.OPTIMAL:
            for i, var in enumerate(variables):
                lst.append(var.solution_value())
            roster = [[[], [], []] for i in range(7)]
            names = ["A1", "A2", "A3", "A4", "A5"]
            cnt = 0
            for workers in range(5):
                for days in range(7):
                    for hour_shift in range(3):
                        if lst[cnt] == 1: roster[days][hour_shift].append(names[workers])
                        cnt +=1
            return roster
        else:
            print('The problem does not have an optimal solution.')
    def SP_Schedule(req, day_status):

        # Schedule meets requirements for the week
        service_req = [[], [], [], [], [], [], []]
        for i in range(7):
            for j in range(3):
                if j == 0: service_req[i].append(req[i][j][1])
                elif j == 1: service_req[i].extend([req[i][j][1] for k in range(2)])
                else: service_req[i][2] += req[i][j][1]

        print(service_req)

        Rank = [service_req[i][2] for i in range(7)]
        info = [i[0] for i in sorted(enumerate(Rank), key=lambda x:x[1])]
        Rank_lst = []
        for i in range(7):
            for j in range(7):
                if i == info[j]: Rank_lst.append(j)

        Shifts = [6.5, 1, 2]

        for k in range(8):

            solver = pywraplp.Solver.CreateSolver('CP-SAT')
            variables = [solver.IntVar(0, 1, f'x{i}') for i in range(1, 169)]

            # Minimum hours
            for i in range(8):
                tmp = 33
                if i >= 3: tmp = 40
                constraint = solver.Constraint(tmp, solver.infinity())
                for j in range(7):
                    key = (i * 21) + (j * 3)
                    constraint.SetCoefficient(variables[key], Shifts[0])
                    constraint.SetCoefficient(variables[key+1], Shifts[1])
                    constraint.SetCoefficient(variables[key+2], Shifts[2])

            # Schedule meets requirements for the week
            for i in range(21):
                constraint = solver.Constraint(service_req[i//3][i%3], solver.infinity())
                for j in range(8):
                    constraint.SetCoefficient(variables[i+(j*21)], 1)

            # At least one day off
            # Idea: A1 off on least bziest day, A2 off on 2nd least bziest day, ..., A5 off on 5th least bziest day
            ## 1st person go on off whenver possible

            if k < 7:
              constraint = solver.Constraint(0, 0)
              tmp = Rank_lst[k]*3
              for i in range(3):
                  constraint.SetCoefficient(variables[tmp+i], 1)

            for i in range(7):
                constraint = solver.Constraint(0, 0)
                key = ((i+1)*21) + (Rank_lst[i]*3)
                for j in range(key, key+3):
                    constraint.SetCoefficient(variables[j], 1)

            # Cost function
            objective = solver.Objective()
            for i in range(8):
                for j in range(7):
                    key = (i * 21) + (j * 3)
                    tmp = 13 + day_status[j]
                    if i >= 3: tmp += 1
                    objective.SetCoefficient(variables[key], tmp*Shifts[0])
                    objective.SetCoefficient(variables[key+1], tmp*Shifts[1])
                    objective.SetCoefficient(variables[key+2], tmp*Shifts[2])
            objective.SetMinimization

            # Solve
            status = solver.Solve()
            lst = []
            if status == pywraplp.Solver.OPTIMAL:
                  for i, var in enumerate(variables):
                      lst.append(var.solution_value())
                  roster = [[[], [], []] for i in range(7)]
                  names = ["D1", "D2", "D3", "B1", "B2", "B3", "B4", "B5"]
                  cnt = 0
                  for workers in range(8):
                      for days in range(7):
                          for hour_shift in range(3):
                              if lst[cnt] == 1: roster[days][hour_shift].append(names[workers])
                              cnt +=1
                  return roster
            else:
                  print('The problem does not have an optimal solution.')


    def dish_Schedule(req, day_status):

        dish_req = [[], [], [], [], [], [], []]
        for i in range(7):
            for j in range(3):
                if j == 0: dish_req[i].append(req[i][j][2])
                elif j == 1: dish_req[i].extend([req[i][j][2] for k in range(2)])
                else: dish_req[i][2] += req[i][j][2]

        Rank = [dish_req[i][2] for i in range(7)]
        info = [i[0] for i in sorted(enumerate(Rank), key=lambda x:x[1])]
        lst = []
        for i in range(7):
            for j in range(7):
                if i == info[j]: lst.append(j)

        Shifts = [6.5, 1, 2]

        solver = pywraplp.Solver.CreateSolver('SCIP')
        variables = [solver.IntVar(0, 1, f'x{i}') for i in range(1, 43)]

        # Minimum hours
        for i in range(2):
            constraint = solver.Constraint(40, solver.infinity())
            for j in range(7):
                key = (i * 21) + (j * 3)
                constraint.SetCoefficient(variables[key], Shifts[0])
                constraint.SetCoefficient(variables[key+1], Shifts[1])
                constraint.SetCoefficient(variables[key+2], Shifts[2])

        # Schedule meets requirements for the week
        for i in range(21):
            constraint = solver.Constraint(dish_req[i//3][i%3], solver.infinity())
            for j in range(2):
                constraint.SetCoefficient(variables[i+(j*21)], 1)

        # At least one day off
        # Idea: Need 2 least buziest day that is not 2 dishwashers if only everyday except one is 2 dish, then prioritise C1
        if Rank[lst[0]] < 2:
          constraint = solver.Constraint(0, 0)
          tmp1 = lst[0]*3
          for i in range(3):
                constraint.SetCoefficient(variables[tmp1+i], 1)
        if Rank[lst[1]] < 2:
          constraint = solver.Constraint(0, 0)
          tmp2 = 21 + lst[1]*3
          for i in range(3):
              constraint.SetCoefficient(variables[tmp2+i], 1)

        # Cost function
        objective = solver.Objective()
        cnt = 0
        for i in range(2):
            for j in range(7):
                key = (i * 21) + (j * 3)
                tmp = 14 + day_status[j]
                objective.SetCoefficient(variables[key], tmp*Shifts[0])
                objective.SetCoefficient(variables[key+1], tmp*Shifts[1])
                objective.SetCoefficient(variables[key+2], tmp*Shifts[2])
        objective.SetMinimization

        # Solve
        status = solver.Solve()
        lst = []
        if status == pywraplp.Solver.OPTIMAL:
            for i, var in enumerate(variables):
                lst.append(var.solution_value())
            roster = [[[], [], []] for i in range(7)]
            names = ["C1", "C2"]
            cnt = 0
            for workers in range(2):
                for days in range(7):
                    for hour_shift in range(3):
                        if lst[cnt] == 1: roster[days][hour_shift].append(names[workers])
                        cnt +=1
        else:
            print('The problem does not have an optimal solution.')

        return roster


    kitchen = kitchen_Schedule(req, day_status)
    serve = SP_Schedule(req, day_status)
    dish = dish_Schedule(req, day_status)

    full_Schedule = kitchen
    for i in range(7):
        for j in range(3):
            full_Schedule[i][j].extend(serve[i][j])
            full_Schedule[i][j].extend(dish[i][j])

    return full_Schedule


df = pd.read_csv("../output/predictions.csv").head(7)

print(smart_Schedule(df))

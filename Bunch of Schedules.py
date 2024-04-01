from ortools.linear_solver import pywraplp
import random

def smart_Schedule(C_Buffet, I_Buffet, I_Reserve, day_status):

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
                Req[i][2][0] += 1
                Req[i][2][1] += 1
                
        return Req
    
    def kitchen_Schedule(C_Buffet, I_Buffet, I_Reserve, day_status):
        solver = pywraplp.Solver.CreateSolver('SCIP')
        variables = [solver.IntVar(0, 1, f'x{i}') for i in range(1, 351)]

        # Minimum hours
        for i in range(5):
            constraint = solver.Constraint(40, solver.infinity())
            for j in range(i*70, (i+1)*70):
                constraint.SetCoefficient(variables[j], 1)
        
        # Schedule meets requirements for the week
        req = Requirements(C_Buffet, I_Buffet, I_Reserve)
        kitchen_req = [[], [], [], [], [], [], []]
        for i in range(7):
            for j in range(3):
                if j == 0: kitchen_req[i].extend([req[i][j][0] for k in range(7)])
                elif j == 1: kitchen_req[i].extend([req[i][j][0] for k in range(3)])
                else:
                    for k in range(2): kitchen_req[i][-(k+1)] += req[i][j][0]
        for i in range(70):
            constraint = solver.Constraint(kitchen_req[i//10][i%10], solver.infinity())
            for j in range(5):
                constraint.SetCoefficient(variables[i+(j*70)], 1)
        
        # At least one day off
        # Idea: A1 off on least bziest day, A2 off on 2nd least bziest day, ..., A5 off on 5th least bziest day
        Rank = [kitchen_req[i][9] for i in range(7)]
        info = [i[0] for i in sorted(enumerate(Rank), key=lambda x:x[1])]
        lst = []
        for i in range(7):
            for j in range(7):
                if i == info[j]: lst.append(j)
                
        for i in range(5):
            constraint = solver.Constraint(0, 0)
            key = (i*70) + (lst[i]*10)
            for j in range(key, key+10):
                constraint.SetCoefficient(variables[j], 1)

        # Cost function
        objective = solver.Objective()
        cnt = 0
        for i in range(5):
            for j in range(7):
                for k in range(10):
                    tmp = 15 + day_status[j]
                    objective.SetCoefficient(variables[cnt], tmp)
                    cnt += 1
        objective.SetMinimization

        # Solve
        status = solver.Solve()
        lst = []
        if status == pywraplp.Solver.OPTIMAL:
            print('This is an optimal schedule and here is the cost for the week:', solver.Objective().Value())
            for i, var in enumerate(variables):
                lst.append(var.solution_value())
            roster = [[[], [], [], [], [], [], [], [], [], []] for i in range(7)]
            names = ["A1", "A2", "A3", "A4", "A5"]
            cnt = 0
            for workers in range(5):
                for days in range(7):
                    for hour_shift in range(10):
                        if lst[cnt] == 1: roster[days][hour_shift].append(names[workers])
                        cnt +=1
        else:
            print('The problem does not have an optimal solution.')
        
        return solver.Objective().Value(), roster
    
    def SP_Schedule(C_Buffet, I_Buffet, I_Reserve, day_status):
        solver = pywraplp.Solver.CreateSolver('SCIP')
        variables = [solver.IntVar(0, 1, f'x{i}') for i in range(1, 561)]

        # Minimum hours for Full-Time service and Part-Time
        for i in range(5):
            tmp = 33
            if i >= 3: tmp =40
            constraint = solver.Constraint(tmp, solver.infinity())
            for j in range(i*70, (i+1)*70):
                constraint.SetCoefficient(variables[j], 1)
      
        # Schedule meets requirements for the week
        req = Requirements(C_Buffet, I_Buffet, I_Reserve)
        service_req = [[], [], [], [], [], [], []]
        for i in range(7):
            for j in range(3):
                # Lunch hours
                if j == 0: service_req[i].extend([req[i][j][1] for k in range(7)])
                # Chinese Buffet
                elif j == 1: service_req[i].extend([req[i][j][1] for k in range(3)])
                # Indian Buffet
                else:
                    for k in range(2): service_req[i][-(k+1)] += req[i][j][1]
      
        
        for i in range(70):
            constraint = solver.Constraint(service_req[i//10][i%10], solver.infinity())
            for j in range(8):
                constraint.SetCoefficient(variables[i+(j*70)], 1)

        # At least one day off
        # Idea: D1, D2 off on least bziest day, D3 off on 2nd least bziest day, ..., (D1 D2 D3 B1 B2 B3 B4 B5)
        Rank = [service_req[i][9] for i in range(7)]
        info = [i[0] for i in sorted(enumerate(Rank), key=lambda x:x[1])]
        lst = []
        for i in range(7):
            for j in range(7):
                if i == info[j]: lst.append(j)

        ## 2 ppl go on off
        constraint = solver.Constraint(0, 0)
        for i in range(10):
            tmp1 = lst[0]*10
            tmp2 = 70 + tmp1
            constraint.SetCoefficient(variables[tmp1+i], 1)
            constraint.SetCoefficient(variables[tmp2+i], 1)
        ## 1 ppl go on off
        for i in range(6):
            constraint = solver.Constraint(0, 0)
            key = ((i+2)*70) + (lst[i+1]*10)
            for j in range(key, key+10):
                constraint.SetCoefficient(variables[j], 1)
        

        # Cost function
        objective = solver.Objective()
        cnt = 0
        for i in range(8):
            for j in range(7):
                for k in range(10):
                    tmp = 13 + day_status[j]
                    if i >= 3: tmp += 1
                    objective.SetCoefficient(variables[cnt], tmp)
                    cnt += 1
        objective.SetMinimization

        # Solve
        status = solver.Solve()
        lst = []
        if status == pywraplp.Solver.OPTIMAL:
            print('This is an optimal schedule and here is the cost for the week:', solver.Objective().Value())
            for i, var in enumerate(variables):
                lst.append(var.solution_value())
            roster = [[[], [], [], [], [], [], [], [], [], []] for i in range(7)]
            names = ["D1", "D2", "D3", "B1", "B2", "B3", "B4", "B5"]
            cnt = 0
            for workers in range(8):
                for days in range(7):
                    for hour_shift in range(10):
                        if lst[cnt] == 1: roster[days][hour_shift].append(names[workers])
                        cnt +=1
        else:
            print('The problem does not have an optimal solution.')

        return solver.Objective().Value(), roster
    
    def dish_Schedule(C_Buffet, I_Buffet, I_Reserve, day_status):
        solver = pywraplp.Solver.CreateSolver('SCIP')
        variables = [solver.IntVar(0, 1, f'x{i}') for i in range(1, 141)]

        # Minimum hours
        for i in range(2):
            constraint = solver.Constraint(40, solver.infinity())
            for j in range(i*70, (i+1)*70):
                constraint.SetCoefficient(variables[j], 1)

        # Schedule meets requirements for the week
        req = Requirements(C_Buffet, I_Buffet, I_Reserve)
        dish_req = [[], [], [], [], [], [], []]
        for i in range(7):
            for j in range(3):
                if j == 0: dish_req[i].extend([req[i][j][2] for k in range(7)])
                elif j == 1: dish_req[i].extend([req[i][j][2] for k in range(3)])
                else:
                    for k in range(2): dish_req[i][-(k+1)] += req[i][j][2]
        for i in range(70):
            constraint = solver.Constraint(dish_req[i//10][i%10], solver.infinity())
            for j in range(2):
                constraint.SetCoefficient(variables[i+(j*70)], 1)

        # At least one day off
        # Idea: Need 2 least buziest day that is not 2 dishwashers if only everyday except one is 2 dish, then prioritise C1
        Rank = [dish_req[i][9] for i in range(7)]
        info = [i[0] for i in sorted(enumerate(Rank), key=lambda x:x[1])]
        lst = []
        for i in range(7):
            for j in range(7):
                if i == info[j]: lst.append(j)
        
        if Rank[lst[0]] < 2:
          constraint = solver.Constraint(0, 0)
          tmp1 = lst[0]*10
          for i in range(10):
                constraint.SetCoefficient(variables[tmp1+i], 1)
        if Rank[lst[1]] < 2:
          constraint = solver.Constraint(0, 0)
          tmp2 = lst[1]*10
          for i in range(10):
              constraint.SetCoefficient(variables[tmp2+i], 1)

        # Cost function
        objective = solver.Objective()
        cnt = 0
        for i in range(2):
            for j in range(7):
                for k in range(10):
                    tmp = 14 + day_status[j]
                    objective.SetCoefficient(variables[cnt], tmp)
                    cnt += 1
        objective.SetMinimization

        # Solve
        status = solver.Solve()
        lst = []
        if status == pywraplp.Solver.OPTIMAL:
            print('This is an optimal schedule and here is the cost for the week:', solver.Objective().Value())
            for i, var in enumerate(variables):
                lst.append(var.solution_value())
            roster = [[[], [], [], [], [], [], [], [], [], []] for i in range(7)]
            names = ["C1", "C2"]
            cnt = 0
            for workers in range(2):
                for days in range(7):
                    for hour_shift in range(10):
                        if lst[cnt] == 1: roster[days][hour_shift].append(names[workers])
                        cnt +=1
        else:
            print('The problem does not have an optimal solution.')

        return solver.Objective().Value(), roster
    
    kitchen = kitchen_Schedule(C_Buffet, I_Buffet, I_Reserve, day_status)
    serve = SP_Schedule(C_Buffet, I_Buffet, I_Reserve, day_status)
    dish = dish_Schedule(C_Buffet, I_Buffet, I_Reserve, day_status)

    full_Schedule = kitchen[1]
    for i in range(7):
        for j in range(10):
            full_Schedule[i][j].extend(serve[1][i][j])
            full_Schedule[i][j].extend(dish[1][i][j])
    total_cost = kitchen[0] + serve[0] + dish[0]
    return total_cost, full_Schedule

Chinese = [1, 0, 1, 0, 0, 0, 1]
Indian1 = [1, 0, 0, 0, 0, 1, 0]
Indian2 = [0, 1, 1, 0, 0, 1, 0]
day_status = [0, 2, 0, 0, 0, 1, 1]
Jesus = smart_Schedule(Chinese, Indian1, Indian2, day_status)
print(Jesus[0])
for i in range(7): print(Jesus[1][i])

def dumb_Schedule(I_Reserve, day_status):
    A = ["A1", "A2", "A3", "A4", "A5"]
    B = ["B1", "B2", "B3", "B4", "B5"]
    C = ["C1", "C2"]
    D = ["D1", "D2", "D3"]
    Rates = [15, 14, 13]
    random.shuffle(A)
    random.shuffle(B)
    random.shuffle(C)
    random.shuffle(D)
    
    A1, A2, A3, A4, A5 = A[0], A[1], A[2], A[3], A[4]
    B1, B2, B3, B4, B5 = B[0], B[1], B[2], B[3], B[4]
    C1, C2 = C[0], C[1]
    D1, D2, D3 = D[0], D[1], D[2]
    
    # Strategy behind this baseline schedule: "Buffet focused and Prepare for the worst"
    # Cycle Order for services and part time: B1 D1 D3 D2 B3 B4 B2 B5
    # A5, B1, C2, D1 on off
    Mon = [[A1, A2, A3, A4, B3, B4, C1, D2, D3], [A1, A2, A3, A4, B3, B4, C1, D2, D3], [A1, A2, A3, A4, B3, B4, C1, D2, D3], [A1, A2, A3, A4, B3, B4, C1, D2, D3],
           [A1, A2, A3, A4, B3, B4, C1, D2, D3], [A1, A2, A3, A4, B3, B4, C1, D2, D3], [A1, A2, A3, A4, B3, B4, C1, D2, D3], [A3, A4, B2, B3, B4, B5, C1], 
           [A3, A4, B2, B3, B4, B5, C1], [A3, A4, B2, B3, B4, B5, C1], [A2, C2, D2, D3]]
    # A4, D3, C1 on off
    Tues = [[A1, A2, A3, A5, B2, B3, B4, C2, D2], [A1, A2, A3, A5, B2, B3, B4, C2, D2], [A1, A2, A3, A5, B2, B3, B4, C2, D2], [A1, A2, A3, A5, B2, B3, B4, C2, D2], 
            [A1, A2, A3, A5, B2, B3, B4, C2, D2], [A1, A2, A3, A5, B2, B3, B4, C2, D2], [A1, A2, A3, A5, B2, B3, B4, C2, D2], [A2, A3, B1, B2, B5, C2, D1], 
            [A2, A3, B1, B2, B5, C2, D1], [A2, A3, B1, B2, B5, C2, D1], [A1, B3, B4, C1]]
    # A3, D2 on off
    Wed = [[A1, A2, A4, A5, B2, B3, B4, B5, C1], [A1, A2, A4, A5, B2, B3, B4, B5, C1], [A1, A2, A4, A5, B2, B3, B4, B5, C1], [A1, A2, A4, A5, B2, B3, B4, B5, C1], 
           [A1, A2, A4, A5, B2, B3, B4, B5, C1], [A1, A2, A4, A5, B2, B3, B4, B5, C1], [A1, A2, A4, A5, B2, B3, B4, B5, C1], [A1, A2, B1, B5, C2, D1, D3], 
           [A1, A2, B1, B5, C2, D1, D3], [A1, A2, B1, B5, C2, D1, D3], [A5, B2, B4, C1]]
    # A2, B3 on off
    Thurs = [[A1, A3, A4, A5, B1, B2, B4, B5, C2], [A1, A3, A4, A5, B1, B2, B4, B5, C2], [A1, A3, A4, A5, B1, B2, B4, B5, C2], [A1, A3, A4, A5, B1, B2, B4, B5, C2], 
             [A1, A3, A4, A5, B1, B2, B4, B5, C2], [A1, A3, A4, A5, B1, B2, B4, B5, C2], [A1, A3, A4, A5, B1, B2, B4, B5, C2], [A1, A5, B1, C1, D1, D2, D3], 
             [A1, A5, B1, C1, D1, D2, D3], [A1, A5, B1, C1, D1, D2, D3], [A4, B2, B4, C2]]
    # A1, B4 on off
    Fri = [[A2, A3, A4, A5, B1, B2, B5, C1, D1], [A2, A3, A4, A5, B1, B2, B5, C1, D1], [A2, A3, A4, A5, B1, B2, B5, C1, D1], [A2, A3, A4, A5, B1, B2, B5, C1, D1], 
           [A2, A3, A4, A5, B1, B2, B5, C1, D1], [A2, A3, A4, A5, B1, B2, B5, C1, D1], [A2, A3, A4, A5, B1, B2, B5, C1, D1], [A4, A5, B3, C2, D1, D2, D3], 
           [A4, A5, B3, C2, D1, D2, D3], [A4, A5, B3, C2, D1, D2, D3], [A3, B2, B5, C1]]
    # B2 on off
    Sat = [[A1, A2, A3, A4, B1, B5, C2, D1, D3], [A1, A2, A3, A4, B1, B5, C2, D1, D3], [A1, A2, A3, A4, B1, B5, C2, D1, D3], [A1, A2, A3, A4, B1, B5, C2, D1, D3], 
           [A1, A2, A3, A4, B1, B5, C2, D1, D3], [A1, A2, A3, A4, B1, B5, C2, D1, D3], [A1, A2, A3, A4, B1, B5, C2, D1, D3], [A4, A5, B3, B4, C1, D2, D3], 
           [A4, A5, B3, B4, C1, D2, D3], [A4, A5, B3, B4, C1, D2, D3], [A3, B1, B5, C2]]
    # B5 on off
    Sun = [[A1, A2, A4, A5, B1, C1, D1, D3, D2], [A1, A2, A4, A5, B1, C1, D1, D3, D2], [A1, A2, A4, A5, B1, C1, D1, D3, D2], [A1, A2, A4, A5, B1, C1, D1, D3, D2], 
           [A1, A2, A4, A5, B1, C1, D1, D3, D2], [A1, A2, A4, A5, B1, C1, D1, D3, D2], [A1, A2, A4, A5, B1, C1, D1, D3, D2], [A1, A2, B2, B3, B4, C2, D2], 
           [A1, A2, B2, B3, B4, C2, D2], [A1, A2, B2, B3, B4, C2, D2], [A3, B1, C1, D1]]
    
    stupid_roster = [Mon, Tues, Wed, Thurs, Fri, Sat, Sun]
    cost = 0
    for i in range(7):
        for j in range(10):
            for ppl in stupid_roster[i][j]:
                if ppl in A: cost += (Rates[0] + day_status[i])
                elif ppl in D: cost += (Rates[2] + day_status[i])
                else: cost += (Rates[1] + day_status[i])
        if I_Reserve[i]:
            for ppl in stupid_roster[i][10]:
                if ppl in A: cost += (Rates[0] + day_status[i])
                elif ppl in D: cost += (Rates[2] + day_status[i])
                else: cost += (Rates[1] + day_status[i])

    return cost, stupid_roster

Plebs = dumb_Schedule(Indian2, day_status)
print(Plebs[0])
for i in range(7): print(Plebs[1][i])






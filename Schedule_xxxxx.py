import pandas as pd
import random

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

Chinese = [1, 0, 1, 0, 0, 0, 1] 
Indian1 = [1, 0, 0, 0, 0, 1, 0]
Indian2 = [0, 1, 1, 0, 0, 1, 0]


A = ["A1", "A2", "A3", "A4", "A5"]
B = ["B1", "B2", "B3", "B4", "B5"]
C = ["C1", "C2"]
D = ["D1", "D2", "D3"]

Staffs = {"Kitchen":A, "Service":B, "Dishwasher":C, "Part-Time":D}

def Cycle(lst, idx):
    assert idx <= len(lst)
    for i in range(idx):
        tmp = lst[i]
        lst.append(tmp)
    del lst[0:idx] 
    return lst
    
def Schedule(Staff, C_Buffet, I_Buffet, I_Reserve):
    req = Requirements(C_Buffet, I_Buffet, I_Reserve)

    S_off, D_off = 0, 0
    for i in range(7):
        if req[i][1][1] + req[i][2][1] < 7: S_off +=1
        if req[i][1][2] + req[i][2][2] < 2: D_off += 1
    if D_off < 2: print("Warning: there will at least be one Dishwasher that cannot have off this week")
    if S_off < 1: print("warning: there will at least one Service/Part-Time staff that cannot have off this week")

    A = Staff["Kitchen"]
    B = Staff["Service"]
    C = Staff["Dishwasher"]
    D = Staff["Part-Time"]

    random.shuffle(A)
    random.shuffle(B)
    random.shuffle(C)
    random.shuffle(D)

    T = [B[0], D[0], D[1], D[2], B[1], B[2], B[3], B[4]]

    ### A1 A2 A3 A4 A5
    ### B1 D1 D2 D3 B2 B3 B4 B5
    ### Bziest day C split half days by default Sat
    ### Least bziest day 2 service/part and 1 dish off, default mon
    ### 2nd least bziest day 1 dish off
    ### Since bziset day corr to num of service/part staff, we shall define bziness of a day by total no. of service staff needed for both buffet service

    Ser = []
    for i in range(7):
        Ser.append(req[i][1][1] +req[i][2][1])
    info = [i[0] for i in sorted(enumerate(Ser), key=lambda x:x[1])]

    ### All is good above, just make sure not to overload var name!

    ### Now I need a list of dicts of lists [{lunch:[], chinese:[], indian[]}, ...., {lunch:[], chinese[], indian[]}]

    print("Hello")
    lst = []
    for i in range(7):
        day = {"Lunch": [], "Chinese":[], "Indian":[]}
        ### status:
        
        split = (info[i] == 0)
        db_s_off = (info[i] == 6 and (req[i][1][1] + req[i][2][1]) < 7)
        one_d_off = (info[i] == 6 and (req[i][1][2] + req[i][2][2]) < 2)
        two_d_off = (info[i] == 5 and (req[i][1][2] + req[i][2][2]) < 2)
        
        ### e.g. its monday so a2 a3 a4 a5, then we also start with a2 a3 a4 a5
        ### deal with who's on off first
        
        Day_K_cycle = Cycle(A, i%5)
        Day_T_cycle = Cycle(T, i%8)
        Day_D_cycle = Cycle(C, i%2)
        if one_d_off: Day_T_cycle = Day_T_cycle[1:]

        print(Day_D_cycle[0])

        day["Lunch"].extend(Day_K_cycle[0:3])
        day["Lunch"].extend(Day_T_cycle[0:3])
        day["Lunch"].append(Day_D_cycle[0])

        day["Chinese"].extend(Day_K_cycle[0:req[i][1][0]])
        day["Chinese"].extend(Day_T_cycle[0:req[i][1][1]])
        day["Chinese"].append(Day_D_cycle[0])

        if req[i][2][0] >0 :
            day["Indian"].extend(Day_K_cycle[0:req[i][2][0]])
            day["Indian"].extend(Day_T_cycle[0:req[i][2][1]])
            day["Indian"].append(Day_D_cycle[1])
            
        lst.append(day)
    return lst 


print(Schedule(Staffs, Chinese, Indian1, Indian2))

    
    
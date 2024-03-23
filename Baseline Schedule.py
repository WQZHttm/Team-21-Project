import random
import pandas as pd

A = ["A1", "A2", "A3", "A4", "A5"]
B = ["B1", "B2", "B3", "B4", "B5"]
C = ["C1", "C2"]
D = ["D1", "D2", "D3"]
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
Mon = {"10-11":[A1, A2, A3, A4, B3, C1, D2, D3], "11-12":[A1, A2, A3, A4, B3, C1, D2, D3], "12-13":[A1, A2, A3, A4, B3, C1, D2, D3], "13-14":[A1, A2, A3, A4, B3, C1, D2, D3],
       "14-15":[A1, A2, A3, A4, B3, C1, D2, D3], "15-16":[A1, A2, A3, A4, B3, C1, D2, D3], "16-17":[A1, A2, A3, A4, B3, C1, D2, D3], "19-20":[A3, A4, B2, B4, B5, C1],
       "20-21":[A3, A4, B2, B4, B5, C1], "21-22":[A3, A4, B2, B4, B5, C1], "22-23":[B2, B4, B5, C1], "Indian Buffet":[A2, B3, C2, D2, D3]}

# A4, D3, C1 on off
Tues = {"10-11":[A1, A2, A3, A5, B3, B4, C2, D2], "11-12":[A1, A2, A3, A5, B3, B4, C2, D2], "12-13":[A1, A2, A3, A5, B3, B4, C2, D2], "13-14":[A1, A2, A3, A5, B3, B4, C2, D2],
       "14-15":[A1, A2, A3, A5, B3, B4, C2, D2], "15-16":[A1, A2, A3, A5, B3, B4, C2, D2], "16-17":[A1, A2, A3, A5, B3, B4, C2, D2], "19-20":[A2, A3, B1, B2, B5, C2, D1],
       "20-21":[A2, A3, B1, B2, B5, C2, D1], "21-22":[A2, A3, B1, B2, B5, C2, D1], "22-23":[B1, B2, B5, C2, D1], "Indian Buffet":[A1, B3, B4, C1, D2]}

# A3, D2 on off
Wed = {"10-11":[A1, A2, A4, A5, B2, B3, B4, C1], "11-12":[A1, A2, A4, A5, B2, B3, B4, C1], "12-13":[A1, A2, A4, A5, B2, B3, B4, C1], "13-14":[A1, A2, A4, A5, B2, B3, B4, C1],
       "14-15":[A1, A2, A4, A5, B2, B3, B4, C1], "15-16":[A1, A2, A4, A5, B2, B3, B4, C1], "16-17":[A1, A2, A4, A5, B2, B3, B4, C1], "19-20":[A1, A2, B1, B5, C2, D1, D3],
       "20-21":[A1, A2, B1, B5, C2, D1, D3], "21-22":[A1, A2, B1, B5, C2, D1, D3], "22-23":[B1, B5, C2, D1, D3], "Indian Buffet":[A5, B2, B3, B4, C1]}

# A2, B3 on off
Thur = {"10-11":[A1, A3, A4, A5, B2, B4, B5, C2], "11-12":[A1, A3, A4, A5, B2, B4, B5, C2], "12-13":[A1, A3, A4, A5, B2, B4, B5, C2], "13-14":[A1, A3, A4, A5, B2, B4, B5, C2],
       "14-15":[A1, A3, A4, A5, B2, B4, B5, C2], "15-16":[A1, A3, A4, A5, B2, B4, B5, C2], "16-17":[A1, A3, A4, A5, B2, B4, B5, C2], "19-20":[A1, A5, B1, C1, D1, D2, D3],
       "20-21":[A1, A5, B1, C1, D1, D2, D3], "21-22":[A1, A5, B1, C1, D1, D2, D3], "22-23":[B1, C1, D1, D2, D3], "Indian Buffet":[A4, B2, B4, B5, C2]}

# A1, B4 on off
Fri = {"10-11":[A2, A3, A4, A5, B1, B2, B5, C1], "11-12":[A2, A3, A4, A5, B1, B2, B5, C1], "12-13":[A2, A3, A4, A5, B1, B2, B5, C1], "13-14":[A2, A3, A4, A5, B1, B2, B5, C1],
       "14-15":[A2, A3, A4, A5, B1, B2, B5, C1], "15-16":[A2, A3, A4, A5, B1, B2, B5, C1], "16-17":[A2, A3, A4, A5, B1, B2, B5, C1], "19-20":[A4, A5, B3, C2, D1, D2, D3],
       "20-21":[A4, A5, B3, C2, D1, D2, D3], "21-22":[A4, A5, B3, C2, D1, D2, D3], "22-23":[B3, C2, D1, D2, D3], "Indian Buffet":[A3, B1, B2, B5, C1]}

# B2 on off
Sat = {"10-11":[A1, A2, A3, A4, B1, B5, C2, D1], "11-12":[A1, A2, A3, A4, B1, B5, C2, D1], "12-13":[A1, A2, A3, A4, B1, B5, C2, D1], "13-14":[A1, A2, A3, A4, B1, B5, C2, D1],
       "14-15":[A2, A3, A4, A5, B1, B5, C2, D1], "15-16":[A2, A3, A4, A5, B1, B5, C2, D1], "16-17":[A2, A3, A4, A5, B1, B5, C2, D1], "19-20":[A4, A5, B3, B4, C1, D2, D3],
       "20-21":[A4, A5, B3, B4, C1, D2, D3], "21-22":[A4, A5, B3, B4, C1, D2, D3], "22-23":[B3, B4, C1, D2, D3], "Indian Buffet":[A3, B1, B5, C2, D1]}

# B5 on off
Sun =  {"10-11":[A1, A2, A4, A5, B1, C1, D1, D3], "11-12":[A1, A2, A4, A5, B1, C1, D1, D3], "12-13":[A1, A2, A4, A5, B1, C1, D1, D3], "13-14":[A1, A2, A4, A5, B1, C1, D1, D3],
       "14-15":[A1, A2, A4, A5, B1, C1, D1, D3], "15-16":[A1, A2, A4, A5, B1, C1, D1, D3], "16-17":[A1, A2, A4, A5, B1, C1, D1, D3], "19-20":[A1, A2, B2, B3, B4, C2, D2],
       "20-21":[A1, A2, B2, B3, B4, C2, D2], "21-22":[A1, A2, B2, B3, B4, C2, D2], "22-23":[B2, B3, B4, C2, D2], "Indian Buffet":[A3, B1, C1, D1, D3]}

Timings = ["1000-1100", "1100-1200", "1200-1300","1300-1400", "1400-1500", "1500-1600", "1600-1700", "1900-2000", "2000-2100", "2100-2200", "2200-2300", "Indian Buffet"]

old_Schedule = {"Monday":Mon, "Tuesday":Tues, "Wednesday":Wed, "Thursday":Thur, "Friday":Fri, "Saturday":Sat, "Sunday":Sun}

def schedule_to_df(Schedule):
   lst = []
   for days in Schedule.values():
      tmp = []
      for stuff in days.values():
         tmp.append(" ".join(stuff))
      lst.append(tmp)
   return lst

print(schedule_to_df(old_Schedule))
DF_schedule = pd.DataFrame(schedule_to_df(old_Schedule), columns = Timings, dtype = str)

def cost_Schedule(Schedule, k_rate, p_rate, f_rate, PH):
   cost = 0
   day = 0
   for days in Schedule.values():
      day += 1
      shift = 0
      for stuff in days.values():
         shift += 1
         for ppl in stuff:
            p, f, k = p_rate[0], f_rate[0], k_rate[0]
            if day >= 6: p, f, k = p_rate[1], f_rate[1], k_rate[1]
            if PH[day-1] == 1: p, f, k = p_rate[2], f_rate[2], k_rate[2]
            scale = 1
            if shift == 12: scale = 3
            if ppl in A: cost += (scale*k)
            elif ppl in D: cost += (scale*p)
            else: cost += (scale*f)
   return cost
  
k_rate = [15, 16, 17]
p_rate = [13, 14, 15]
f_rate = [14, 15, 16]
PH = [1, 0, 0, 0, 0, 1, 0]

old_cost = cost_Schedule(old_Schedule, k_rate, p_rate, f_rate, PH)

Fake_Prediction = pd.DataFrame([["Monday", 49], ["Tuesday", 34], ["Wednesday", 69], ["Thursday", 46], ["Friday", 89], ["Saturday", 177], ["Sunday", 164]], 
                               columns = ["Day", "Customer Count"], dtype = float)

Trolling_plot = pd.DataFrame([["Cost of Old Schedule", old_cost], ["Cost of New Schedule", old_cost]], columns = ["Schedules", "Manpower Costs per Week"], dtype = float)

print(DF_schedule)

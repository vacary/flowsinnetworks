\* Problem: sparsestcut *\

Minimize
 obj: + q

Subject To
 capacity_sr_5: + x_s_r_5 - q <= 0
 capacity_rt_3: + x_r_t_3 - 1.1 q <= 0
 capacity_s0s_0: + x_s0_s_0 - 3.7 q <= 0
 capacity_s0r_0: + x_s0_r_0 - 0.5 q <= 0
 capacity_s0r_1: + x_s0_r_1 - 0.6 q <= 0
 capacity_s0r_2: + x_s0_r_2 - 0.7 q <= 0
 capacity_s0r_3: + x_s0_r_3 - 0.8 q <= 0
 capacity_s0r_4: + x_s0_r_4 - 0.9 q <= 0
 capacity_s0t_0: + x_s0_t_0 - 0.8 q <= 0
 capacity_s0t_1: + x_s0_t_1 - 0.9 q <= 0
 capacity_s0t_2: + x_s0_t_2 - q <= 0
 balance_s: - x_s0_s_0 + x_s_r_5 = -3.4999999997757
 balance_r: - x_s0_r_4 - x_s0_r_3 - x_s0_r_2 - x_s0_r_1 - x_s0_r_0
 - x_s_r_5 + x_r_t_3 = -2.69999999982697
 balance_s0: + x_s0_t_2 + x_s0_t_1 + x_s0_t_0 + x_s0_r_4 + x_s0_r_3
 + x_s0_r_2 + x_s0_r_1 + x_s0_r_0 + x_s0_s_0 = 9.89999999960267
 balance_t: - x_s0_t_2 - x_s0_t_1 - x_s0_t_0 - x_r_t_3 = -3.7

End

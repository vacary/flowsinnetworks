\* Problem: sparsestcut *\

Minimize
 obj: + q

Subject To
 capacity_sr_3: + x_sr_3 - q <= 0
 capacity_rt_3: + x_rt_3 - q <= 0
 capacity_s0s_0: + x_s0s_0 - 3.5 q <= 0
 capacity_s0r_0: + x_s0r_0 - q <= 0
 capacity_s0r_1: + x_s0r_1 - q <= 0
 capacity_s0r_2: + x_s0r_2 - q <= 0
 capacity_s0t_0: + x_s0t_0 - q <= 0
 capacity_s0t_1: + x_s0t_1 - q <= 0
 capacity_s0t_2: + x_s0t_2 - q <= 0
 balance_s: - x_s0s_0 + x_sr_3 = -2.99999999975243
 balance_r: - x_s0r_2 - x_s0r_1 - x_s0r_0 - x_sr_3 + x_rt_3
 = -2.99999999975243
 balance_s0: + x_s0t_2 + x_s0t_1 + x_s0t_0 + x_s0r_2 + x_s0r_1 + x_s0r_0
 + x_s0s_0 = 9.49999999950485
 balance_t: - x_s0t_2 - x_s0t_1 - x_s0t_0 - x_rt_3 = -3.5

End

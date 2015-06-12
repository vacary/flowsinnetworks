\* Problem: sparsestcut *\

Minimize
 obj: + q

Subject To
 capacity_v1v2_0: + x_v1v2_0 - 2 q <= 0
 capacity_v1t_0: + x_v1t_0 - 3 q <= 0
 capacity_sv2_0: + x_sv2_0 - 4 q <= 0
 capacity_s0v1_0: + x_s0v1_0 - 3 q <= 0
 capacity_s0s_0: + x_s0s_0 - 4 q <= 0
 capacity_s0t_0: + x_s0t_0 - q <= 0
 balance_v1: - x_s0v1_0 + x_v1t_0 + x_v1v2_0 = 0
 balance_s: - x_s0s_0 + x_sv2_0 = -3
 balance_s0: + x_s0t_0 + x_s0s_0 + x_s0v1_0 = 8
 balance_v2: - x_sv2_0 - x_v1v2_0 = -1
 balance_t: - x_s0t_0 - x_v1t_0 = -4

End

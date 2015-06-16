graph [
  directed 1
  node [
    id 0
    label "20.0"
    label_thin_flow_overtime "[1.0, 1.0, 1.0]"
    label_thin_flow 1.0
    nlabel "s"
    label_overtime "[0, 1.0, 2.0, 20.0]"
  ]
  node [
    id 1
    label "21.0"
    label_thin_flow_overtime "[2.0, 0.0, 1.0]"
    label_thin_flow 1.0
    nlabel "r"
    label_overtime "[1, 3.0, 3.0, 21.0]"
  ]
  node [
    id 2
    label "22.0"
    label_thin_flow_overtime "[2.0, 0.0, 1.0]"
    label_thin_flow 1.0
    nlabel "t"
    label_overtime "[2, 4.0, 4.0, 22.0]"
  ]
  edge [
    source 0
    target 1
    x_overtime "[0.0, 2.0, 2.0, 20.0]"
    F_e_minus_overtime "[0.0, 2.0, 2.0, 20.0]"
    capacity 1
    f_e_plus_overtime "[2.0, 0.0, 1.0]"
    f_e_minus_overtime "[1.0, 0.0, 1.0]"
    time 1
    flow 0
    thin_flow 1.0
    edge_key 2
    F_e_plus_overtime "[0.0, 2.0, 2.0, 20.0]"
    edge_skey 0
    x 20.0
    thin_flow_overtime "[2.0, 0.0, 1.0]"
    switching_times "[0, 0, 1.0, 2.0, 3.0, 19.0, 20.0, 20.0]"
    z_e_overtime "[0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]"
  ]
  edge [
    source 1
    target 2
    x_overtime "[0.0, 0.0, 0.0, 0.0]"
    F_e_minus_overtime "[0.0, 0.0, 0.0, 0.0]"
    capacity 1
    f_e_plus_overtime "[0.0, 0.0, 0.0]"
    f_e_minus_overtime "[0.0, 0.0, 0.0]"
    time 2
    flow 0
    thin_flow 0.0
    edge_key 0
    F_e_plus_overtime "[0.0, 0.0, 0.0, 0.0]"
    edge_skey 0
    x 0.0
    thin_flow_overtime "[0.0, 0.0, 0.0]"
    switching_times "[1, 1, 2, 3.0, 4.0, 19.0]"
    z_e_overtime "[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"
  ]
  edge [
    source 1
    target 2
    x_overtime "[0.0, 2.0, 2.0, 20.0]"
    F_e_minus_overtime "[0.0, 2.0, 2.0, 20.0]"
    capacity 1
    f_e_plus_overtime "[1.0, 0.0, 1.0]"
    f_e_minus_overtime "[1.0, 0.0, 1.0]"
    time 1
    flow 0
    thin_flow 1.0
    edge_key 1
    F_e_plus_overtime "[0.0, 2.0, 2.0, 20.0]"
    edge_skey 1
    x 20.0
    thin_flow_overtime "[2.0, 0.0, 1.0]"
    switching_times "[1, 1, 2, 3.0, 4.0, 20.0, 21.0, 21.0]"
    z_e_overtime "[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]"
  ]
]

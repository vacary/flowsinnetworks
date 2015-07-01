graph [
  directed 1
  node [
    id 0
    label "v1"
    label_thin_flow_overtime "[1.3333333333333333, 1.3333333333333333, 1.3333333333333333, 1.0, 1.0]"
    pos "[-69.230769230769226, 35.042735042735046, 0.0]"
    label_overtime "[1.0, 2.333333333333333, 3.666666666666667, 5.000000000000001, 12.0, 22.0]"
    nlabel "v1"
  ]
  node [
    id 1
    label "s"
    label_thin_flow_overtime "[1.0, 1.0, 1.0, 1.0, 1.0]"
    pos "[-100.0, 23.076923076923084, 0.0]"
    label_overtime "[0, 1.0, 2.0000000000000004, 3.000000000000001, 10.0, 20.0]"
    nlabel "s"
  ]
  node [
    id 2
    label "v2"
    label_thin_flow_overtime "[2.0, 0.6666666666666666, 1.3333333333333333, 1.0, 1.0]"
    pos "[-38.46153846153846, 11.53846153846154, 0.0]"
    label_overtime "[2.0, 4.0, 4.666666666666667, 6.000000000000001, 13.0, 23.0]"
    nlabel "v2"
  ]
  node [
    id 3
    label "t"
    label_thin_flow_overtime "[4.0, 1.3333333333333333, 1.3333333333333333, 1.0, 1.0]"
    pos "[-7.6923076923076898, 23.076923076923077, 0.0]"
    label_overtime "[3.0, 7.0, 8.333333333333334, 9.666666666666668, 16.666666666666668, 26.666666666666668]"
    nlabel "t"
  ]
  edge [
    source 0
    target 2
    edge_skey 0
    capacity 2.0
    edge_key 3
    time 1.0
  ]
  edge [
    source 0
    target 3
    edge_skey 0
    capacity 3.0
    edge_key 2
    time 4.66666666667
  ]
  edge [
    source 1
    target 0
    edge_skey 0
    capacity 3.0
    edge_key 0
    time 1.0
  ]
  edge [
    source 1
    target 2
    edge_skey 0
    capacity 4.0
    edge_key 1
    time 3.0
  ]
  edge [
    source 2
    target 3
    edge_skey 0
    capacity 1.0
    edge_key 4
    time 1.0
  ]
]

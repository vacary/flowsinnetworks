graph [
  directed 1
  node [
    id 0
    label "v1"
    label_thin_flow_overtime "[1.3333333333333333, 1.3333333333333333, 1.3333333332557231, 1.3333333332557231, 1.3333333333139308, 1.0]"
    nlabel "v1"
    label_overtime "[1.0, 1.6666666666666665, 2.333333333333333, 2.9999999999611946, 3.666666666666667, 4.999999999825378, 21.999999999883585]"
  ]
  node [
    id 1
    label "s"
    label_thin_flow_overtime "[1.0, 1.0, 0.9999999999417923, 0.9999999999417923, 0.9999999999417923, 1.0]"
    nlabel "s"
    label_overtime "[0, 0.5, 1.0, 1.4999999999708962, 2.0000000000000004, 2.999999999825378, 19.999999999883585]"
  ]
  node [
    id 2
    label "v2"
    label_thin_flow_overtime "[2.0, 2.0, 0.6666666666278616, 0.6666666666278616, 1.3333333333139308, 1.0]"
    nlabel "v2"
    label_overtime "[2.0, 3.0, 4.0, 4.333333333313931, 4.666666666666667, 5.999999999825378, 22.999999999883585]"
  ]
  node [
    id 3
    label "t"
    label_thin_flow_overtime "[4.0, 4.0, 1.3333333332557231, 1.3333333332557231, 1.3333333333139308, 1.0]"
    nlabel "t"
    label_overtime "[3.0, 5.0, 7.0, 7.666666666627862, 8.333333333333334, 9.666666666492045, 26.666666666550253]"
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

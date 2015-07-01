graph [
  directed 1
  node [
    id 0
    label "s"
    label_thin_flow_overtime "[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]"
    pos "[-100.0, 20.943209876543214, 0.0]"
    label_overtime "[0, 0.07142857142857142, 0.26108374384236455, 0.5279802955665025, 0.6701746529332736, 1.5987460815047019, 1.7847744688261926, 4.737899468826193, 5.098746081504704, 10.0, 20.0]"
    nlabel "s"
  ]
  node [
    id 1
    label "r"
    label_thin_flow_overtime "[8.0, 3.6363636363636367, 2.2222222222222223, 2.2222222222222223, 1.5384615384615385, 1.1428571428571428, 1.1428571428571428, 1.142857142857143, 1.0, 1.0]"
    pos "[-55.55555555555555, 20.943209876543211, 0.0]"
    label_overtime "[0.5, 1.0714285714285714, 1.7610837438423648, 2.3541871921182267, 2.6701746529332735, 4.098746081504702, 4.3113499527292625, 7.6863499527292625, 8.098746081504704, 13.0, 23.0]"
    nlabel "r"
  ]
  node [
    id 2
    label "t"
    label_thin_flow_overtime "[8.0, 5.0, 5.0, 2.3529411764705883, 2.3529411764705883, 2.3529411764705883, 1.4814814814814814, 1.142857142857143, 1.0526315789473684, 1.0526315789473681]"
    pos "[-11.111111111111109, 20.943209876543207, 0.0]"
    label_overtime "[1.5, 2.071428571428571, 3.019704433497537, 4.354187192118227, 4.688762150628277, 6.873636100208108, 7.3113499527292625, 11.686349952729262, 12.098746081504704, 17.257960732552384, 27.784276522026065]"
    nlabel "t"
  ]
  edge [
    source 0
    target 1
    edge_skey 0
    capacity 0.5
    edge_key 4
    time 0.5
  ]
  edge [
    source 0
    target 1
    edge_skey 1
    capacity 0.6
    edge_key 5
    time 1.0
  ]
  edge [
    source 0
    target 1
    edge_skey 2
    capacity 0.7
    edge_key 6
    time 1.5
  ]
  edge [
    source 0
    target 1
    edge_skey 3
    capacity 0.8
    edge_key 7
    time 2.0
  ]
  edge [
    source 0
    target 1
    edge_skey 4
    capacity 0.9
    edge_key 8
    time 2.5
  ]
  edge [
    source 0
    target 1
    edge_skey 5
    capacity 1.0
    edge_key 9
    time 3.0
  ]
  edge [
    source 1
    target 2
    edge_skey 0
    capacity 0.8
    edge_key 0
    time 1.0
  ]
  edge [
    source 1
    target 2
    edge_skey 1
    capacity 0.9
    edge_key 1
    time 2.0
  ]
  edge [
    source 1
    target 2
    edge_skey 2
    capacity 1.0
    edge_key 2
    time 3.0
  ]
  edge [
    source 1
    target 2
    edge_skey 3
    capacity 1.1
    edge_key 3
    time 4.0
  ]
]

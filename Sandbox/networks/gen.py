##
#
# Inria Chile - Flows In Networks
# 
# Dynamic flow visualization
#
# * Data manager
#
#

def data_generator():
    
    import os, sys
    import settings
    
    state = True
    
    try:
    
        lib_path = os.path.abspath(os.path.join('..','..'))
        sys.path.append(lib_path)
        
        import Flows.test as t
        
        
        VDATA_T_MAX     = max(settings.T_MAX,1E-12)
        VDATA_TIME_STEP = max(settings.TIME_STEP,1E-12)
        VDATA_NGRAPH    = str(settings.NETWORK_GRAPH)
    
        vpars = [True,VDATA_TIME_STEP,VDATA_T_MAX,VDATA_NGRAPH]
        
        ns = VDATA_NGRAPH
        
        if (ns == 'example_Fig1_Cominetti'):
            
            t.test13(vpars)
            
        elif (ns == 'example_Larre'):
            
            t.test15(vpars)
            
        elif (ns == 'example_doubleparallelpath'):
            
            t.test21(vpars)
        
        else:
            
            state = False
            print '[ MSG ] No data available for selected graph ( gen.py )'     

    except:
        
        state = False
        print '[ MSG ] Problem with data generator'
        print sys.exc_info()

    return state


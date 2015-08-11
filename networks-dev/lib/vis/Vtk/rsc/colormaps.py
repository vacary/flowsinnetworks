"""

Colormaps functions (test)


"""

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb_tuple = tuple(int(value[i:i+lv/3],16)/255.0 for i in range(0,lv,lv/3))
    return rgb_tuple

def getColorMap(value):
    
    if (value == 0):

        #green2orange

        colorList = "#5EC3D8,#4EC5D4,#3EC7CE,#2EC8C7,#20CABF,#19CBB6,#1CCCAC,#27CCA1,#34CC96,#43CC8A,#51CB7E,#5FCB72,#6DC965,#7BC859,#89C64C,#96C440,#A4C134,#B2BD29,#BFBA1E,#CDB515,#DAB010,#E7AB11"
        colorList = colorList.replace("#","")
        aux = colorList.split(",")
        colorMap = []
        for hexColor in aux:
            c = hex_to_rgb(hexColor)
            colorMap.append(c)

    elif (value == 1):
    
        #darkgreen2green
    
        colorList = "#23535E,#265A66,#29626E,#2B6A76,#2E727E,#317B87,#34838F,#368C97,#39949F,#3B9DA8,#3EA6B0,#40AEB8,#42B7C1,#45C0C9,#47CAD1,#4AD3DA,#4CDCE2,#4FE6EA,#51EFF2,#53F9FA" 
        colorList = colorList.replace("#","")
        aux = colorList.split(",")
        colorMap = []
        for hexColor in aux:
            c = hex_to_rgb(hexColor)
            colorMap.append(c)        
            
    elif (value == 2):

        #darkgreen2green
        
        colorList = "#246470,#266C77,#28737E,#2A7A86,#2C828D,#2F8A95,#31919D,#3299A4,#34A1AC,#36A9B3,#38B1BB,#3AB9C3,#3CC1CA,#3EC9D2,#3FD2D9,#41DAE1,#43E3E9,#45EBF0,#47F4F8,#49FCFF"
        colorList = colorList.replace("#","")
        aux = colorList.split(",")
        colorMap = []
        for hexColor in aux:
            c = hex_to_rgb(hexColor)
            colorMap.append(c)
        
    elif (value == 3):
        
        #darkgreen2green
        
        colorList = "#255566,#255A6B,#245E6F,#236373,#216877,#206D7A,#1E727E,#1C7782,#1B7C85,#198188,#17868B,#158B8E,#149091,#139593,#139B96,#15A098,#17A59A,#1AAA9C,#1DAF9E,#22B59F"
        colorList = colorList.replace("#","")
        aux = colorList.split(",")
        colorMap = []
        for hexColor in aux:
            c = hex_to_rgb(hexColor)
            colorMap.append(c)
        
    elif (value == 4):
        
        #darkgreen2green
        
        colorList = "#1D4757,#1F4C5C,#205061,#215565,#215A6A,#225E6F,#236374,#236879,#246D7E,#247283,#247788,#247C8D,#248192,#248697,#248B9C,#2491A1,#2396A5,#239BAA,#22A0AF,#21A6B4"
        colorList = colorList.replace("#","")
        aux = colorList.split(",")
        colorMap = []
        for hexColor in aux:
            c = hex_to_rgb(hexColor)
            colorMap.append(c)
        
    elif (value == 5):

        #cyan2blue

        colorList = "#00E6FF,#00DCFC,#00D2FA,#00C8F7,#00BFF5,#00B5F2,#00ABF0,#00A2EE,#0098EB,#008EE9,#0084E6,#007BE4,#0071E1,#0067DF,#005EDD,#0054DA,#004AD8,#0040D5,#0037D3,#002DD0,#0023CE,#001ACC"
        colorList = colorList.replace("#","")
        aux = colorList.split(",")
        colorMap = []
        for hexColor in aux:
            c = hex_to_rgb(hexColor)
            colorMap.append(c)
        
    elif (value == 6):
        
        # blue2cyan
        
        colorList = "#001ACC,#0024CE,#002FD0,#003AD3,#0045D5,#0050D8,#005BDA,#0066DD,#0071DF,#007CE1,#0087E4,#0091E6,#009CE9,#00A7EB,#00B2EE,#00BDF0,#00C8F2,#00D3F5,#00DEF7,#00E9FA,#00F4FC,#00FFFF"
        colorList = colorList.replace("#","")
        aux = colorList.split(",")
        colorMap = []
        for hexColor in aux:
            c = hex_to_rgb(hexColor)
            colorMap.append(c)
        
    elif (value == 7):
        
        # cyan2blue
        
        colorList = "#001ACC,#0021CD,#0028CF,#0030D0,#0037D2,#003ED4,#0046D5,#004DD7,#0055D9,#005CDA,#0063DC,#006BDE,#0072DF,#007AE1,#0081E3,#0088E4,#0090E6,#0097E7,#009EE9,#00A6EB,#00ADEC,#00B5EE,#00BCF0,#00C3F1,#00CBF3,#00D2F5,#00DAF6,#00E1F8,#00E8FA,#00F0FB,#00F7FD,#00FFFF"
        colorList = colorList.replace("#","")
        aux = colorList.split(",")
        colorMap = []
        for hexColor in aux:
            c = hex_to_rgb(hexColor)
            colorMap.append(c)
        colorMap = list(reversed(colorMap))
        
    else:
        
        #blue2red_divergent_map
        
        colorMap = []
          
        colorMap.append([0.23137254902, 0.298039215686, 0.752941176471])
        colorMap.append([0.266666666667, 0.352941176471, 0.8])
        colorMap.append([0.305882352941, 0.407843137255, 0.843137254902])
        colorMap.append([0.345098039216, 0.458823529412, 0.882352941176])
        colorMap.append([0.38431372549, 0.509803921569, 0.917647058824])
        colorMap.append([0.423529411765, 0.556862745098, 0.945098039216])
        colorMap.append([0.466666666667, 0.603921568627, 0.96862745098])
        colorMap.append([0.509803921569, 0.647058823529, 0.98431372549])
        colorMap.append([0.552941176471, 0.690196078431, 0.996078431373])
        colorMap.append([0.596078431373, 0.725490196078, 1.0])
        colorMap.append([0.639215686275, 0.760784313725, 1.0])
        colorMap.append([0.682352941176, 0.788235294118, 0.992156862745])
        colorMap.append([0.721568627451, 0.81568627451, 0.976470588235])
        colorMap.append([0.760784313725, 0.835294117647, 0.956862745098])
        colorMap.append([0.8, 0.850980392157, 0.933333333333])
        colorMap.append([0.835294117647, 0.858823529412, 0.901960784314])
        colorMap.append([0.866666666667, 0.866666666667, 0.866666666667])
        colorMap.append([0.898039215686, 0.847058823529, 0.819607843137])
        colorMap.append([0.925490196078, 0.827450980392, 0.776470588235])
        colorMap.append([0.945098039216, 0.8, 0.725490196078])
        colorMap.append([0.960784313725, 0.76862745098, 0.678431372549])
        colorMap.append([0.96862745098, 0.733333333333, 0.627450980392])
        colorMap.append([0.96862745098, 0.694117647059, 0.580392156863])
        colorMap.append([0.96862745098, 0.650980392157, 0.529411764706])
        colorMap.append([0.956862745098, 0.603921568627, 0.482352941176])
        colorMap.append([0.945098039216, 0.552941176471, 0.435294117647])
        colorMap.append([0.925490196078, 0.498039215686, 0.388235294118])
        colorMap.append([0.898039215686, 0.439215686275, 0.341176470588])
        colorMap.append([0.870588235294, 0.380392156863, 0.298039215686])
        colorMap.append([0.835294117647, 0.313725490196, 0.258823529412])
        colorMap.append([0.796078431373, 0.243137254902, 0.219607843137])
        colorMap.append([0.752941176471, 0.156862745098, 0.18431372549])
        colorMap.append([0.705882352941, 0.0156862745098, 0.149019607843])
        
    return colorMap




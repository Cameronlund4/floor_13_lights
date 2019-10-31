from FixedLightProvider import FixedLightProvider

class GradientFixedLightProvider(FixedLightProvider):
    steps = []
    startInd = 0

    def __init__(self, colors, colorIts):
        super(GradientFixedLightProvider, self).__init__(self.gradientifyColors(colors, colorIts))
        
    
    def gradient(self, percent, colorA, colorB):
        color = [0, 0, 0]
        for i in range(3):
            color[i] = int(colorA[i] + percent * (colorB[i] - colorA[i]))
        return color


    def gradientifyColors(self, colors, colorIts):
        steps = []
        colors.append(colors[0])
        print("Processing...")
        for i in range(len(colors)-1):
            for j in range(colorIts):
                perc = j/colorIts if i != 0 else 0
                steps.append(self.gradient(perc, colors[i], colors[i+1]))
        print("Done! Got", len(steps), "light instances!")
        return steps, colors

GradientFixedLightProvider([[255, 255, 255], [0, 0, 0]], 30)
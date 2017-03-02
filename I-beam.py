#
# I-beam (Structural Analysis)
# (c) Afaan Bilal ( https://afaan.ml )
#

class IBeamPart:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.elevation = 0
        self.h = 0

    def setWidth(self, width):
        self.width = width

    def setHeight(self, height):
        self.height = height

    def setElevation(self, elevation):
        self.elevation = elevation

    def setH(self, Ybar):
        self.h = Ybar - self.ybar() if Ybar > self.ybar() else self.ybar() - Ybar 

    def ybar(self):
        return self.elevation + self.height / 2

    def area(self):
        return self.width * self.height

    def I(self):
        return self.width * self.height ** 3 / 12

    def IaboutNA(self):
        return self.I() + self.area() * self.h ** 2


class IBeam:
    def __init__(self):
        self.FlangeU = IBeamPart()
        self.FlangeL = IBeamPart()
        self.Web = IBeamPart()
        self.span = 0
        self.height = 0
        self.permStressT = 0
        self.permStressC = 0
        self.appliedM = 0
        
    def inputDimensions(self):
        print("Input dimensions: ")
        w = float(input("Lower flange - width (mm): "))
        h = float(input("Lower flange - height(mm): "))
        self.FlangeL.setWidth(w)
        self.FlangeL.setHeight(h)
        w = float(input("Web          - width (mm): "))
        h = float(input("Web          - height(mm): "))
        self.Web.setWidth(w)
        self.Web.setHeight(h)
        w = float(input("Upper flange - width (mm): "))
        h = float(input("Upper flange - height(mm): "))
        self.FlangeU.setWidth(w)
        self.FlangeU.setHeight(h)
        self.span = float(input("Span length (m): "))
        self.permStressC = float(input("Permissible Stress (Compression) (N/mm2): "))
        self.permStressT = float(input("Permissible Stress (Tension)     (N/mm2): "))
        self.appliedM    = float(input("Applied bending moment            (kN-m): "))
        self.height = self.FlangeL.height + self.Web.height + self.FlangeU.height

    def ybar(self):
        return ( self.FlangeL.area() * self.FlangeL.ybar()   \
               + self.Web.area()     * self.Web.ybar()       \
               + self.FlangeU.area() * self.FlangeU.ybar() ) \
               / ( self.FlangeL.area() + self.Web.area() + self.FlangeU.area() )

    def I(self):
        self.FlangeL.setElevation(0)
        self.Web.setElevation(self.FlangeL.height)
        self.FlangeU.setElevation(self.FlangeL.height + self.Web.height)
        
        self.FlangeL.setH(self.ybar())
        self.Web.setH(self.ybar())
        self.FlangeU.setH(self.ybar())

        return self.FlangeL.IaboutNA() + self.Web.IaboutNA() + self.FlangeU.IaboutNA()

    def yMaxT(self):
        return self.ybar()

    def yMaxC(self):
        return self.height - self.ybar()

    def mMaxT(self):
        return self.permStressT * self.I() / ( self.yMaxT() * 1000 * 1000 )

    def mMaxC(self):
        return self.permStressC * self.I() / ( self.yMaxC() * 1000 * 1000 )

    def MOR(self):
        return self.mMaxT() if self.mMaxT() < self.mMaxC() else self.mMaxC()

    def maxUDL(self):
        return 8 * self.MOR() / ( ( self.span ) ** 2 )

    def maxConc(self):
        return 4 * self.MOR() / ( self.span )

    def maxTotalLoad(self):
        return self.maxUDL() * self.span

    def maxInducedStressT(self):
        return self.appliedM * 1000000 * self.yMaxT() / self.I()

    def maxInducedStressC(self):
        return self.appliedM * 1000000 * self.yMaxC() / self.I()

    def totalForceT(self):
        areaUnderTension = self.FlangeL.area() + ( self.yMaxT() - self.FlangeL.height ) * self.Web.width
        return self.maxInducedStressT() / 2 * areaUnderTension / 1000

    def totalForceC(self):
        areaUnderCompression = self.FlangeU.area() + ( self.yMaxC() - self.FlangeU.height ) * self.Web.width
        return self.maxInducedStressC() / 2 * areaUnderCompression / 1000

    def printAnalysis(self):
        print("\n--- Analysis ---")
        print("Moment of Inertia (about NA)        : %.4f mm4"   % self.I())
        print("Max Tensile Moment      (MT)        : %.4f kN-m"  % self.mMaxT())
        print("Max Compressive Moment  (MC)        : %.4f kN-m"  % self.mMaxC())
        print("Moment of Resistance   (MOR)        : %.4f kN-m"  % self.MOR())
        print("Maximum UDL across the span         : %.4f kN/m"  % self.maxUDL())
        print("Maximum total load across the span  : %.4f kN"    % self.maxTotalLoad())
        print("Maximum concentrated load at midspan: %.4f kN"    % self.maxConc())
        print("Maximum induced tensile stress      : %.4f N/mm2" % self.maxInducedStressT())
        print("Maximum induced compressive stress  : %.4f N/mm2" % self.maxInducedStressC())
        print("Total tensile force                 : %.4f kN"     % self.totalForceT())
        print("Total compressive force             : %.4f kN"     % self.totalForceC())

print("\nI-beam: Structural Analysis")
print("(c) Afaan Bilal ( https://afaan.ml )\n")
ibeam = IBeam()
ibeam.inputDimensions()
ibeam.printAnalysis()

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class fuzzynilaiakhir:
     
    def __init__(self):
        self.absen = ctrl.Antecedent(np.arange(0, 11, 1), 'absen')
        self.tugas = ctrl.Antecedent(np.arange(0, 11, 1), 'tugas')
        self.kuis = ctrl.Antecedent(np.arange(0, 11, 1), 'kuis')
        self.ujian = ctrl.Antecedent(np.arange(0, 11, 1), 'ujian')
        self.nilaiakhir = ctrl.Consequent(np.arange(0, 101, 1), 'nilaiakhir')
        
    def keanggotaaninput(self):
        self.absen.automf(3)
        self.tugas.automf(3)
        self.kuis.automf(3)
        self.ujian.automf(3)
         
    def keanggotaanoutput(self):
        self.keanggotaaninput()
        self.nilaiakhir['rendah'] = fuzz.trimf(self.nilaiakhir.universe,[0,0,60])
        self.nilaiakhir['menengah'] = fuzz.trimf(self.nilaiakhir.universe,[50,70,100])
        self.nilaiakhir['tinggi'] = fuzz.trimf(self.nilaiakhir.universe,[80,100,100])
         
    def syarat(self):
        self.keanggotaaninput()
        self.keanggotaanoutput()

        self.syarat1 = ctrl.Rule(self.ujian['good'] | self.tugas['good'], self.nilaiakhir['tinggi'])
        self.syarat2 = ctrl.Rule(self.ujian['poor'] | self.tugas['poor'], self.nilaiakhir['rendah'])
        self.syarat3 = ctrl.Rule(self.ujian['poor'] & self.kuis['good'] | self.tugas['poor'] & self.kuis['good'], self.nilaiakhir['menengah']) 
        self.syarat4 = ctrl.Rule(self.kuis['poor'] | self.absen['poor'], self.nilaiakhir['menengah'])
        
    def penilaian(self):
        self.syarat()
        sistempenilaian = ctrl.ControlSystem([self.syarat1, self.syarat2, self.syarat3, self.syarat4])
        self.penilaian = ctrl.ControlSystemSimulation(sistempenilaian)
        
        self.penilaian.input['absen'] = 2
        self.penilaian.input['tugas'] = 8
        self.penilaian.input['kuis'] = 3
        self.penilaian.input['ujian'] = 1
	
        self.penilaian.compute()
         
    def hasil(self):
        self.penilaian()
        print(self.penilaian.output['nilaiakhir'])
        self.nilaiakhir.view(sim=self.penilaian)
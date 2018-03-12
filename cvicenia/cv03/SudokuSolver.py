import os.path
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../../examples/sat')]

import sat

class SudokuSolver:
    def q(self, i,j,n):
        if (9 * 9 * i + 9 * j + n == 36):
            print(36,i,j,n)
        if (9 * 9 * i + 9 * j + n == 39):
            print(39,i,j,n)
        return 9 * 9 * i + 9 * j + n;
    
    def solve(self, pole):
        self.pole = pole
        solver = sat.SatSolver()
        w = sat.DimacsWriter('SudokuSolverIn.txt')

        # zaznamenaj, co je dane
        for i in range(9):
            for j in range(9):
                n = pole[i][j]
                if n != 0:
                    w.writeLiteral(self.q(i,j,n))
                    w.finishClause()

        # v kazdom riadku kazde cislo aspon raz
        for i in range(9):
            for n in range(1,10):
                for j in range(9):
                    w.writeLiteral(self.q(i,j,n))
                w.finishClause()

        # v kazdom stlpci kazde cislo aspon raz
        for j in range(9):
            for n in range(1,10):
                for i in range(9):
                    w.writeLiteral(self.q(i,j,n))
                w.finishClause()

        # na kazdom policku len jedno cislo
        for i in range(9):
            for j in range(9):
                for n1 in range(1,10):
                    for n2 in range(n1+1,10):
                        w.writeImpl(self.q(i,j,n1), -self.q(i,j,n2))

        # v kazdom stvorci kazde cislo aspon raz
        for i in range(9):
            for n in range(1,10):
                for j in range(9):
                    w.writeLiteral(self.q(3*(i//3)+j//3,3*(i%3)+j%3,n))
                w.finishClause()


        w.close()
        ok, sol = solver.solve(w, 'SudokuSolverOut.txt')

        ret = []
        for i in range(9):
            pomoc = []
            for j in range(9):
                pomoc.append(0)
            ret.append(pomoc)
        if ok:
            pocet = 0
            for x in sol:
                if (x > 0):
                    pocet += 1
                    if x%9 == 0:
                        x -= 9
                        ret[x//(9*9)][(x//9)%9] = 9
                    else:
                        ret[x//(9*9)][(x//9)%9] = x%9
        return ret
                    
        
        



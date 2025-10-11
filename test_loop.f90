program ising_non_square   !!da unire in uno script shell al programma python che fa l'analisi per ogni valore di beta
implicit none 

integer, parameter :: n_horiz = 2, n_vert = 2, N = 5*10**6                
integer, parameter :: rows = 4+3*(n_vert-1)+2, columns = 4+3*(n_horiz-1)+2  
integer :: i, j, iteration, rowtemp, coltemp, s
real :: beta	          !!temperatura inversa
real :: aux, acceptance, r
integer :: lattice(rows, columns) 
double precision :: totalE, totalMagn

read *, beta

print *, rows*columns, beta

lattice = 0          !!inizializzo il reticolo 
do j=1,columns
   lattice(1,j) = 0
   lattice(rows,j) = 0
enddo
do i=2,rows-1
   if (i==2 .or. mod(i-1,3)==1) then
   do j=2,columns-1 
      if (j/=2 .and. mod(j-1,3)/=1) then
      lattice(i,j) = 1
      end if
   enddo
   else 
   do j=2,columns-1
      if (j==2 .or. mod(j-1,3)==1) then
      lattice(i,j) = 1
      end if
   enddo
   end if
enddo

acceptance = 0       !!seleziono un punto casuale, posso saltare le prime e ultime righe/colonne
do iteration=1,N
   do i=2,rows-1  
      do j=2,columns-1
   2  call random_number(aux)
      coltemp = int(aux*(columns))+1
      call random_number(aux)
      rowtemp = int(aux*(rows))+1
      
      if (lattice(rowtemp, coltemp)==0) then   !!tengo solo i punti del reticolo effettivo (sicuramente lentissimo)
      goto 2
      end if
     
      s = 0         !!somma sui vicini
      
      if (rowtemp-1==1 .or. mod(rowtemp-1,3)==1) then
      s = s + lattice(rowtemp, coltemp+1)+lattice(rowtemp, coltemp-1)
      s = s + lattice(rowtemp+1, coltemp-1)+lattice(rowtemp-1, coltemp-1)
      s = s + lattice(rowtemp-1, coltemp+1)+lattice(rowtemp+1, coltemp+1)
      else
      s = s + lattice(rowtemp+1, coltemp)+lattice(rowtemp-1, coltemp)
      s = s + lattice(rowtemp+1, coltemp-1)+lattice(rowtemp-1, coltemp-1)
      s = s + lattice(rowtemp-1, coltemp+1)+lattice(rowtemp+1, coltemp+1)
      end if

      s = s*lattice(rowtemp,coltemp)
      
      
      r = 0                     !!step metropolis
      if (s < 0) then
      lattice(rowtemp,coltemp) = -lattice(rowtemp,coltemp)
      acceptance = acceptance + 1
      else 
      call random_number(r)
      if (r <= exp(-beta*2*s)) then
      lattice(rowtemp,coltemp) = -lattice(rowtemp,coltemp)
      acceptance = acceptance + 1
      end if
      end if
      enddo
   enddo
print *, totalE(lattice, rows, columns), totalMagn(lattice, rows, columns)         !!misura dopo aver iterato su tutto il reticolo
enddo 

end program ising_non_square

function totalE(lattice, rows, columns) result(E) 
implicit none
double precision :: E
integer :: i, j, rows, columns, lattice(rows,columns), temp
temp = 0
do i=2,rows-1
   do j=2,columns-1
   temp = temp - lattice(i,j)*lattice(i,j+1)
   temp = temp - lattice(i,j)*lattice(i+1,j)
   temp = temp - lattice(i,j)*lattice(i+1,j+1)
   temp = temp - lattice(i,j)*lattice(i+1,j-1)
   enddo
enddo
E = dble(temp)/dble(rows*columns)
end function totalE

function totalMagn(lattice, rows, columns) result(m) 
implicit none
double precision :: m
integer :: i, j, rows, columns, lattice(rows,columns), temp
temp = 0
do i=2,rows-1
   do j=2,columns-1
   temp = temp + lattice(i,j)
   enddo
enddo
m = dble(temp)/dble(rows*columns)
end function totalMagn










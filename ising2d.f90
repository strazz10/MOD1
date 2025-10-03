program ising2d !!da ottimizzare
implicit none 

integer, parameter :: L = 4, N = 10000
integer :: i, j, x, y, xtemp, ytemp, lattice(L,L), iteration, metropolis_ising, temp, s, state
real, parameter :: beta = 0.5
real :: totalE, totalMagn, aux, acceptance
real :: r, F1, test_function

open (unit = 20, file = 'ising.dat', status = 'unknown')

lattice = 0
do i=1,L
  do j=1,L
  lattice(i,j) = 1
  enddo
enddo

acceptance = 0
do iteration=1,N
  do x=1,L
    do y=1,L
    call random_number(aux)
    xtemp = int(aux*L)+1
    call random_number(aux)
    ytemp = int(aux*L)+1
    
    r = 0
    s = 0
    state = 0
    temp = mod(xtemp+1,L)
    if (temp == 0) then 
    temp = xtemp+1
    end if
    s = s + lattice(temp,ytemp)

    temp = xtemp-1
    if (temp < 1) then 
    temp = L
    end if
    s = s + lattice(temp,ytemp)

    temp = mod(ytemp+1,L)
    if (temp == 0) then 
    temp = ytemp+1
    end if
    s = s + lattice(xtemp,temp)

    temp = ytemp-1
    if (temp < 1) then 
    temp = L
    end if
    s = s + lattice(xtemp,temp)
    state = s*lattice(xtemp,ytemp)
   
    !!metropolis
    if (state < 0) then 
    lattice(xtemp,ytemp) = -lattice(xtemp,ytemp)
    acceptance = acceptance + 1
    else 
      call random_number(r)
      if (r <= exp(-beta*2*state)) then
      lattice(xtemp,ytemp) = -lattice(xtemp,ytemp)
      acceptance = acceptance + 1
      end if
    end if
    enddo
  enddo
  write(20,*) totalE(lattice, L), totalMagn(lattice, L) 
enddo

print *, 'acceptance=', acceptance/(N*L*L)

close(20)

end program ising2d	

function totalE(lattice, L) result(E) !per unità di v
implicit none
real :: E
integer :: x, y, lattice(L,L), L, mog, temp

temp = 0
mog = 0
do x=1,L
  do y=1,L
  mog = mod(x+1, L)
  if (mog==0) then
  mog = x+1
  end if
  temp = temp - lattice(mog,y)*lattice(x,y)
  
  mog = mod(y+1, L)
  if (mog==0) then
  mog = y+1
  end if
  temp = temp - lattice(x,mog)*lattice(x,y)
  
  enddo
enddo
E = temp/(L*L)

end function totalE

function totalMagn(lattice, L) result(m) 
implicit none
real :: m
integer :: L, x, y, lattice(L,L), tmp

tmp = 0
do x=1,L
  do y=1,L
  tmp = tmp + lattice(x,y)
  enddo
enddo
m = tmp/(L*L)

end function totalMagn




program bootstrap
implicit none
integer, parameter :: N = 10**5

real, parameter :: delta = 2 !!parametri metro
real :: state, state_temp, r, interval, F1, F2, gaussian, x_i(N)
integer :: o, acceptance
integer, parameter :: Q = 200, blocking = 100 !!parametri bootstrap, mettere blocking=100 per no blocking
integer :: i,j,l,m,b
real ::  k, s1, s2, ghost, sample, mean1, mean2, secondary_obs(Q), sum1, sum2, estimate, y_i(N/blocking)
double precision :: var

open (unit = 20, file = 'bootstrap.dat', status = 'unknown')

!!metropolis

state = 0
state_temp = 0
r = 0
interval = 0
acceptance = 0
x_i(N) = 0

call random_number(state) !stato iniziale

do o=1,n
call random_number(interval)
interval = (interval-0.5)*2*delta !intervallo simmetrico
state_temp = state + interval
  if (F1(gaussian(state_temp)/gaussian(state)) >= 1) then 
  state = state_temp
  acceptance = acceptance+1
  else 
      call random_number(r)
      if (r <= F1(gaussian(state_temp)/gaussian(state))) then
      state = state_temp
      acceptance = acceptance+1
      end if
  end if
write (20,*) o, state
x_i(o) = state
end do
close (20)
!!fine metropolis

!!bootstrap
mean1 = 0
mean2 = 0

do i=1,Q 
  s1 = 0
  s2 = 0
  do j=1,N
    call random_number(k)
    l = int(k*(N)) !!numeri interi casuali da 1 a N
    sample = x_i(l)
    s1 = s1 + sample**2 !!funzioni generiche di sample
    s2 = s2 + sample**4
  enddo
  mean1 = s1/N
  mean2 = s2/N
  secondary_obs(i) = mean2/(mean1)**2
enddo	  

sum1 = 0 !somma da quadrare
sum2 = 0 !somma dei quadrati

do i=1,Q !calcolo le somme
  sum1 = sum1 + secondary_obs(i)
  sum2 = sum2 + secondary_obs(i)**2
enddo

estimate = sum1/Q
var = (Q/(Q-1))*((sum2/Q)-((sum1)/Q)**2)

print *, 'bootstrap estimate, var for <x^4/(x^2)^2>', estimate, var 

end program bootstrap

!!!subroutines necessarie

function gaussian(x) result(y)
implicit none
real,intent(in) :: x
real :: y, mu, sigma
real,parameter :: pi = 3.14159
mu = 0
sigma = 1
y = 1/(sqrt(2*pi*sigma**2)) * exp(-((x-mu)**2)/(2*sigma**2))
end function gaussian	

function F1(x) result(y) 
implicit none
real,intent(in) :: x
real :: y
y = min(1.0,x)
end function F1



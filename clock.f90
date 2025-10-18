program clock_model
    implicit none                            !!mettendo tutto in double viene più preciso (male non ci fa, per esperienza)
    integer, parameter :: L = 16          
    integer, parameter :: N = 10**6       
    integer, parameter :: q = 4              !!parametro del modello
    integer :: i, j, step, new_state, ix, iy
    real(8) :: theta(L, L), theta_new(L, L)
    real(8) :: energy, energy_change, p_accept, magn, rand_temp
    real(8) :: beta 
                          
                          
    call random_seed()               !!inizializzo il generatore e il reticolo
    read*, beta
    call random_angles(theta)

    do step = 1, N
        do i = 1, L*L
            call random_number(rand_temp)
            ix = int(rand_temp * L) + 1     !!tra 1 e L
            iy = int(rand_temp * L) + 1  

            call random_number(rand_temp)
            new_state = int(rand_temp * q)  !! tra 0 e q-1

            energy_change = calculate_energy_change(theta, ix, iy, new_state)

            if (energy_change < 0.0) then   !!metro
                theta(ix, iy) = real(new_state, kind=8)
            else
                call random_number(rand_temp)
                if (rand_temp < exp(-energy_change * beta)) then
                    theta(ix, iy) = real(new_state, kind=8)
                    energy = energy + energy_change  
                end if
            end if
        end do

        energy = calculate_total_energy(theta)
        magn = calculate_magn(theta)

        print*, energy, magn
    end do

contains

    subroutine random_angles(theta)      !!inizializza una matrice con valori casuali da 0 a q-1
        real(8), dimension(L, L) :: theta
        real(8) :: rand_temp
        integer :: i, j
        integer, parameter :: q = 4

        do i = 1, L
            do j = 1, L
                call random_number(rand_temp)
                theta(i, j) = int(rand_temp * q)
            end do
        end do
    end subroutine random_angles

    function calculate_total_energy(theta) result(total_energy)
        real(8), dimension(L, L) :: theta
        real(8) :: total_energy
        integer :: i, j
        integer :: neighbor_x, neighbor_y
        real(8) :: diff, cos_diff
        integer, parameter :: q = 4

        total_energy = 0.0
        do i = 1, L
            do j = 1, L
                neighbor_x = mod(i, L) + 1
                neighbor_y = mod(j, L) + 1

                diff = mod(real(theta(i, j) - theta(neighbor_x, j), kind=8), real(q, kind=8))
                cos_diff = cos(2.0d0 * 3.141592653589793d0 * diff / real(q, kind=8))
                total_energy = total_energy - cos_diff
                
                diff = mod(real(theta(i, j) - theta(i, neighbor_y), kind=8), real(q, kind=8))
                cos_diff = cos(2.0d0 * 3.141592653589793d0 * diff / real(q, kind=8))
                total_energy = total_energy - cos_diff
            end do
        end do
    end function calculate_total_energy

    function calculate_energy_change(theta, ix, iy, new_state) result(energy_change)  !!funzione per il dE
        real(8), dimension(L, L) :: theta
        integer :: ix, iy, new_state
        real(8) :: energy_change
        real(8) :: diff, cos_diff
        integer :: neighbor_x, neighbor_y
        integer, parameter :: q = 4


        energy_change = 0.0

        neighbor_x = mod(ix, L) + 1
        neighbor_y = mod(iy, L) + 1

        diff = mod(real(new_state - theta(neighbor_x, iy), kind=8), real(q, kind=8))
        cos_diff = cos(2.0d0 * 3.141592653589793d0 * diff / real(q, kind=8))
        energy_change = energy_change + cos_diff - cos(2.0d0 * 3.141592653589793d0 * & 
        mod(real(theta(ix, iy) - theta(neighbor_x, iy), kind=8), real(q, kind=8)) / real(q, kind=8))

        diff = mod(real(new_state - theta(ix, neighbor_y), kind=8), real(q, kind=8))
        cos_diff = cos(2.0d0 * 3.141592653589793d0 * diff / real(q, kind=8))
        energy_change = energy_change + cos_diff - cos(2.0d0 * 3.141592653589793d0 * & 
        mod(real(theta(ix, iy) - theta(ix, neighbor_y), kind=8), real(q, kind=8)) / real(q, kind=8))
    end function calculate_energy_change

    function calculate_magn(theta) result(mag)
        real(8), dimension(L, L) :: theta
        real(8) :: mag
        integer :: i, j
        integer, parameter :: q = 4

        mag = 0.0
        do i = 1, L
            do j = 1, L
                mag = mag + & 
                cos(2.0d0 * 3.141592653589793d0 * real(theta(i, j), kind=8) / real(q, kind=8))
            end do
        end do
        mag = mag / (L * L)
    end function calculate_magn

end program clock_model

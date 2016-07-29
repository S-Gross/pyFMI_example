import os as O
import pyfmi as fmi
import matplotlib.pyplot as plt

__author__ = "sgross"


def run_simulation(t_start, t_stop, micro_t_step, macro_t_step, sim_tolerance, fmu_name):
    # Time variable for the simulation
    current_simulation_time = t_start

    # This list contains the simulation outputs stored always after one macro step
    simulation_result = []

    # Build path to the FMU model
    curr_dir = O.path.dirname(O.path.abspath(__file__))
    path_to_fmus = O.path.join(curr_dir)
    path_to_fmu = O.path.join(path_to_fmus, fmu_name)

    # load FMU
    model = fmi.load_fmu(path_to_fmu)

    # initialize model
    model.setup_experiment(start_time=t_start, stop_time=t_stop, tolerance=sim_tolerance)
    model.initialize()

    # Set simulation parameters here
    # model.set([Parameter Name], [Parameter value])    # Example

    # Enter the simulation loop
    while current_simulation_time < t_stop:
        print()
        # Set simulation inputs for next step
        # model.set([Variable Name], [Variable value])    # Example

        for i in range(int(macro_t_step/micro_t_step)):
            model.do_step(current_t=current_simulation_time + i*micro_t_step, step_size=micro_t_step, new_step=True)

        # Get simulation output after
        model_value_reference = model.get_variable_valueref("y")
        model_output = model.get_real(model_value_reference)

        # Store model output in simulation result list
        simulation_result.append(model_output[0])

        # Increase current time
        current_simulation_time = current_simulation_time + macro_t_step

    # return the results for the given FMU
    return simulation_result


if __name__ == '__main__':

    # Simulation Parameter
    t_start = 0          # Start time of simulation
    t_stop = 10        # Stop time of simulation
    micro_t_step = 0.01     # Step wide of fixed step solver
    macro_t_step = 0.1    # Output results after macro_t_step
    sim_tolerance = 0.1  # rel. Tolerance of the simulation

    # Name of FMU to execute
    fmu_name = "Integrator_cs_20.fmu"

    res = run_simulation(t_start, t_stop, micro_t_step, macro_t_step, sim_tolerance, fmu_name)
    print(res)

    plt.plot(res)
    plt.show()

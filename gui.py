import PySimpleGUI as sg
from random import randint
from forest_fire import sim_with_grid, fast_simulation

sg.ChangeLookAndFeel('Dark')

main_layout = [
    [sg.Text('Grid size', size=(15, 1)), sg.InputText('25')],
    [sg.Text('Number of fire start points', size=(15, 1)), sg.InputText('1')],
    [sg.Text('Percolation coefficient (for PyGame simulation only)', size=(15, 1)), sg.InputText('0.5')],
    [sg.Checkbox('Fast Simulation (no PyGame animations)')],
    [sg.Text('Number of epochs (for fast simulation only)', size=(15, 1)), sg.InputText('1')],
    [sg.Submit()]
]


main_window = sg.Window('Forest Fire Simulator').Layout(main_layout)
button, values = main_window.Read()

if values[3] == True:
    fast_simulation(epochs=values[4], nb_fires=values[1], size=values[0])
else:
    sim_with_grid(size=values[0], nb_fires=values[1], perco=values[2])



result_layout = [
    [sg.Text('Results', justification='center', font='Helvetica 20', auto_size_text=True)],
    [sg.Text('Mean tree density left: '), sg.Text(str(population.current_gen+1))],
    [sg.Text('Mean time to propagate from left to right: '), sg.Text(str(strong))],
    [sg.Text('Mean number of steps to complete: '), sg.Text(str(weak))],
    [sg.Text('Detected percolation threshold: '),  sg.Text()]
    [sg.CloseButton(button_text='Close')]
]

result_window = sg.Window('Results').Layout(result_layout)

button, values = result_window.Read()

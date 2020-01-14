import PySimpleGUI as sg
from random import randint
from forest_fire import simulate, plot_result

sg.ChangeLookAndFeel('Dark')

main_layout = [
    [sg.Text('Grid size', size=(15, 1)), sg.InputText('25')],
    [sg.Text('Number of fire start points', size=(15, 1)), sg.InputText('1')],
    [sg.Text('Percolation coefficient (for PyGame simulation only)', size=(15, 1)), sg.InputText('0.5')],
    [sg.Checkbox('Fast Simulation (no PyGame animations)')],
    [sg.Text('Number of epochs (for fast simulation only)', size=(15, 1)), sg.InputText('1')],
    [sg.Text('Percolation delta (for fast simulation only)', size=(15, 1)), sg.InputText('1')],
    [sg.Submit()]
]


main_window = sg.Window('Forest Fire Simulator').Layout(main_layout)
button, values = main_window.Read()

if values[3]:
    results = simulate(epochs=int(values[4]), nb_fires=int(values[1]), size=int(values[0]), p_start=0, p_max=1, delta=float(values[5]), graphical_rendering=False)
else:
    results = simulate(nb_fires=int(values[1]), size=int(values[0]), p_start=float(values[2]), p_max=float(values[2])+1, delta=1)



result_layout = [
    [sg.Text('Results', justification='center', font='Helvetica 20', auto_size_text=True)],
    [sg.Text('Mean tree density left: '), sg.Text(str(results["mean_tree_left"]))],
    [sg.Text('Mean number of steps to complete: '), sg.Text(str(results["steps"]))],
    [sg.Text('Detected percolation threshold: '),  sg.Text(str(results["perco_threshold"]))],
    [sg.CloseButton(button_text='Close')]
]

result_window = sg.Window('Results').Layout(result_layout)

plot_result(results)

button, values = result_window.Read()

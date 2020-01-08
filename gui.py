import PySimpleGUI as sg
from random import randint
from forest_fire import sim_with_grid, fast_simulation

sg.ChangeLookAndFeel('Dark')

main_layout = [
    [sg.Text('Grid size', size=(15, 1)), sg.InputText('25')],
    [sg.Text('Number of fire start points', size=(15, 1)), sg.InputText('1')],
    [sg.Text('Percolation coefficient', size=(15, 1)), sg.InputText('0.5')],
    [sg.Checkbox('Fast Simulation (no PyGame animations)')],
    [sg.Text('Number of epochs (for fast simulation only)', size=(15, 1)), sg.InputText('1')],
    [sg.Submit()]
]


main_window = sg.Window('Genetic Knapsack').Layout(main_layout)
button, values = main_window.Read()

if values[3] == True:
    
else:
    



strong, weak = population.get_results()

result_layout = [
    [sg.Text('Results', justification='center', font='Helvetica 20', auto_size_text=True)],
    [sg.Text('Number of generations: '), sg.Text(str(population.current_gen+1))],
    [sg.Text('Strongest child: ', text_color='green'), sg.Text(str(strong))],
    [sg.Text('Weakest child: ', text_color='red'), sg.Text(str(weak))],
    [sg.CloseButton(button_text='Close')]
]

result_window = sg.Window('Results').Layout(result_layout)

button, values = result_window.Read()

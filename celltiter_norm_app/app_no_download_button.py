# celltiter-glo shiny app 

# packages and libraries to import
from shiny import *
from shiny.types import FileInfo
from io import StringIO
from htmltools import HTML
from shiny.ui import tags, h2

import pandas as pd
import numpy as np
import subprocess
import re
import random # only for test calcs
import asyncio
import os
from datetime import date
import io
from typing import Any

from pathlib import Path
from shiny import App, ui, render, reactive, Inputs, Outputs, Session
import pandas as pd
from pandas import read_csv
      


# ui section
app_ui = ui.page_fluid(

    # add navigation tabs
    ui.navset_tab(
        ui.nav('CellTiter-Glo', #'Calculate volumes Laemmli buffer based on CTG values'),
    #)

            # Describe purpose of app
            ui.panel_title('Calculate volume of Laemmli buffer needed to resuspend cell pellets'),

            # add input controls to a sidebar
            ui.layout_sidebar(
                ui.panel_sidebar(

                    # have user upload files as inputs
                    # user input ctg file
                    ui.input_file(id = 'plate',
                        label = 'CellTiter-Glo file',
                        placeholder = 'Select CellTiter-Glo file'),

                    # user presses button to calculate outputs
                    ui.input_action_button(id = 'call_me',
                        label = 'Calculate!',
                        class_= 'btn-success'),
                    ui.br(),
                    ui.br(),
                    # have user input volume of media per aliquot
                    # default = 1000 (ul) but can select anywhere
                    # between 100 and 1000 ul, not more 
                    ui.input_slider('sample_vol', 'Sample volume (µl)', min = 0, max = 1000, step = 50, value = 1000, sep = ''),
                        
            ui.br(),
            ui.input_numeric('some_value', 'µl 4X Laemmli buffer', 0),
            ui.input_numeric('some_value_1', 'µl H2O', 0),
            ui.input_numeric('some_value_2', 'Master mix volume', 0),
            
            #ui.download_button('download', 'Download .csv'),

                  ),

            # output(s)
            ui.panel_main(
                ui.output_table('calc_volumes'), 
            
            )
          )

    # new navtab? could combine this with the checkInserts app


    )#**
  )
)

# server section
def server(input, output, session):

    #set up checkInserts to run in response to clicking "Compare"
    #and to render a table as output
    @output
    @render.table(index=True)
    @reactive.event(input.call_me)
    #run checkInserts subprocess, return stdout
    def calc_volumes():

        # convert oligo file path into string input for checkInserts
        f: list[FileInfo] = input.plate()
        plate = f[0]['datapath']        
        sample_vol = str(input.sample_vol())
        # run checkInserts on the user inputs
        res = subprocess.run(['python', 'celltiter_shiny.py', plate, '-v1', sample_vol], text=True, capture_output=True)
        so = res.stdout
        # format as an 8x12 table
        so = re.sub(' +', ',', so).split('\n')
        result = []
        for element in so:
            element = element.lstrip(',').split(',')
            result.append(element)
        result = result[0:8]
        result = pd.DataFrame(result, 
            columns = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            index = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
        return result
        
    # @session.download(filename='test_download.csv')
    # def download():
        # yield calc_volumes().to_cv()
           
    @reactive.Effect
    @reactive.event(input.call_me)
    def some_value():
        # convert oligo file path into string input for checkInserts
        f: list[FileInfo] = input.plate()
        plate = f[0]['datapath']        

        # run checkInserts on the user inputs
        sample_vol = str(input.sample_vol())
        res = subprocess.run(['python', 'celltiter_shiny.py', plate, '-v1', sample_vol], text=True, capture_output=True)
        so = res.stdout
        
        # get the sum of all numbers
        so = re.sub('\s+', ',', so).lstrip(',').rstrip(',').split(',')
        summation = 0
        for item in so:
            item = int(item)
            summation = summation + item
        total_vol = summation * 1.2
        laemmli_vol = total_vol / 4
        water_vol = laemmli_vol * 3
        # set value of val reactive as sum
#        val.set(newVal)
        ui.update_numeric('some_value', value = laemmli_vol)
        ui.update_numeric('some_value_1', value = water_vol)
        ui.update_numeric('some_value_2', value = total_vol)
    
#
# call app
app = App(app_ui, server)
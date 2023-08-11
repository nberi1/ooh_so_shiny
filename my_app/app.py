# reverse-complement a string of nucleotides

# packages and libraries to import
from shiny import *
from shiny.types import FileInfo
from io import StringIO
from htmltools import HTML

import pandas as pd
import numpy as np
import subprocess
import re

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('query')
args = parser.parse_args()

# ui section
app_ui = ui.page_fluid(

    # add navigation tabs
    ui.navset_tab(
        ui.nav('Reverse complement', #'Calculate volumes Laemmli buffer based on CTG values'),
    #)

            # Describe purpose of app
            ui.panel_title('Get the reverse complement of a sequence'),

            # add input controls to a sidebar
            ui.layout_sidebar(
                ui.panel_sidebar(

                    # have user upload files as inputs
                    # user input ctg file
                    ui.input_text(id = 'query',
                        label = 'Input sequence',
                        placeholder = 'ATCG'),
                        
                    # have user upload files as inputs
                    # user input ctg file
                    ui.input_text(id = 'revcom',
                        label = 'Reverse complement',
                        placeholder = 'CGAT'),

                    # user presses button to calculate outputs
                    ui.input_action_button(id = 'call_me',
                        label = 'Get revcom',
                        class_= 'btn-success'),
                        
                  ),

                # output(s)
                ui.panel_main(
                    # ui.output_text_verbatim('get_revcom'),
                    # ui.output_text_verbatim('return_input_string'),
                
            )
          )
    )#**
  )
)
        
def server(input, output, session):

    #all this needs to do is update the text in the revcom text box
    @reactive.Effect
    @reactive.event(input.call_me)    
    
    # this function gets the revcom of the input sequence :)
    def get_revcom():

        #make dict of nucleotide pairs
        my_dict = {
        'A':'T', 'a':'t', 'T':'A', 't':'a', 'C':'G', 'c':'g', 'G':'C', 'g':'c'
        }

        # declare objects query, comp_seq (complementary sequence), comp_list (list of chars in the sequence)
        query = str(input.query())
        comp_seq = ''
        comp_list = []

        # get complement of each nucleotide
        for i in query:
            res = [val for key, val in my_dict.items() if i in key]
            comp_seq += ''.join(res)

        # reverse the complementary sequence
        revcom = ''.join(reversed(comp_seq))
        
        ui.update_text('revcom', value = revcom)     
        
#
# call app
app = App(app_ui, server)
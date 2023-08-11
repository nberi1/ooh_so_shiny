# test shiny for python app

# packages and libraries to import 
from shiny import *
from shiny.types import FileInfo
from io import StringIO
from htmltools import HTML
from simple_colors import *

import numpy as np
import pandas as pd
import re
import subprocess

# not using currently - want to have the optoi nfor the user to check their target sequence for a text string that tehy input manually 
# choices = ['Type in sequence', 'Upload file']

# ui section
app_ui = ui.page_fluid(

    # add navigation tabs
    ui.navset_tab(
        ui.nav('checkInserts', #'Check any sequence for an insert'),
    #)

        # Describe purpose of app
        ui.panel_title('Check any sequence for an insert'),

    # add input controls to a sidebar
    ui.layout_sidebar(
        ui.panel_sidebar(

            # user input sequence file(s)
            ui.input_file('sequence', 'Input sequence(s)', 
                placeholder = 'Select .seq file(s)', 
                multiple = True),
            
            # type of oligos input as file or manually antered
            # to be chosen on server seide
            # based on switch True False status 
            # default is False, ie File input
            # can switch to True, ie type in your sequence as iput
            # switch between choose file or manual oligos input
            ui.input_switch('manual', 'Input oligos manually', False),
            ui.output_ui('insert_manual_entry'),
           
           # user presses button to check the sequence for the oligo insert
            ui.input_action_button(id = 'call_me', 
                label = 'Compare',
                class_= 'btn-success'),

          ),

    # output(s)
    ui.panel_main(
        ui.output_table('check', style = 'font-family: Courier,courier; font-size:100%'),

        )
      )
    )
  )
)

# server section
def server(input, output, session):

    @output 
    @render.ui
    @reactive.event(input.manual)
    def insert_manual_entry():
        is_input_manual = input.manual()
        if is_input_manual:
            return ui.TagList(
                ui.input_text('oligo_name', 'Oligo name: '),
                ui.input_text('fwd_seq', 'FWD sequence: '),
                ui.input_text('rev_seq', 'REV sequence: '),
            )
        else:
            return ui.TagList(
            # user input oligos file
            ui.input_file('oligos', 
                label = 'Input oligo(s)', 
                placeholder = 'Select oligos (.csv) file'
                )     

            )


    #def make_reverse_complement():



    # update the revcom as user types in fwd seq
    @reactive.Effect
    def _():
        fwd = str(input.fwd_seq())
                # make revcom of input oligo seq
        #make dict of nucleotide pairs
        myDict = {
        'A':'T', 'T':'A', 'C':'G', 'G':'C'
        }

        # declare objects query, comp_seq, comp_list
        query = str(input.fwd_seq())
        comp_seq = ''
        comp_list = []

        # get complement of each nucleotide
        for i in query:
            res = [val for key, val in myDict.items() if i in key]
            comp_seq += ''.join(res)

        # reverse the complementary sequence
        revcom = ''.join(reversed(comp_seq))

        #print query and revcom sequences 
        #print("FWD:", query, "\nREV:", revcom)
        
        ui.update_text('rev_seq', value = revcom)

    # set up checkInserts to run in response to clicking "Compare"
    # and to render a table as output
    @output
    @render.table
    @reactive.event(input.call_me)   
    # run checkInserts subprocess, return stdout
    def check():

        # manual input toggle yes no 
        entry_is_manual = input.manual()  
        my_oligos = ''
        
        # # get plasmid or sequence file input 
        file_infos = input.sequence()
        file_info = file_infos[0]
        file_path = str(file_info['datapath'])

        # work out how to use manual oligos entry
        if entry_is_manual:
            oligo_entry_method = 'Manual'
            name = str(input.oligo_name())
            fwd = str(input.fwd_seq())
            rev = str(input.rev_seq())
            #rev = make_reverse_complement()
            my_oligos = name + ',' + fwd + ',' + rev
        
        # enter oligos as a file
        else:
            oligo_entry_method = 'File'
            f: list[FileInfo] = input.oligos()
            my_oligos = f[0]['datapath']
            # return f

        #return(my_oligos)

        # # run checkInserts on the user inputs, getting the stdout as the return value and assign it to result
        result = subprocess.run(['python', 'checkInserts_shiny.py', file_path, my_oligos, oligo_entry_method], text = True, capture_output = True)

        #return result
        #organize the result into a data frame
        so = result.stdout
        so = so.lstrip('[\'').rstrip('\n\']').split(',')
        # return result
        oligo_name = so[0]
        oligo_seq = so[1]
        target_id = so[2]
        target_seq = so[3]
     
        #print(oligo_name, oligo_seq, target_id, target_seq)
        # form those information pieces into a sentence that will be the title of the table
        if oligo_name == 'No match was found':
            oligo_found_statement = 'No match was found'
        else:
            oligo_found_statement = 'Oligo ' + oligo_name + ' was found in sequence ' + target_id
        title = str(oligo_found_statement)
        # split that sequence into sections of 100 characters
        split_target_seq = [target_seq[i:i+100] for i in range(0, len(target_seq), 100)]        
        # full output list
        full_output_seq = []
        # append split_target_seq to full output
        for substring in split_target_seq:
            # if '\\' in substring:
                # substring = re.sub('\\.*', '', substring)
            # else:
                # substring = substring
            full_output_seq.append(substring)
        # make and return df of results  
        out_df = pd.DataFrame(full_output_seq, columns = [title])
        return out_df


# call app
app = App(app_ui, server)


# note, the current issue is I'm not sure how input.oligo_name and the seqs are 
# getting inputted into the subprocess 
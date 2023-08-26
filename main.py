from components.scroll_label import ScrollLabel
from utils.stormpy_util import StormpyUtil

import os
import sys
import json
import ast
import re

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from views.model_specification_plotter_window import ModelSpecificationPlotterWindow
from views.model_verification_plotter_window import ModelVerificationPlotterWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.stormpyUtil = StormpyUtil()
        self.stormpyUtil.copy_stormpy_driver_to_docker()
        
        # Variables
        self.model_specification_filepath = ""
        self.data_model = []
        
        # Build main window structure
        self.setWindowTitle("CloudChecker")
        self.setWindowTitle('PyQt File Dialog')
        self.setGeometry(100, 100, 400, 100)

        # Add layout for adding widgets inside main window
        layout = QVBoxLayout()

        # Add text label notify user to insert model specification
        label_model_specification = QLabel('Select model specifications that you want to verify:')
        layout.addWidget(label_model_specification)
        
        # Add line edit so that path of selected model specification file is shown here
        self.model_specification_filepath_line_edit = QLineEdit()
        layout.addWidget(self.model_specification_filepath_line_edit)
        
        # Add button in order for user to browse and pick model specification file
        model_specification_file_browse = QPushButton('Browse')
        model_specification_file_browse.clicked.connect(self.open_file_dialog)
        # model_specification_file_browse.clicked.connect(self.hide_vis_btn)
        layout.addWidget(model_specification_file_browse)
        
        # Add button to verify and visualize model specification - only shown after model spec file is choosen
        self.hide_visualize_btn = False
        self.visualize_model_button = QPushButton('Visualize Model')
        self.visualize_model_button.clicked.connect(self.open_plot_window)
        self.visualize_model_button.hide()
        layout.addWidget(self.visualize_model_button)
        
        # Add text label notify user to insert constant variables
        label_constant_variables = QLabel('Initialize constant variables (if any) :')
        layout.addWidget(label_constant_variables)        

        # Add line edit for user to enter constant variables
        self.constant_variables_line_edit = QLineEdit()
        layout.addWidget(self.constant_variables_line_edit)
        
        # Add text label notify user to insert properties specification
        label_properties_specification = QLabel('Specify properties that you want your model to verify with :')
        layout.addWidget(label_properties_specification)

        # Add line edit for user to enter properties specification
        self.properties_edit = QLineEdit()
        layout.addWidget(self.properties_edit)

        # Add scroll label to show verification output
        self.label = ScrollLabel(self)
        self.label.setText("No model has been check")      
        layout.addWidget(self.label)       
        
        # Add button for user to verify model specification based on properties
        model_check = QPushButton('Verify Model')
        model_check.clicked.connect(self.verification_process)
        # model_check.clicked.connect(self.hide_verify_vis_btn)
        layout.addWidget(model_check)

        # Add button to visualize verification model
        self.hide_verify_visualize_btn = False
        self.verify_visualize_model_button = QPushButton('Visualize Model Verification')
        self.verify_visualize_model_button.clicked.connect(self.open_verify_window)
        self.verify_visualize_model_button.hide()
        layout.addWidget(self.verify_visualize_model_button)

        # Create container and set the layout for container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container) # Set the central widget of the Window.
    
    # def hide_vis_btn(self):
    #     if self.hide_visualize_btn:
    #         self.visualize_model_button.show()
    #         self.hide_visualize_btn = False
    #     else:
    #         self.visualize_model_button.hide()
    #         self.hide_visualize_btn = True

    # def hide_verify_vis_btn(self):
    #     if self.hide_verify_visualize_btn:
    #         self.verify_visualize_model_button.show()
    #         self.hide_verify_visualize_btn = False
    #     else:
    #         self.verify_visualize_model_button.hide()
    #         self.hide_verify_visualize_btn = True

    def open_file_dialog(self):
        
        root_path = os.path.abspath(".")
        
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            root_path
        )         
        
        if filename:
            self.model_specification_filepath = str(os.path.abspath(filename))
            self.model_specification_filepath_line_edit.setText(self.model_specification_filepath)
            
            if self.model_specification_filepath != "":
                self.visualize_model_button.show()
            else:
                self.visualize_model_button.hide()
    
    def create_model_inputs_file(self, model_specification_file_path, constant_variables="", properties_specification=""):
        model_inputs = {
            "model_specification":  os.path.basename(model_specification_file_path),
            "constant_variables": constant_variables,
            "properties_specification": properties_specification
        }
        
        json_model_input_files = json.dumps(model_inputs, indent=4)
        
        model_inputs_path = os.path.abspath("docker/model_inputs.json")
        
        with open(model_inputs_path , "w") as outfile:
            outfile.write(json_model_input_files)
        
        input_files = [
            model_specification_file_path,
            model_inputs_path
        ]
        
        return input_files
    
    def verification_process(self):
        
        model_specification_file_path = self.model_specification_filepath
        constant_variables = self.constant_variables_line_edit.text().strip()
        properties_specification = self.properties_edit.text().strip()
        
        if model_specification_file_path != "" and properties_specification != "":
            
            model_inputs = self.create_model_inputs_file(model_specification_file_path, constant_variables, properties_specification)
            
            output = self.stormpyUtil.verify_model(model_inputs)
            
            self.label.setText(output)
            
            self.verify_visualize_model_button.show()
            

    def open_plot_window(self):
        
        model_specification_file_path = self.model_specification_filepath
        constant_variables = self.constant_variables_line_edit.text().strip()
        
        if model_specification_file_path != "":
        
            model_inputs = self.create_model_inputs_file(model_specification_file_path, constant_variables)     

            data_model_str = self.stormpyUtil.get_model_info(model_inputs)

            data_model_dict = ast.literal_eval(data_model_str)     

            self.data_model = data_model_dict

            print(self.data_model)

            self.plot_window = ModelSpecificationPlotterWindow(self.data_model)
            
            self.plot_window.show()


    def open_verify_window(self):
        
        model_specification_file_path = self.model_specification_filepath
        properties_specification = self.properties_edit.text().strip()
        constant_variables = self.constant_variables_line_edit.text().strip()
                
        print("m: ", model_specification_file_path, 
              "p: ", properties_specification)
        
        
        
        if properties_specification != "" and model_specification_file_path != "":
            
            model_inputs = self.create_model_inputs_file(model_specification_file_path, constant_variables, properties_specification)
            
            verification_process_str = self.stormpyUtil.check_model3(model_inputs)

            print(verification_process_str)
            
            max_value = str(max([int(s) for s in re.findall(r'\b\d+\b', verification_process_str)]))
            
            verification_process_str = verification_process_str.replace("inf", max_value)
            
            print(verification_process_str)
            
            verification_process_list = ast.literal_eval(verification_process_str) 

            self.verify_result_list = verification_process_list

            print(type(self.verify_result_list))
            
            print(self.verify_result_list)
            
            self.verify_window = ModelVerificationPlotterWindow(self.verify_result_list)
            self.verify_window.show()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()


# Pmax=? [ F ("stop")&(lat>=maxLat) ]

# Pmin=? [ F ("stop"&lat>=maxLat) ]

# R{"lat_violation_underProvision"}max=? [ F ("stop") ]

# R{"lat_violation_underProvision"}min=? [ F ("stop") ]

# R{"lat_violation_overProvision"}max=? [ F ("stop") ]

# R{"lat_violation_overProvision"}min=? [ F ("stop") ]

# R{"cum_reward"}max=? [ F ("stop") ]

# R{"cum_reward"}min=? [ F ("stop") ]

# R{"final_vm1"}max=? [ C<=1000 ]

# R{"final_vm2"}max=? [ C<=1000 ]

# R{"lat_violation_underProvision"}max=? [ C<=1000 ]

# R{"lat_violation_underProvision"}min=? [ C<=1000 ]

# R{"lat_violation_overProvision"}max=? [ C<=1000 ]

# R{"lat_violation_overProvision"}min=? [ C<=1000 ]

# R{"final_vm"}max=?[ F ("stop") ]

# Rmin=? [F "found"]

# minVm=5,i_vm=5,maxVm=30,maxLat=30
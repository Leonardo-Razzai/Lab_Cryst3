import numpy as np

init_string_list = [
    ("INIT", "", ""),
    ("Trigger = Off","", "(0)"),
    ("Trigger CCD = Off","", "(1)"),
    ("MOT B Field = Off","", "(14)"),
    ("Ref Rep Freq = 10000000.0 Hz","", "(30)"),
    ("Ref Cool Freq = 10000000.0 Hz","", "(32)"),
    ("ENDINIT", "", "\n")
]

MOT_DURATION = 5
mot_string_list = [
    ("+1us", "Ref Cool Freq = 10000000.0 Hz", "(32)"),
    ("+1us", "AOM MOT Amp = [700]", "(41)"),
    ("+1s", "MOT B Field = On", "(14)"),
    (f"+{MOT_DURATION:.1f}s", "MOT B Field = Off", "(14)"),
    ("+1us", "AOM MOT Amp = [0]", "(41)")
]

end_cycle_string_list = [
    ("+1us", "AOM MOT Amp = [700]", "(41)"),
    ("+20ms", "Ref Cool Freq = 10000000.0 Hz", "(32)")
]

def print_string(string_list, file):
    
    first_pos = 30
    second_pos = first_pos + 30
    
    for item in string_list:
        file.write(f"{item[0]:<{first_pos}} {item[1]:<{second_pos}} {item[2]}\n")
        

def get_photo_string_list(tof: float)-> str:
    if tof < 0:
        raise ValueError("Time of flight must be greater than 0")
    if tof > 100:
        raise ValueError("Time of flight must be less than 100")
    
    tof_string_list = [
    ("+100us", "Ref Cool Freq = 9886000.0 Hz", "(32)"),
    (f"+{tof:.1f}ms", "Trigger CCD = On", "(1)"),
    ("+1us", "AOM MOT Amp = [700]", "(41)"),
    ("+1ms", "AOM MOT Amp = [0]", "(41)"),
    ("+5ms", "Trigger CCD = Off", "(1)")
    ]
    
    return tof_string_list

def print_routine_tof_imaging(tof: float, file_name= 'tof_imaging')-> str:

    with open(f"{file_name}.mot", "w") as file:
        file.write("")
        file.write("LOOP\n\n")
        
        # initialization
        print_string(init_string_list, file)
        
        file.write("INNER\n")
        # MOT phase
        print_string(mot_string_list, file)
        
        # TOF and photo phase
        tof_string_list = get_photo_string_list(tof)
        print_string(tof_string_list, file)
        
        # End cycle
        print_string(end_cycle_string_list, file)
        file.write("ENDINNER\n")
        
        file.write("\nITERATIONS 1\n")
        file.write("\nENDLOOP")
        

if __name__ == "__main__":
    print_routine_tof_imaging(tof = 10)
  
    
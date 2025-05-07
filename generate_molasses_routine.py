from generate_mot_routine import print_string, get_photo_string_list

init_string_list = [
    ("INIT", "", ""),
    ("Trigger = Off","", "(0)"),
    ("Trigger CCD = Off","", "(1)"),
    ("MOT B Field = Off","", "(14)"),
    ("Coils X Current = 0.0 A","", "(20)"),
    ("Coils Y Current = 0.0 A","", "(21)"),
    ("Coils Z Current = 0.0 A","", "(22)"),
    ("Ref Rep Freq = 10000000.0 Hz","", "(30)"),
    ("Ref Cool Freq = 10000000.0 Hz","", "(32)"),
    ("ENDINIT", "", "\n")
]

MOT_DURATION = 5 # seconds
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

REF_FREQ = 10e6 # Hz (ref freq cooler lock for mot loading)
GAMMA = 5.89 # MHz
MOT_BN = 1140 # MHz
Delta_Det_MOLASSES = 2 * GAMMA # MHz
MOLASSES_DDS_FREQ = (1 + Delta_Det_MOLASSES / MOT_BN) * REF_FREQ # Hz

def get_molasses_string_list(t_molasses = 10.0, Shim_x_current= 0.0, Shim_y_current= 0.0, Shim_z_current= 0.0)-> str:
    
    if t_molasses < 0 or t_molasses > 100:
        raise ValueError("Time of flight must be between 0 and 100 ms")
    
    if Shim_x_current < 0 or Shim_x_current > 2:
        raise ValueError("Shim_x must be between 0 and 2 A")
    if Shim_y_current < 0 or Shim_y_current > 2:
        raise ValueError("Shim_y must be between 0 and 2 A")
    if Shim_z_current < 0 or Shim_z_current > 2:
        raise ValueError("Shim_z must be between 0 and 2 A")
    
    molasses_string_list = [
    ("+1.5ms", f"Coils X Current = {Shim_x_current:.2f} A", "(20)"),
    ("+1us", f"Coils Y Current = {Shim_y_current:.2f} A", "(21)"),
    ("+1us", f"Coils Z Current = {Shim_z_current:.2f} A", "(22)"),
    ("+0.5ms", f"Ref Cool Freq = {MOLASSES_DDS_FREQ:.1f} Hz", "(32)"),
    ("+1us", "AOM MOT Amp = [700]", "(41)"),
    (f"+{t_molasses:.1f}ms", "AOM MOT Amp = [0]", "(41)"),
    ]
    
    return molasses_string_list
        
def print_routine_molasses(t_molasses: float, Shim_x_current = 0.0, Shim_y_current = 0.0, Shim_z_current = 0.0, file_name= 'molasses')-> str:

    with open(f"{file_name}.mot", "w") as file:
        file.write("")
        file.write("LOOP\n\n")
        
        # initialization
        print_string(init_string_list, file)
        
        file.write("INNER\n")
        # MOT phase
        print_string(mot_string_list, file)
        # Molasses phase
        molasses_string_list = get_molasses_string_list(t_molasses, Shim_x_current, Shim_y_current, Shim_z_current)
        print_string(molasses_string_list, file)
        
        # photo phase
        tof_string_list = get_photo_string_list(1)
        print_string(tof_string_list, file)
        
        # End cycle
        print_string(end_cycle_string_list, file)
        file.write("ENDINNER\n")
        
        file.write("\nITERATIONS 1\n")
        file.write("\nENDLOOP")
        
print_routine_molasses(t_molasses = 10, Shim_x_current = 0.0, Shim_y_current = 0.5, Shim_z_current = 0.0)
  
    
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import time
import socket
import sys
import os

# Import the necessary module for Windows Registry manipulation
try:
    import winreg 
except ImportError:
    # This will be caught when running on non-Windows systems, 
    # but the whole script is Windows-dependent anyway.
    pass

class App(tk.Tk):
    # --- Base Directory Definition ---
    BASE_DIR = r"C:\na\V3" 
    # A unique key name for the registry entry
    RESTART_REGISTRY_KEY = "ScriptRunnerAppRestart"

    def __init__(self):
        super().__init__()
        self.title("Script Runner")

        # Set the window to fullscreen and on top of other windows
        self.attributes('-fullscreen', True)
        self.attributes('-topmost', True)

        # --- File Paths (Relative to BASE_DIR) ---
        self.logo_path = os.path.join(self.BASE_DIR, "nalogo.png")
        self.pc_config_path = os.path.join(self.BASE_DIR, "pcconfig.bat")
        self.post_settings_path = os.path.join(self.BASE_DIR, "POSTsettings.bat") 

        # --- Set up the main PanedWindow ---
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # --- Left Panel (60% of screen width) ---
        self.left_panel = tk.Frame(self.paned_window, bg="#f0f0f0")
        self.update_idletasks()
        self.paned_window.add(self.left_panel, width=int(self.winfo_screenwidth() * 0.60))

        # Check if the app was relaunched after a PC name change
        self.check_for_post_reboot()

        # Logo display
        self.logo_label = tk.Label(self.left_panel, bg="#f0f0f0")
        self.logo_label.pack(pady=20, padx=20)
        self.load_logo()
        
        # Internet connection status
        self.connection_status_label = tk.Label(self.left_panel, text="Checking...", font=("Aptos", 12), bg="#f0f0f0")
        self.connection_status_label.pack(pady=10)
        self.check_connection()
        
        # PC Name change section
        self.pc_name_frame = tk.Frame(self.left_panel, bg="#f0f0f0")
        self.pc_name_frame.pack(pady=20, padx=10)

        tk.Label(self.pc_name_frame, text="New PC Name:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=(5, 0))
        
        # Create a validation command to limit the entry to 15 characters
        vcmd = (self.register(self._validate_pc_name), '%P')
        self.pc_name_entry = tk.Entry(self.pc_name_frame, width=20, validate="key", validatecommand=vcmd)
        self.pc_name_entry.pack(pady=5)
        
        # Frame for the two buttons
        self.pc_name_button_frame = tk.Frame(self.pc_name_frame, bg="#f0f0f0")
        self.pc_name_button_frame.pack(pady=5)
        
        self.pc_name_button = tk.Button(self.pc_name_button_frame, text="Change PC Name", command=self.change_pc_name, font=("Aptos", 10), bg="#FFFFFF", fg="black")
        self.pc_name_button.pack(side=tk.LEFT, padx=5)
        
        # --- SKIP BUTTON ---
        self.skip_pc_name_button = tk.Button(self.pc_name_button_frame, text="Skip", command=self.skip_pc_name_change, font=("Aptos", 10), bg="#FF6347", fg="white")
        self.skip_pc_name_button.pack(side=tk.LEFT, padx=5)
        
        # PC Configuration section (initially hidden)
        self.pc_config_frame = tk.Frame(self.left_panel, bg="#f0f0f0")
        
        tk.Label(self.pc_config_frame, text="Complete PC Configuration:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=(5, 0))
        
        self.pc_config_button = tk.Button(self.pc_config_frame, text="Start Configuration", command=self.run_pc_config, font=("Arial", 10), bg="#FFFFFF", fg="black")
        self.pc_config_button.pack(pady=5)
        
        # Software Installation section (initially hidden)
        self.software_install_frame = tk.Frame(self.left_panel, bg="#f0f0f0")
        tk.Label(self.software_install_frame, text="Select Software to Install:", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=(5, 0))
        
        self.select_all_var = tk.BooleanVar()
        self.select_all_button = tk.Checkbutton(self.software_install_frame, text="Select All", variable=self.select_all_var, command=self.toggle_all_software, bg="#f0f0f0")
        self.select_all_button.pack(anchor="w", padx=20)
        
        self.software_vars = {
            "N-Able": tk.BooleanVar(),
            "Dell Support Assist": tk.BooleanVar(),
            "Anydesk": tk.BooleanVar(),
            "JDK8": tk.BooleanVar(),
            "JDK11": tk.BooleanVar(),
            "Google Chrome": tk.BooleanVar(),
            "TSPrint": tk.BooleanVar(),
            "NetTime": tk.BooleanVar(),
            "Adobe PDF": tk.BooleanVar(),
            "Windows Scan": tk.BooleanVar(),
            "Whatsapp": tk.BooleanVar(),
            "Office 365": tk.BooleanVar(),
            "ESET": tk.BooleanVar()
        }
        
        # Create a frame to hold the software list in a grid
        self.software_grid_frame = tk.Frame(self.software_install_frame, bg="#f0f0f0")
        self.software_grid_frame.pack(padx=20, pady=10)

        self.software_labels = {}
        row_idx, col_idx = 0, 0
        for software, var in self.software_vars.items():
            item_frame = tk.Frame(self.software_grid_frame, bg="#f0f0f0")
            item_frame.grid(row=row_idx, column=col_idx, padx=10, pady=5, sticky="w")
            
            tk.Checkbutton(item_frame, text=software, variable=var, bg="#f0f0f0").pack(side=tk.LEFT)
            status_label = tk.Label(item_frame, text="", bg="#f0f0f0", fg="green")
            status_label.pack(side=tk.LEFT, padx=5)
            self.software_labels[software] = status_label
            
            col_idx += 1
            if col_idx > 2:
                col_idx = 0
                row_idx += 1
                
        self.start_install_button = tk.Button(self.software_install_frame, text="Start Installation", command=self.start_software_installation, font=("Arial", 10), bg="#FFFFFF", fg="black")
        self.start_install_button.pack(pady=10)
        
        # --- Right Panel (Output Terminal) ---
        self.right_panel = tk.Frame(self.paned_window, bg="#E0E0E0")
        self.paned_window.add(self.right_panel, width=int(self.winfo_screenwidth() * 0.25))

        self.terminal_label = tk.Label(self.right_panel, text="Progress", font=("Arial", 12, "bold"), bg="#E0E0E0", fg="black")
        self.terminal_label.pack(pady=(10, 0))

        self.terminal_output = tk.Text(self.right_panel, bg="white", fg="black", insertbackground="black", state="disabled", font=("Courier New", 10))
        self.terminal_output.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.scrollbar = tk.Scrollbar(self.terminal_output, command=self.terminal_output.yview)
        self.terminal_output['yscrollcommand'] = self.scrollbar.set

        # Exit button at the bottom
        self.exit_button = tk.Button(self, text="Exit", command=self.destroy, font=("Arial", 10), bg="#ffffff", fg="black", activebackground="#ffffff")
        self.exit_button.pack(side=tk.BOTTOM, pady=10)

    # --- NEW REGISTRY / RESTART LOGIC ---

    def set_app_to_restart(self):
        """Sets a key in the Windows Registry to automatically run this script on the next login."""
        try:
            # Get the full path to the running script interpreter
            # sys.executable is the Python interpreter (e.g., python.exe)
            # sys.argv[0] is the path to the current script
            app_command = f'"{sys.executable}" "{sys.argv[0]}"'
            
            # Access the 'Run' key in the registry
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            
            # Set the value: key name (RESTART_REGISTRY_KEY) and the command to run
            winreg.SetValueEx(key, self.RESTART_REGISTRY_KEY, 0, winreg.REG_SZ, app_command)
            winreg.CloseKey(key)
            self.update_terminal("Registry key set to relaunch application after reboot.\n")
            return True
        except Exception as e:
            self.update_terminal(f"Error setting registry key for restart: {e}\n")
            return False

    def remove_app_restart_key(self):
        """Removes the registry key after the application has been successfully relaunched."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE)
            winreg.DeleteValue(key, self.RESTART_REGISTRY_KEY)
            winreg.CloseKey(key)
            self.update_terminal("Application restart registry key cleaned up.\n")
        except FileNotFoundError:
            # Key wasn't there, which is fine
            pass
        except Exception as e:
            self.update_terminal(f"Error removing registry key: {e}\n")

    def check_for_post_reboot(self):
        """Checks if the application was started via the restart registry key."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
            # Try to read the value we set
            winreg.QueryValueEx(key, self.RESTART_REGISTRY_KEY)
            winreg.CloseKey(key)
            
            # If the value is found, we know we're post-reboot
            # We must remove the key first, then proceed to the next step
            self.remove_app_restart_key()
            
            # Transition directly to the PC Configuration section
            self.after(500, self.show_pc_config_section)
            self.after(500, lambda: self.update_terminal("\n*** PC Name Change complete (after reboot). Resuming setup... ***\n"))
            
            # Return True to signal that the initial UI should be bypassed
            return True 

        except FileNotFoundError:
            # Key not found, which is the normal starting condition
            return False
        except Exception as e:
            # Handle other errors, but proceed normally
            self.after(0, lambda: self.update_terminal(f"Warning during post-reboot check: {e}\n"))
            return False
            
    # --- MODIFIED METHODS ---

    def show_name_change_restart_prompt(self):
        """
        Displays a modal dialog box to prompt the user to restart the computer.
        The restart button now prepares the app to relaunch.
        """
        self.update_terminal("PC Name changed successfully in memory.\n\n"
                             "**A RESTART IS MANDATORY** for the new name to take full effect.\n"
                             "Clicking 'Restart Now' will automatically relaunch this application.\n")
        
        restart_window = tk.Toplevel(self)
        restart_window.title("Restart Required")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 500
        window_height = 220
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        restart_window.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
        
        restart_window.attributes('-topmost', True)
        restart_window.grab_set() 
        
        message_label = tk.Label(restart_window, text="PC Name change is complete.\n\n"
                                                      "**RESTART NOW** to finalize the name change and automatically continue setup.", 
                                 font=("Arial", 12, "bold"), fg="#DC143C")
        message_label.pack(pady=20, padx=10)
        
        button_frame = tk.Frame(restart_window)
        button_frame.pack(pady=10)
        
        # Bind the restart button to the new restart flow
        restart_button = tk.Button(button_frame, 
                                   text="Restart Now (Relaunch App)", 
                                   command=lambda: [self.set_app_to_restart(), self.force_restart()], # New flow!
                                   font=("Arial", 10, "bold"), 
                                   bg="#DC143C", 
                                   fg="white")
        restart_button.pack(side=tk.LEFT, padx=10)
        
        continue_button = tk.Button(button_frame, 
                                    text="Continue without Restart (Not Recommended)", 
                                    command=lambda: [restart_window.destroy(), self.show_pc_config_section()], 
                                    font=("Arial", 10), 
                                    bg="#4682B4", 
                                    fg="white")
        continue_button.pack(side=tk.RIGHT, padx=10)
        
    def skip_pc_name_change(self):
        """
        Skips the PC name change section and moves directly to the PC configuration section.
        """
        self.update_terminal("PC Name change skipped. Moving to PC configuration.\n")
        self.show_pc_config_section()

    def show_pc_config_section(self):
        """Hides the PC name section and displays the PC configuration section."""
        self.pc_name_frame.pack_forget()
        self.pc_config_frame.pack(pady=20, padx=10)
        # Add a clear message if we are continuing from a fresh start or a skip
        if not self.check_for_post_reboot(): 
             self.update_terminal("Ready to begin PC configuration.\n")
        
    # ... (Other methods like load_logo, check_connection, _read_stream, etc., are unchanged) ...
    def load_logo(self):
        """Loads the logo image from the specified path."""
        try:
            logo_img = Image.open(self.logo_path)
            # Resize image to fit
            width, height = logo_img.size
            if width > 200 or height > 200:
                logo_img = logo_img.resize((450, 200), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            self.logo_label.config(image=self.logo_photo)
        except FileNotFoundError:
            self.logo_label.config(text="Logo Not Found", fg="red", font=("Arial", 12))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logo: {e}")
            
    def check_connection(self):
        """Checks for internet connection and updates the status label."""
        try:
            socket.create_connection(("google.com", 80))
            self.connection_status_label.config(text="Online", fg="green")
        except OSError:
            self.connection_status_label.config(text="Offline", fg="red")
        
        # Schedule the next check in 3 seconds (3000 ms)
        self.after(3000, self.check_connection)

    def _validate_pc_name(self, P):
        """Validates the input to ensure it is no more than 15 characters."""
        return len(P) <= 15
        
    def change_pc_name(self):
        """
        Validates the new PC name and executes a PowerShell command to change it.
        """
        new_name = self.pc_name_entry.get().strip()

        if not new_name:
            self.update_terminal("Error: PC name cannot be empty.\n")
            return

        # PowerShell command to change the computer name without restarting
        command = f"Rename-Computer -NewName '{new_name}' -Force -PassThru"
        
        # Clear the terminal output
        self.terminal_output.config(state="normal")
        self.terminal_output.delete("1.0", tk.END)
        self.terminal_output.config(state="disabled")

        self.update_terminal(f"Changing PC name to '{new_name}'...\n\n")

        # The callback now shows a prompt to restart for the name change
        thread = threading.Thread(target=self._execute_process_thread, args=(command, self.show_name_change_restart_prompt))
        thread.start()

    def run_pc_config(self):
        """Runs the PC configuration batch file."""
        self.update_terminal("Starting PC configuration...\n\n")
        # The callback shows the software installation section
        thread = threading.Thread(target=self._execute_process_thread, args=(self.pc_config_path, self.show_software_installation_section))
        thread.start()
        
    def toggle_all_software(self):
        """Toggles all software checkboxes based on the 'Select All' checkbox state."""
        is_checked = self.select_all_var.get()
        for var in self.software_vars.values():
            var.set(is_checked)
        
    def mark_as_installed(self, software_name):
        """Updates the label to show that the software has been installed."""
        if software_name in self.software_labels:
            self.software_labels[software_name].config(text="Installed")
            
    def start_software_installation(self):
        """
        Runs the installation scripts for the selected software sequentially.
        """
        selected_software = [sw for sw, var in self.software_vars.items() if var.get()]
        if not selected_software:
            self.update_terminal("No software selected for installation.\n")
            return
            
        self.update_terminal("Starting software installation...\n\n")
        
        # Start a single thread to run all scripts sequentially
        thread = threading.Thread(target=self._run_all_scripts_sequentially, args=(selected_software,))
        thread.start()

    # --- SEQUENTIAL EXECUTION METHOD ---
    def _run_all_scripts_sequentially(self, selected_software):
        """
        Runs all selected software installation scripts, and then the final post-settings script.
        This must be run within a thread.
        """
        # --- 1. Run all selected software scripts ---
        for script_name in selected_software:
            # Assumes individual scripts are named "SoftwareName.ps1"
            script_path = os.path.join(self.BASE_DIR, f"{script_name.replace(' ', '')}.ps1")

            self.after(0, lambda name=script_name: self.update_terminal(f"Installing {name} from '{os.path.basename(script_path)}'...\n"))

            # _execute_process_sync is a blocking call within this thread
            success = self._execute_process_sync(script_path) 
            
            if success:
                 # Update the GUI on the main thread after successful completion
                self.after(0, lambda name=script_name: self.mark_as_installed(name))
            else:
                self.after(0, lambda name=script_name: self.update_terminal(f"Installation of {name} failed or was interrupted.\n"))
                
        # --- 2. Execute the post-installation script ---
        self.after(0, lambda: self.update_terminal(f"Starting post-installation settings script '{os.path.basename(self.post_settings_path)}'...\n"))
        
        # Run the post-settings script (blocking call)
        post_settings_success = self._execute_process_sync(self.post_settings_path)
        
        # --- 3. Show final restart prompt on main thread ---
        if post_settings_success:
            self.after(0, self.show_restart_prompt)
        else:
            self.after(0, lambda: self.update_terminal("Post-installation settings script failed. Manual check required.\n"))

    def _read_stream(self, stream):
        """Reads a stream line-by-line in real-time and updates the terminal."""
        for line in iter(stream.readline, ''):
            self.after(0, lambda: self.update_terminal(line))
        stream.close()

    # --- NON-BLOCKING THREAD (for main UI flow) ---
    def _execute_process_thread(self, command, callback=None):
        """
        Threaded function to execute a command or script non-blocking to the main UI.
        """
        # Blocking execution within the thread
        success = self._execute_process_sync(command)
        
        # If successful and a callback is provided, run it on the main thread
        if success and callback:
            self.after(0, callback)
            
    # --- BLOCKING SYNCHRONOUS EXECUTION (for sequential installation) ---
    def _execute_process_sync(self, command):
        """
        Synchronous (blocking) function to execute a command and display its output.
        Returns True on success (return code 0), False otherwise.
        """
        return_code = -1
        try:
            if sys.platform != "win32":
                self.after(0, lambda: self.update_terminal("Error: This feature is only supported on Windows."))
                return False

            is_batch_file = command.lower().endswith(".bat")
            is_ps_file = command.lower().endswith(".ps1")
            
            # Use subprocess.Popen for real-time output reading
            if is_batch_file:
                # Use cmd.exe /c for batch files
                proc = subprocess.Popen(['cmd.exe', '/c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            elif is_ps_file:
                # Use powershell.exe -File for PowerShell scripts
                proc = subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            else: # Assume it's a direct command (like Rename-Computer)
                proc = subprocess.Popen(['powershell.exe', '-Command', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            # Start separate threads to read stdout and stderr in real-time
            stdout_thread = threading.Thread(target=self._read_stream, args=(proc.stdout,))
            stderr_thread = threading.Thread(target=self._read_stream, args=(proc.stderr,))

            stdout_thread.start()
            stderr_thread.start()

            # Wait for the process and output threads to complete
            proc.wait()
            stdout_thread.join()
            stderr_thread.join()

            return_code = proc.returncode
            self.after(0, lambda: self.update_terminal(f"\nCommand finished with return code {return_code}.\n"))
            
            return return_code == 0
            
        except FileNotFoundError:
            self.after(0, lambda: self.update_terminal(f"Error: The executable or file '{command}' was not found.\n"))
        except Exception as e:
            self.after(0, lambda: self.update_terminal(f"An unexpected error occurred: {e}\n"))
        
        return False # Return False on any exception or non-zero return code

    def show_software_installation_section(self):
        """Hides the PC config section and displays the software installation section."""
        self.pc_config_frame.pack_forget()
        self.software_install_frame.pack(pady=20, padx=10)
        self.update_terminal("\nPC configuration completed. Please select the software you wish to install.\n")

    def show_restart_prompt(self):
        """
        Displays a modal dialog box to prompt the user to restart the computer.
        (This is the final restart prompt after all installs are done)
        """
        self.update_terminal("All installations completed. A final restart is required. Please click the button to restart.\n")
        
        restart_window = tk.Toplevel(self)
        restart_window.title("Restart Required")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 200
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        restart_window.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
        
        restart_window.attributes('-topmost', True)
        restart_window.grab_set() # Make it modal
        
        message_label = tk.Label(restart_window, text="All installations are complete.\n\n"
                                                      "Please click 'Restart' to finish the setup.", 
                                 font=("Arial", 12))
        message_label.pack(expand=True)
        
        restart_button = tk.Button(restart_window, text="Restart Now", command=self.force_restart, font=("Arial", 10, "bold"), bg="#4682B4", fg="white")
        restart_button.pack(pady=10)

    def force_restart(self):
        """
        Forces a system restart.
        """
        self.update_terminal("Initiating system restart...\n")
        # Command to force a restart
        command = "shutdown /r /f /t 0"
        try:
            subprocess.run(command, check=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except subprocess.CalledProcessError as e:
            self.update_terminal(f"Error initiating restart: {e.stderr}\n")
        except FileNotFoundError:
            self.update_terminal("Error: 'shutdown' command not found.\n")

    def update_terminal(self, text):
        """Inserts text into the terminal and applies color."""
        self.terminal_output.config(state="normal")
        self.terminal_output.insert(tk.END, text)
        self.terminal_output.config(state="disabled")
        self.terminal_output.see(tk.END)
        
if __name__ == "__main__":
    # The application needs to be launched as an administrator for registry and system commands.
    app = App()
    app.mainloop()
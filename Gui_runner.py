import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import time
import socket
import sys
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Script Runner")

        # Set the window to fullscreen and on top of other windows
        self.attributes('-fullscreen', True)
        self.attributes('-topmost', True)

        # --- File Paths (adjust as needed) ---
        self.logo_path = r"C:\na\V3\nalogo.png"
        self.pc_config_path = r"C:\na\V3\pcconfig.bat"
        self.software_bat_path = r"C:\na\V3\Software.bat"

        # --- Set up the main PanedWindow ---
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # --- Left Panel (75% of screen width) ---
        self.left_panel = tk.Frame(self.paned_window, bg="#f0f0f0")
        self.paned_window.add(self.left_panel, width=int(self.winfo_screenwidth() * 0.60))

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
        
        self.pc_name_button = tk.Button(self.pc_name_frame, text="Change PC Name", command=self.change_pc_name, font=("Aptos", 10), bg="#FFFFFF", fg="black")
        self.pc_name_button.pack(pady=5)
        
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

        thread = threading.Thread(target=self._execute_process_thread, args=(command, self.show_pc_config_section))
        thread.start()

    def run_pc_config(self):
        """Runs the PC configuration batch file."""
        self.update_terminal("Starting PC configuration...\n\n")
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
        Runs the installation scripts for the selected software.
        """
        selected_software = [sw for sw, var in self.software_vars.items() if var.get()]
        if not selected_software:
            self.update_terminal("No software selected for installation.\n")
            return
            
        self.update_terminal("Starting software installation...\n\n")
        
        # This will run scripts sequentially.
        def run_all_scripts(scripts):
            for script_name in scripts:
                script_path = os.path.join(r"C:\na\V3", f"{script_name.replace(' ', '')}.ps1")
                self.update_terminal(f"Installing {script_name} from '{os.path.basename(script_path)}'...\n")
                
                # Pass a lambda function as the callback to correctly pass the software name
                callback = lambda name=script_name: self.mark_as_installed(name)
                self._execute_process_thread(script_path, callback)

            # Execute the post-installation script after all software is installed
            post_settings_path = r"C:\na\V3\POSTsettings.bat"
            self.update_terminal(f"Starting post-installation settings script '{os.path.basename(post_settings_path)}'...\n")
            # The callback for this last script will show the restart prompt
            self._execute_process_thread(post_settings_path, self.show_restart_prompt)


        thread = threading.Thread(target=run_all_scripts, args=(selected_software,))
        thread.start()
        
    def _read_stream(self, stream):
        """Reads a stream line-by-line in real-time and updates the terminal."""
        for line in iter(stream.readline, ''):
            self.after(0, lambda: self.update_terminal(line))
        stream.close()

    def _execute_process_thread(self, command, callback=None):
        """
        Threaded function to execute a command or script and display its output.
        NOTE: This script must be run with administrator privileges to work correctly.
        """
        try:
            if sys.platform == "win32":
                is_batch_file = command.lower().endswith(".bat")
                is_ps_file = command.lower().endswith(".ps1")
                
                if is_batch_file or is_ps_file:
                    # Unblock the file before running
                    try:
                        subprocess.run(['powershell.exe', 'Unblock-File', '-Path', command], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
                    except Exception as e:
                        self.after(0, lambda: self.update_terminal(f"Warning: Could not unblock file '{command}': {e}\n"))

                if is_batch_file:
                    proc = subprocess.Popen(['cmd.exe', '/c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
                elif is_ps_file:
                    proc = subprocess.Popen(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
                else: # Assume it's a direct command
                    proc = subprocess.Popen(['powershell.exe', '-Command', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
                
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
                
                # If command was successful and a callback is provided, run it
                if return_code == 0 and callback:
                    self.after(0, callback)
            
            else:
                self.after(0, lambda: self.update_terminal("Error: This feature is only supported on Windows."))
            
        except FileNotFoundError:
            self.after(0, lambda: self.update_terminal(f"Error: The file '{command}' was not found.\n"))
        except Exception as e:
            self.after(0, lambda: self.update_terminal(f"An unexpected error occurred: {e}\n"))
    
    def show_pc_config_section(self):
        """Hides the PC name section and displays the PC configuration section."""
        self.pc_name_frame.pack_forget()
        self.pc_config_frame.pack(pady=20, padx=10)
        self.update_terminal("\nA restart is required for the new PC name to take effect.\n")
        
    def show_software_installation_section(self):
        """Hides the PC config section and displays the software installation section."""
        self.pc_config_frame.pack_forget()
        self.software_install_frame.pack(pady=20, padx=10)
        self.update_terminal("\nPC configuration completed. Please select the software you wish to install.\n")

    def show_restart_prompt(self):
        """
        Displays a modal dialog box to prompt the user to restart the computer.
        """
        self.update_terminal("All installations completed. A restart is required. Please click the button to restart.\n")
        
        restart_window = tk.Toplevel(self)
        restart_window.title("Restart Required")
        
        # Center the window on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 200
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        restart_window.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
        
        restart_window.attributes('-topmost', True)
        restart_window.grab_set()  # Make it modal
        
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
        # The /t 0 makes it immediate
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
    # IMPORTANT: You must run this script as an administrator for the subprocess to have elevated privileges.
    # To run as admin, right-click the script and select 'Run as Administrator'.
    app = App()
    app.mainloop()

import win32cred
from tkinter import messagebox, Tk, Scrollbar, END, StringVar, Entry, Canvas, Frame as TkFrame, Label as TkLabel
from tkinter.ttk import Button, Style, Frame as TtkFrame, Label as TtkLabel
import sys
import os
import threading
import subprocess
import platform

# --- Optional Libraries for Logo ---
try:
    from PIL import Image, ImageTk
except ImportError:
    Image, ImageTk = None, None 

# --- Configuration Constants ---
RDP_CREDENTIAL_PREFIX = "TERMSRV/"
LOGO_PATH = r"C:\na\v3\nalogosage.jpg" 

# --- DOMAIN CONSTANT ---
RDP_DOMAIN_SUFFIX = ".networkassociates.co.za"

# --- BLOCK SIZING CONSTANTS ---
CARDS_PER_ROW = 6 
CARDS_PER_COLUMN_VISIBLE = 8 
CARD_WIDTH = 280
CARD_HEIGHT = 110
CARD_PAD = 12

# Calculated dimensions for the inner frame (after padding inside the card)
INNER_PAD = 10 
INNER_W = CARD_WIDTH - (2 * INNER_PAD)
INNER_H = CARD_HEIGHT - (2 * INNER_PAD)

# Calculated minimum canvas dimensions based on fixed block sizes
CANVAS_WIDTH = (CARD_WIDTH + 2 * CARD_PAD) * CARDS_PER_ROW
CANVAS_HEIGHT = (CARD_HEIGHT + 2 * CARD_PAD) * CARDS_PER_COLUMN_VISIBLE
# ------------------------------

ONLINE_COLOR = '#2ecc71'
OFFLINE_COLOR = '#e74c3c'
DEFAULT_CARD_BG = '#ecf0f1'
PING_COUNT = '1'
PING_TIMEOUT = '1000'
MONITOR_INTERVAL_MS = 5000

class RDPGUI:
    def __init__(self, master):
        self.master = master
        master.title("RDP Credential Dashboard")
        
        # Set window state to maximized
        if platform.system() == "Windows":
             master.state('zoomed') 

        self.master_profiles_list = [] 
        self.search_var = StringVar() 
        self.filter_term = ""
        self.card_container_id = None
        
        self.card_references = {} 
        self._monitoring_job = None 

        # --- Variables for Manual Connect Section ---
        self.server_var = StringVar()
        self.username_var = StringVar()
        self.password_var = StringVar()


        self._setup_styles()
        self.logo_image = self._load_logo()
        
        # Row 1 is the main content/canvas, weight=1 ensures it takes all extra space
        self.master.grid_rowconfigure(1, weight=1) 
        self.master.grid_columnconfigure(0, weight=1)

        # --- Top Bar (Row 0) ---
        top_bar_frame = TtkFrame(master, style="TopBar.TFrame")
        top_bar_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        # Configure columns (0: Header, 1: Filler, 2: Search Bar)
        top_bar_frame.grid_columnconfigure(0, weight=1) 
        top_bar_frame.grid_columnconfigure(1, weight=1)
        top_bar_frame.grid_columnconfigure(2, weight=0)

        
        # --- Header (Logo and Title - Left) ---
        header_frame = TtkFrame(top_bar_frame, style="TopBar.TFrame")
        header_frame.grid(row=0, column=0, sticky="w", padx=(0, 10)) 
        
        # 1. LOGO (Packed first for left position)
        if self.logo_image:
            logo_label = TtkLabel(header_frame, image=self.logo_image) 
            logo_label.image = self.logo_image 
            logo_label.pack(side="left", padx=(0, 15)) # Padding on the right of the logo
            
        # 2. TITLE (Packed second, right of the logo)
        TtkLabel(header_frame, text="RDP Dashboard", 
                                font=("Aptos",32, "bold"), style="TopBar.TLabel").pack(side="left", pady=5)

        
        # --- Search Bar (Right) ---
        search_frame = TtkFrame(top_bar_frame, style="TopBar.TFrame")
        search_frame.grid(row=0, column=2, sticky="e") 
        
        TtkLabel(search_frame, text="Filter:", style="TopBar.TLabel", font=("Aptos", 12)).pack(side="left", padx=(0, 10))
        
        search_entry = Entry(search_frame, textvariable=self.search_var, font=("Consolas", 12), width=40, fg='gray')
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind('<KeyRelease>', self._filter_list)
        
        search_entry.insert(0, "Search Server or Username...")
        search_entry.bind('<FocusIn>', lambda event: self._clear_placeholder(search_entry)) 
        search_entry.bind('<FocusOut>', lambda event: self._restore_placeholder(search_entry)) 

        # --- Content Area (Row 1: Scrollable Canvas) ---
        content_frame = TtkFrame(master, style="Content.TFrame")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # APPLY MINIMUM SIZE TO CANVAS
        self.canvas = Canvas(content_frame, 
                             highlightthickness=0, 
                             bg="#FFFFFF",
                             width=CANVAS_WIDTH, 
                             height=CANVAS_HEIGHT) 
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = Scrollbar(content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.card_container = TtkFrame(self.canvas, style="Content.TFrame") 
        
        self.card_container_id = self.canvas.create_window(
            (0, 0), window=self.card_container, anchor="nw"
        )
        
        self.card_container.bind("<Configure>", self._on_frame_configure)
        
        # Bind the canvas resize to ensure the inner container width matches
        self.canvas.bind('<Configure>', self._on_canvas_resize) 

        self._display_credentials()
        
        
        # --- Manual Connect Bar (New Row 2 at the bottom) ---
        
        # Row 2 (the bottom row) uses weight=0 so it stays fixed height
        self.master.grid_rowconfigure(2, weight=0) 
        
        manual_connect_frame = TtkFrame(master, style="TopBar.TFrame") # Using TopBar style for dark background
        manual_connect_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        
        # Configure the columns of the manual connect frame (3 labels, 3 entries, 1 button)
        manual_connect_frame.grid_columnconfigure(0, weight=0) # Server Label
        manual_connect_frame.grid_columnconfigure(1, weight=1) # Server Entry (takes most space)
        manual_connect_frame.grid_columnconfigure(2, weight=0) # User Label
        manual_connect_frame.grid_columnconfigure(3, weight=0) # User Entry
        manual_connect_frame.grid_columnconfigure(4, weight=0) # Password Label
        manual_connect_frame.grid_columnconfigure(5, weight=0) # Password Entry
        manual_connect_frame.grid_columnconfigure(6, weight=0) # Connect Button

        # 1. Server Field
        TtkLabel(manual_connect_frame, text="Server:", style="TopBar.TLabel").grid(
            row=0, column=0, sticky='w', padx=(10, 5), pady=10
        )
        Entry(manual_connect_frame, textvariable=self.server_var, font=("Consolas", 12)).grid(
            row=0, column=1, sticky='ew', padx=5, pady=10
        )

        # 2. Username Field
        TtkLabel(manual_connect_frame, text="Username:", style="TopBar.TLabel").grid(
            row=0, column=2, sticky='w', padx=(15, 5), pady=10
        )
        Entry(manual_connect_frame, textvariable=self.username_var, font=("Consolas", 12), width=20).grid(
            row=0, column=3, sticky='w', padx=5, pady=10
        )

        # 3. Password Field
        TtkLabel(manual_connect_frame, text="Password:", style="TopBar.TLabel").grid(
            row=0, column=4, sticky='w', padx=(15, 5), pady=10
        )
        Entry(manual_connect_frame, textvariable=self.password_var, font=("Consolas", 12), show='*', width=20).grid(
            row=0, column=5, sticky='w', padx=5, pady=10
        )

        # 4. Connect Button
        Button(manual_connect_frame, text="Connect", command=self._connect_manual_rdp, style="Connect.TButton").grid(
            row=0, column=6, sticky='e', padx=(15, 10), pady=10
        )
        # -----------------------------------------------


        self.master.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def _on_close(self):
        if self._monitoring_job:
            self.master.after_cancel(self._monitoring_job)
        self.master.destroy()

    def _load_logo(self):
        if Image is None or ImageTk is None or not os.path.exists(LOGO_PATH):
            return None
        
        try:
            img = Image.open(LOGO_PATH)
            img = img.resize((430, 180), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    # --------------------------------------------------------------------------
    # --- MONITORING/Pinging Methods (UNCHANGED) ---
    # --------------------------------------------------------------------------
    
    def _start_status_monitor(self):
        if self._monitoring_job:
            self.master.after_cancel(self._monitoring_job)
            
        self._periodic_status_check()
    
    def _periodic_status_check(self):
        for card_id, refs in self.card_references.items():
            # NOTE: We ping the full server name stored in the credential list, 
            # NOT the shortened display name.
            full_server_name = self._get_full_server_name(refs['server_label']['text'])
            
            t = threading.Thread(target=self._check_server_status, args=(full_server_name, card_id))
            t.daemon = True
            t.start()
        
        self._monitoring_job = self.master.after(MONITOR_INTERVAL_MS, self._periodic_status_check)

    def _get_full_server_name(self, short_name):
        """Reconstructs the FQDN for pinging/connecting based on the short display name."""
        
        # If the short name (in caps) is the prefix of a full name in our master list, use the full name
        short_name_lower = short_name.lower()
        if RDP_DOMAIN_SUFFIX not in short_name_lower:
            for profile in self.master_profiles_list:
                if profile['Server'].lower().startswith(short_name_lower) and profile['Server'].lower().endswith(RDP_DOMAIN_SUFFIX):
                     return profile['Server']
            
        # In all other cases (e.g., if the user saved the short name or an IP), use the short name directly
        return short_name_lower
        
    def _check_server_status(self, server_address, card_id):
        if platform.system().lower() == "windows":
            ping_params = ['ping', '-n', PING_COUNT, '-w', PING_TIMEOUT, server_address]
        else:
            ping_params = ['ping', '-c', PING_COUNT, '-W', str(int(PING_TIMEOUT) // 1000), server_address]
        
        with open(os.devnull, 'w') as devnull:
            try:
                result = subprocess.call(ping_params, stdout=devnull, stderr=devnull)
                is_alive = (result == 0)
            except Exception:
                is_alive = False

        self.master.after(0, self._update_card_status, card_id, is_alive)

    def _update_card_status(self, card_id, is_alive):
        if card_id not in self.card_references:
            return

        status_dot = self.card_references[card_id]['status_dot']
        new_bg = ONLINE_COLOR if is_alive else OFFLINE_COLOR
        
        # We must use ttk.Style() to change the background of a ttk widget
        s = Style()
        # Create or update a specific style for this dot to set its background
        dot_style_name = f'StatusDot-{card_id}.TLabel'
        s.configure(dot_style_name, background=new_bg)
        status_dot.configure(style=dot_style_name)

    # --------------------------------------------------------------------------
    # --- Layout/Style Methods ---
    # --------------------------------------------------------------------------
    
    def _on_canvas_resize(self, event):
        self._on_frame_configure(event)

    def _on_frame_configure(self, event):
        """Updates the Canvas scroll region and inner frame width."""
        if self.card_container_id is not None:
              # Ensure inner frame width is at least the width required for 6 cards, 
              # but expands if the canvas is wider (due to maximization).
              
              # Use max(CANVAS_WIDTH, self.canvas.winfo_width()) to ensure 
              # the container never shrinks below the 6-card width.
              self.canvas.itemconfigure(
                 self.card_container_id, 
                 width=max(CANVAS_WIDTH, self.canvas.winfo_width())
              )
        # Update scrollable region based on the size of the inner frame
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _clear_placeholder(self, entry_widget):
        if entry_widget.get() == "Search Server or Username...":
            entry_widget.delete(0, END)
            entry_widget.config(fg='black')

    def _restore_placeholder(self, entry_widget):
        if not entry_widget.get():
            entry_widget.insert(0, "Search Server or Username...")
            entry_widget.config(fg='gray')

    def _setup_styles(self):
        s = Style()
        s.theme_use('clam')
        
        TOP_BAR_BG = "#00d637"
        
        s.configure('TopBar.TFrame', background=TOP_BAR_BG)
        s.configure('TopBar.TLabel', background=TOP_BAR_BG, foreground='white')
        
        s.configure('Exit.TButton', 
                    font=('Arial', 10, 'bold'), 
                    background=TOP_BAR_BG, 
                    foreground='white',
                    relief='flat', 
                    padding=[10, 5])
        s.map('Exit.TButton', 
              background=[('active', 'red')],
              foreground=[('active', 'white')])

        s.configure('Connect.TButton', 
                    font=('Arial', 10, 'bold'), 
                    background='#2d3456', # Green
                    foreground='white',
                    relief='flat', 
                    padding=[10, 5])
        s.map('Connect.TButton', 
              background=[('active', '#27ae60')])

        s.configure('Content.TFrame', background='#ffffff')
        
        s.configure('StatusDot.TLabel', background=DEFAULT_CARD_BG, relief='raised', borderwidth=1, width=1)

    def _clear_card_container(self):
        for widget in self.card_container.winfo_children():
            widget.destroy()
        self.card_references.clear()

    def _filter_list(self, event=None):
        """Clears and redraws cards based on the filter term."""
        self.filter_term = self.search_var.get().strip().lower()
        if self.filter_term == "search server or username...": 
            self.filter_term = ""
            
        self._clear_card_container()

        if not self.master_profiles_list:
              TkLabel(self.card_container, text="No RDP profiles found.", 
                      font=('Aptos', 14), background="#ffffff").grid(row=0, column=0, padx=20, pady=20)
              self._on_frame_configure(None)
              return

        row, col = 0, 0
        cards_drawn = 0 
        for i, profile in enumerate(self.master_profiles_list):
            server_lower = profile['Server'].lower()
            username_lower = profile['Username'].lower() 
            
            # Filtering logic remains the same (searchable by username OR full server name)
            if not self.filter_term or self.filter_term in server_lower or self.filter_term in username_lower:
                
                card_id = f"card_{i}" 
                
                self._create_profile_card(self.card_container, profile, row, col, card_id)
                cards_drawn += 1 

                col += 1
                if col >= CARDS_PER_ROW:
                    col = 0
                    row += 1
        
        print(f"DEBUG: Filtered and attempted to draw {cards_drawn} cards.")

        self.card_container.update_idletasks()
        self._on_frame_configure(None)
        
        self._start_status_monitor()


    def _create_profile_card(self, parent, profile, row, col, card_id):
        
        # --- LOGIC FOR SHORT DISPLAY NAME ---
        # Get the part of the server name BEFORE the domain suffix
        display_name = profile['Server'].partition(RDP_DOMAIN_SUFFIX)[0]
        if not display_name:
             display_name = profile['Server'] 
             
        # *** NEW: Convert display_name to uppercase ***
        display_name = display_name.upper()
        # ---------------------------------------
        
        # 1. ENFORCE FIXED SIZE ON OUTER CARD
        card = TkFrame(parent, width=CARD_WIDTH, height=CARD_HEIGHT, 
                         bg=DEFAULT_CARD_BG, relief='flat', borderwidth=0)
        card.grid(row=row, column=col, padx=CARD_PAD, pady=CARD_PAD)
        card.grid_propagate(False) # CRITICAL: Forces size adherence
        card.card_id = card_id 
        
        # 2. INNER FRAME (Double-enforce size)
        inner_frame = TkFrame(card, bg=DEFAULT_CARD_BG, width=INNER_W, height=INNER_H)
        inner_frame.pack(fill='both', expand=True, padx=INNER_PAD, pady=INNER_PAD)
        inner_frame.grid_propagate(False) # CRITICAL: Inner frame must also obey size

        # Configure inner grid to push content to the top and ensure uniformity
        inner_frame.grid_columnconfigure(0, weight=1) # Server/Username column takes space
        inner_frame.grid_columnconfigure(1, weight=0) # Status dot column is fixed width
        
        inner_frame.grid_rowconfigure(0, weight=0) # Server row is fixed height
        inner_frame.grid_rowconfigure(1, weight=0) # Username row is fixed height
        inner_frame.grid_rowconfigure(2, weight=1) # *** SPACER ROW TAKES ALL REMAINING VERTICAL SPACE ***

        # Row 0: Server Label and Status Dot
        
        # Status Dot (Top Right)
        status_dot = TtkLabel(inner_frame, style="StatusDot.TLabel")
        status_dot.grid(row=0, column=1, sticky="ne", padx=5, pady=5)
        status_dot.configure(padding=[3, 3]) 

        # Server Label (Top Left)
        server_label = TkLabel(inner_frame, text=display_name, bg=DEFAULT_CARD_BG, 
                                 fg='#34495e', font=('Aptos', 18, 'bold'), justify='left', anchor='nw', 
                                 wraplength=INNER_W - 50) # Use INNER_W minus dot space
        server_label.grid(row=0, column=0, sticky="nw", pady=(0, 5), columnspan=1)
        
        # Row 1: Username Label
        username_label = TkLabel(inner_frame, text=f"User: {profile['Username']}", bg=DEFAULT_CARD_BG, 
                                 fg='#34495e', font=('Aptos', 13, 'bold'), justify='left', anchor='nw', 
                                 wraplength=INNER_W)
        username_label.grid(row=1, column=0, sticky="nw", columnspan=2)
        
        # Row 2: Empty Spacer (Ensures content is top-aligned and block size is uniform)
        TkLabel(inner_frame, text="", bg=DEFAULT_CARD_BG).grid(row=2, column=0, sticky="nsew", columnspan=2)
        
        self.card_references[card_id] = {
            'card': card,
            'inner_frame': inner_frame,
            'server_label': server_label,
            'username_label': username_label, 
            'status_dot': status_dot
        }

        # IMPORTANT: When connecting, we MUST pass the full name from the original profile
        def connect_action(event):
            self._connect_rdp_from_card(profile)

        # Bind click action to all relevant widgets
        for widget in [card, inner_frame, server_label, username_label, status_dot]:
            widget.bind('<Button-1>', connect_action)

    # --------------------------------------------------------------------------
    # --- RDP Connect Logic (UNCHANGED) ---
    # --------------------------------------------------------------------------
    
    def _save_temp_credential(self, server, username, password):
        """
        Saves a temporary session credential to Windows Credential Manager.
        """
        if sys.platform != 'win32':
             return 

        target_name = RDP_CREDENTIAL_PREFIX + server
        
        # Build the CREDENTIAL structure
        cred = {
            'TargetName': target_name,
            'Type': win32cred.CRED_TYPE_GENERIC,
            'UserName': username,
            'CredentialBlob': password, 
            'Persist': win32cred.CRED_PERSIST_SESSION
        }
        
        try:
             win32cred.CredWrite(cred, 0)
             print(f"DEBUG: Temporarily saved credential for {server}")
        except Exception as e:
             messagebox.showerror("Credential Error", f"Failed to save credential to Windows Manager. Error: {e}")
             raise

    def _connect_manual_rdp(self):
        """
        Gathers data from manual entry fields, saves a temporary credential,
        and initiates the RDP connection.
        """
        server = self.server_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        
        if not server or not username or not password:
             messagebox.showwarning("Missing Information", "Please enter Server, Username, and Password to connect.")
             return
             
        if sys.platform != 'win32':
             messagebox.showerror("OS Error", "Manual connection with password injection is only supported on Windows.")
             return

        try:
            # 1. Save the password temporarily to Credential Manager
            self._save_temp_credential(server, username, password)
            
            # 2. Launch RDP, allowing it to find the *just-saved* credential
            manual_profile = {"Server": server, "Username": username}
            self._connect_rdp_from_card(manual_profile, password_provided=True)
            
            # 3. Clear the password field in the GUI
            self.password_var.set("")

        except Exception:
            pass 

    def _connect_rdp_from_card(self, profile, password_provided=False):
        # We ensure we use the FULL FQDN from the profile object here
        server = profile['Server'] 
        username = profile['Username']
        printer_setting = 0

        temp_rdp_file = os.path.join(os.environ['TEMP'], f"temp_rdp_launch_{os.getpid()}.rdp")
        
        prompt_for_creds = 0
        
        rdp_content = f"""
full address:s:{server}
username:s:{username}
prompt for credentials:i:{prompt_for_creds}
redirectprinters:i:{printer_setting}
enablecredsspsupport:i:1
authentication level:i:2
session bpp:i:24
"""
        try:
            with open(temp_rdp_file, 'w') as f:
                f.write(rdp_content.strip())
            
            subprocess.Popen(['mstsc.exe', temp_rdp_file], close_fds=True)

        except Exception as e:
            messagebox.showerror("Launch Error", f"Failed to launch RDP client.\nError: {e}")

    def list_rdp_credentials(self):
        if sys.platform != 'win32':
            print("DEBUG: Non-Windows platform. No RDP credentials will be loaded.", file=sys.stderr)
            return []

        try:
            all_creds = win32cred.CredEnumerate(None, 0)
        except Exception as e:
            messagebox.showerror("Access Error", f"Could not access Windows Credential Manager. Error: {e}")
            print(f"DEBUG: Credential Manager Access Failed: {e}", file=sys.stderr)
            return []

        rdp_profiles = []
        for cred in all_creds:
            target_name = cred['TargetName']
            if target_name.startswith(RDP_CREDENTIAL_PREFIX):
                server_address = target_name[len(RDP_CREDENTIAL_PREFIX):]
                user_name = cred['UserName']
                rdp_profiles.append({
                    # Store the FULL FQDN
                    "Server": server_address, 
                    "Username": user_name,
                    "TargetName": target_name
                })
        return rdp_profiles

    def _display_credentials(self):
        self.search_var.set("Search Server or Username...")
        
        if sys.platform != 'win32':
            self._clear_card_container()
            TkLabel(self.card_container, text="This application only works on Windows.", 
                      font=('Aptos', 14), background='#ffffff').grid(row=0, column=0, padx=20, pady=20)
            self.master_profiles_list = []
            return

        profiles = self.list_rdp_credentials()
        
        print(f"DEBUG: Found {len(profiles)} RDP profiles in Credential Manager.")
        
        if profiles:
            profiles.sort(key=lambda p: p['Server'].lower())
        
        self.master_profiles_list = profiles
        
        self._filter_list()

if __name__ == "__main__":
    
    # Check Dependencies (UNCHANGED)
    missing_deps = []
    try:
        import win32cred
    except ImportError:
        missing_deps.append("pywin32")
        
    if os.path.exists(LOGO_PATH):
        try:
              from PIL import Image, ImageTk
        except ImportError:
              missing_deps.append("Pillow")

    if missing_deps:
        messagebox.showerror("Dependency Error", 
                             "One or more required Python packages are missing. "
                             f"Please install them using: pip install {' '.join(missing_deps)}")
        sys.exit()

    root = Tk()
    app = RDPGUI(root)
    root.mainloop()
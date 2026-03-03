import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import random
import datetime
import os
try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# --- DATA ARCHIVE ---
SCENARIOS = [
    {"name": "Global Retailer", "req": "Home address for jacket delivery.", "type": "Personal", "correct": "CONTRACT", "img": "📦", "why": "Processing is necessary to perform a contract with the data subject."},
    {"name": "Social Connect", "req": "Track user across websites for targeted ads.", "type": "Personal", "correct": "CONSENT", "img": "🍪", "why": "Advertising is not a core necessity; requires clear, free consent."},
    {"name": "Safe-Work Corp", "req": "Recording employee fingerprints for server room access.", "type": "Sensitive", "correct": "EXPLICIT CONSENT", "img": "🆔", "why": "Biometric data is sensitive; requires a higher standard of explicit consent."},
    {"name": "City Health", "req": "Patient is unconscious; doctors need allergy data immediately.", "type": "Sensitive", "correct": "VITAL INTERESTS", "img": "🚑", "why": "Necessary to protect the life of the data subject."},
    {"name": "National Revenue", "req": "Reporting exact salary of all citizens for tax calculation.", "type": "Personal", "correct": "LEGAL OBLIGATION", "img": "🏦", "why": "Necessary to comply with a legal obligation of the controller."},
    {"name": "Charity Pulse", "req": "Keeping records of political affiliations for a non-profit.", "type": "Sensitive", "correct": "NON-PROFIT ORG", "img": "🗳️", "why": "Processing by a non-profit body in the course of its legitimate activities."}
]

PERSONAL_BASES = ["CONSENT", "CONTRACT", "LEGAL OBLIGATION", "VITAL INTERESTS", "PUBLIC INTEREST", "LEGITIMATE INTEREST"]
SENSITIVE_BASES = ["EXPLICIT CONSENT", "EMPLOYMENT LAW", "VITAL INTERESTS", "NON-PROFIT ORG", "LEGAL CLAIMS", "HEALTHCARE", "PUBLIC HEALTH"]
INVALID_BASES = ["BUNDLED CONSENT 🚩", "FORCED CONSENT 🚩", "INVISIBLE TRACKING 🚩"]

class NeonCityGame:
    def __init__(self, root):
        self.root = root
        self.root.title("NEON CITY: DATA ARCHITECT")
        self.root.geometry("1150x850")
        self.root.configure(bg="#020617")
        
        self.username = "Guest_Architect"
        self.trust = 100
        self.stability = 0
        self.codex_tries = 3
        self.warning_shown = False

        self.main_container = tk.Frame(self.root, bg="#020617")
        self.main_container.pack(fill="both", expand=True)

        self.codex_btn = tk.Button(self.root, text=f"🔓 ACCESS LEGAL CODEX ({self.codex_tries}/3)", 
                                   bg="#0f172a", fg="#38bdf8", font=("Courier", 10, "bold"), command=self.open_codex)
        self.codex_btn.pack(side="bottom", fill="x", pady=5)

        self.show_splash()

    def show_splash(self):
        """Display the cover image as a splash screen integrated into the main window."""
        try:
            # Withdraw main UI elements initially
            self.main_container.pack_forget()
            self.codex_btn.pack_forget()
            
            img_path = os.path.join(os.path.dirname(__file__), "assets", "cover.png")
            
            # Create splash frame in the main root window
            self.splash_frame = tk.Frame(self.root, bg="#020617")
            self.splash_frame.pack(fill="both", expand=True)
            
            # Get screen dimensions with margins
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            max_width = int(screen_width * 0.9)
            max_height = int(screen_height * 0.9)
            
            # Load and scale image
            if HAS_PIL:
                img = Image.open(img_path)
                # Calculate scaling to fit screen while maintaining aspect ratio
                img_ratio = img.width / img.height
                screen_ratio = max_width / max_height
                
                if img_ratio > screen_ratio:
                    # Image is wider, scale by width
                    new_width = max_width
                    new_height = int(max_width / img_ratio)
                else:
                    # Image is taller, scale by height
                    new_height = max_height
                    new_width = int(max_height * img_ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label = tk.Label(self.splash_frame, image=photo, bd=0, bg="#020617")
                label.image = photo  # keep a reference
                label.pack(expand=True)
            else:
                # Fallback: use tkinter's PhotoImage (no scaling available)
                photo = tk.PhotoImage(file=img_path)
                label = tk.Label(self.splash_frame, image=photo, bd=0, bg="#020617")
                label.image = photo
                label.pack(expand=True)
            
            def close_splash(event=None):
                try:
                    self.splash_frame.pack_forget()
                    self.splash_frame.destroy()
                except:
                    pass
                self.show_menu()
            
            # Close on click or after 2500ms
            self.splash_frame.after(2500, close_splash)
            self.splash_frame.bind("<Button-1>", close_splash)
            label.bind("<Button-1>", close_splash)
            self.root.update()  # process events to show splash
            
        except Exception as e:
            # If image fails to load, just show menu
            self.show_menu()

    def log_message(self, message, tag=None):
        self.log_terminal.config(state='normal')
        self.log_terminal.insert(tk.END, f"> {message}\n", tag)
        self.log_terminal.see(tk.END)
        self.log_terminal.config(state='disabled')

    def save_mission_log(self, status):
        badge = "ELITE ARCHITECT" if self.trust >= 80 else "STANDARD CONTROLLER"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        log_entry = f"[{timestamp}] User: {self.username} | Result: {status} | Trust: {self.trust}% | Rank: {badge}\n"
        try:
            with open("mission_logs.txt", "a", encoding="utf-8") as f:
                f.write(log_entry)
        except: pass

    def show_menu(self):
        # Restore main UI elements
        self.main_container.pack(fill="both", expand=True)
        self.codex_btn.pack(side="bottom", fill="x", pady=5)
        
        for w in self.main_container.winfo_children(): w.destroy()
        
        # --- HEADER ---
        tk.Label(self.main_container, text="🌃", font=("Arial", 60), bg="#020617").pack(pady=(40, 0))
        tk.Label(self.main_container, text="NEON CITY 2026", font=("Verdana", 42, "bold"), fg="#00f3ff", bg="#020617").pack()
        tk.Label(self.main_container, text="[ THE FOUNDATION OF TOMORROW ]", font=("Courier", 14, "bold"), fg="#f0abfc", bg="#020617").pack(pady=5)

        # --- THE LORE / MISSION TEXT ---
        story_frame = tk.Frame(self.main_container, bg="#0f172a", highlightbackground="#38bdf8", highlightthickness=1)
        story_frame.pack(pady=30, padx=80, fill="x")
        
        story_text = (
            "A new futuristic city is being built from the ground up. "
            "In this digital utopia, data is the concrete, and privacy is the steel. "
            "Your contributions as a Data Architect matter—every decision you make "
            "shapes the trust and stability of our rising society.\n\n"
            "Will you build a sanctuary of rights, or a surveillance nightmare?"
        )
        tk.Label(story_frame, text=story_text, font=("Verdana", 11), fg="#cbd5e1", bg="#0f172a", 
                 padx=40, pady=30, wraplength=700, justify="center").pack()

        # --- CONTROLS ---
        tk.Button(self.main_container, text="INITIALIZE NEURAL LINK", font=("Courier", 16, "bold"), 
                  bg="#00f3ff", fg="#020617", activebackground="#f0abfc", padx=40, pady=15, 
                  command=self.get_username).pack(pady=20)

    def get_username(self):
        name = simpledialog.askstring("Identity Verification", "Enter Architect ID:", parent=self.root)
        if name: self.username = name
        self.start_game()

    def start_game(self):
        for w in self.main_container.winfo_children(): w.destroy()
        self.stability = 0
        self.trust = 100
        
        # Screen Layout
        self.left_panel = tk.Frame(self.main_container, bg="#020617")
        self.left_panel.pack(side="left", fill="both", expand=True)
        
        self.right_panel = tk.Frame(self.main_container, bg="#010409", width=350)
        self.right_panel.pack(side="right", fill="y")
        
        tk.Label(self.right_panel, text="--- SYSTEM LOG ---", bg="#010409", fg="#38bdf8", font=("Courier", 10)).pack(pady=5)
        self.log_terminal = scrolledtext.ScrolledText(self.right_panel, bg="#010409", fg="#94a3b8", font=("Courier", 9), state='disabled', bd=0)
        self.log_terminal.pack(fill="both", expand=True)
        self.log_terminal.tag_config("success", foreground="#10b981")
        self.log_terminal.tag_config("fail", foreground="#ef4444")

        self.hud = tk.Frame(self.left_panel, bg="#0f172a", pady=15)
        self.hud.pack(fill="x")
        tk.Label(self.hud, text=f"OPERATOR: {self.username}", fg="#f0abfc", bg="#0f172a", font=("Courier", 10)).pack()
        self.trust_lbl = tk.Label(self.hud, text=f"TRUST: {self.trust}%", fg="#00f3ff", bg="#0f172a", font=("Courier", 12, "bold"))
        self.trust_lbl.pack(side="left", padx=30)
        self.stab_lbl = tk.Label(self.hud, text=f"STABILITY: {self.stability}/5", fg="#f0abfc", bg="#0f172a", font=("Courier", 12, "bold"))
        self.stab_lbl.pack(side="right", padx=30)

        self.game_area = tk.Frame(self.left_panel, bg="#020617", pady=40)
        self.game_area.pack(fill="both", expand=True)
        
        self.log_message(f"Neural link for {self.username} active. Building future...")
        self.next_round()

    def next_round(self):
        if self.stability >= 5:
            self.save_mission_log("SUCCESS")
            badge = "ELITE ARCHITECT 🎖️" if self.trust >= 80 else "STANDARD CONTROLLER"
            messagebox.showinfo("MISSION SUCCESS", f"ID: {self.username}\nFinal Trust: {self.trust}%\nRank: {badge}\nThe city stands strong thanks to you.")
            self.root.destroy()
            return

        self.curr = random.choice(SCENARIOS)
        for w in self.game_area.winfo_children(): w.destroy()
        
        tk.Label(self.game_area, text=self.curr['img'], font=("Arial", 80), bg="#020617").pack()
        tk.Label(self.game_area, text=f"REQUEST: {self.curr['name']}", font=("Courier", 14, "bold"), fg="#38bdf8", bg="#020617").pack()
        tk.Label(self.game_area, text=f"\"{self.curr['req']}\"", fg="#cbd5e1", font=("Verdana", 12, "italic"), wraplength=450, bg="#020617").pack(pady=20)
        
        btn_f = tk.Frame(self.game_area, bg="#020617")
        btn_f.pack()
        tk.Button(btn_f, text="PERSONAL", bg="#1e40af", fg="white", font=("Courier", 10, "bold"), width=15, pady=10, command=lambda: self.check_class("Personal")).pack(side="left", padx=10)
        tk.Button(btn_f, text="SENSITIVE", bg="#991b1b", fg="white", font=("Courier", 10, "bold"), width=15, pady=10, command=lambda: self.check_class("Sensitive")).pack(side="left", padx=10)

    def check_class(self, choice):
        if choice == self.curr['type']:
            self.log_message(f"Classification {choice} verified.", "success")
            self.render_legal_grid(choice)
        else:
            self.trust -= 15
            self.log_message(f"Classification error. Sector trust dropping.", "fail")
            self.update_stats("😔 WRONG TYPE!")

    def render_legal_grid(self, data_type):
        for w in self.game_area.winfo_children(): w.destroy()
        tk.Label(self.game_area, text="SELECT LEGAL JUSTIFICATION", fg="#fbbf24", bg="#020617", font=("Courier", 14, "bold")).pack(pady=15)
        
        pool = PERSONAL_BASES if data_type == "Personal" else SENSITIVE_BASES
        wrong = random.sample([x for x in pool if x != self.curr['correct']], 2)
        final_opts = [self.curr['correct']] + wrong + [random.choice(INVALID_BASES)]
        random.shuffle(final_opts)

        grid = tk.Frame(self.game_area, bg="#020617")
        grid.pack()
        for i, opt in enumerate(final_opts):
            tk.Button(grid, text=opt.upper(), bg="#1e293b", fg="white", font=("Courier", 9), width=30, pady=12,
                      command=lambda o=opt: self.process_result(o)).grid(row=i//2, column=i%2, padx=5, pady=5)

    def process_result(self, choice):
        if choice == self.curr['correct']:
            self.trust += 10
            self.stability += 1
            self.log_message(f"Audit Success: {choice} confirmed.", "success")
            self.update_stats("🚀 YES! ARCHITECT VERIFIED! +10 Points")
        else:
            penalty = 30 if "🚩" in choice else 15
            self.trust -= penalty
            self.log_message(f"Audit Failure: {choice} is illegal.", "fail")
            self.update_stats(f"😔 NO! FOUNDATION WEAKENED. -{penalty} Points")

    def update_stats(self, msg):
        messagebox.showinfo("NEURAL AUDIT", f"{msg}\n\nREASONING: {self.curr['why']}")
        self.trust_lbl.config(text=f"TRUST: {self.trust}%")
        self.stab_lbl.config(text=f"STABILITY: {self.stability}/5")
        
        if self.trust < 70:
            self.trust_lbl.config(fg="#ef4444")
            if not self.warning_shown:
                messagebox.showwarning("ALERT", "⚠️ SYSTEM TRUST CRITICAL!")
                self.warning_shown = True
        
        if self.trust <= 0:
            self.save_mission_log("FAILED")
            messagebox.showerror("SYSTEM COLLAPSE", "The Architect has failed. The city falls into chaos.")
            self.root.destroy()
        else:
            self.next_round()

    def open_codex(self):
        if self.codex_tries > 0:
            self.codex_tries -= 1
            self.codex_btn.config(text=f"🔓 LEGAL CODEX ({self.codex_tries}/3)")
            win = tk.Toplevel(self.root); win.configure(bg="#010409")
            txt = "PERSONAL (Art 6): Consent, Contract, Legal Duty, Vital Interests, Public Task, Legitimate Interest.\n\nSENSITIVE (Art 9): Explicit Consent, Health, Public Health, Non-Profit, Legal Claims."
            tk.Label(win, text=txt, fg="#38bdf8", bg="#010409", font=("Courier", 11), padx=20, pady=20, wraplength=400, justify="left").pack()

root = tk.Tk()
NeonCityGame(root)
root.mainloop()
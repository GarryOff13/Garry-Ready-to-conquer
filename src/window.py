"""
Garry - Main Window
A premium dark window with fade animation, glow border, and IST greeting.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

import customtkinter as ctk

from sidebar import RemindersSidebar


# --- Design tokens ---
BG          = "#0F1115"
BG_BAR      = "#161A20"
TEXT_MAIN   = "#E8EAED"
TEXT_MUTED  = "#8B949E"
ACCENT      = "#14B8A6"
ACCENT_GLOW = "#1F6B62"
DIVIDER     = "#242A33"

WINDOW_W_RATIO = 0.90
WINDOW_H       = 700
WINDOW_TITLE   = "Garry · Assistant"
IST            = ZoneInfo("Asia/Kolkata")

FADE_ENABLED   = True
FADE_STEPS     = 12
FADE_INTERVAL  = 15
MIN_ALPHA      = 0.0
MAX_ALPHA      = 1.0


def get_greeting():
    hour = datetime.now(IST).hour

    if 5 <= hour < 12:
        return "Good morning, Sir.", "Hope the coffee is strong and the bugs are few."
    elif 12 <= hour < 17:
        return "Good afternoon, Sir.", "Steady progress beats bursts of genius."
    elif 17 <= hour < 21:
        return "Good evening, Sir.", "Wrap up clean. Tomorrow-you will thank you."
    else:
        return "Good night, Sir.", "Rest is part of the work."


class GarryWindow(ctk.CTk):
    """
    One Tk root for the entire app. Starts hidden, gets shown/hidden by claps.
    Never destroyed - hidden with withdraw() and shown with deiconify().
    """

    def __init__(self):
        super().__init__()

        self.overrideredirect(True)
        self.configure(fg_color=BG)
        self.resizable(False, False)

        self._compute_geometry()

        # Hidden at start
        self.attributes("-alpha", MIN_ALPHA)
        self.withdraw()

        self._build_outer_glow()
        self._build_title_bar()
        self._build_content()
        self._build_status_bar()

        self._update_clock()

        # Keep a reference to the running pulse so we can cancel it
        self._clap_check_id = None

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def _compute_geometry(self):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        w = int(screen_w * WINDOW_W_RATIO)
        h = WINDOW_H
        x = (screen_w - w) // 2
        y = (screen_h - h) // 2

        self.geometry(f"{w}x{h}+{x}+{y}")

    # ------------------------------------------------------------------
    # Show / hide
    # ------------------------------------------------------------------

    def show_window(self):
        """Bring the window on-screen with fade-in. Safe to call repeatedly."""
        self.deiconify()
        self.update_idletasks()
        self.attributes("-topmost", True)
        self.lift()
        self.focus_force()
        if FADE_ENABLED:
            self._fade_in()
        else:
            self.attributes("-alpha", MAX_ALPHA)

    def hide_window(self):
        """Fade out and hide. Safe to call repeatedly."""
        if FADE_ENABLED:
            self._fade_out(self.withdraw)
        else:
            self.withdraw()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_outer_glow(self):
        glow = ctk.CTkFrame(self, fg_color=ACCENT_GLOW, corner_radius=0)
        glow.pack(fill="both", expand=True)

        inner = ctk.CTkFrame(glow, fg_color=BG, corner_radius=0)
        inner.pack(fill="both", expand=True, padx=1, pady=1)

        self._inner = inner

    def _build_title_bar(self):
        bar = ctk.CTkFrame(self._inner, fg_color=BG_BAR, height=44, corner_radius=0)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        title = ctk.CTkLabel(
            bar, text=f"  {WINDOW_TITLE}",
            font=("Segoe UI", 12, "bold"),
            text_color=TEXT_MAIN,
        )
        title.pack(side="left", padx=(12, 0))

        close_btn = ctk.CTkButton(
            bar, text="✕", width=44, height=44,
            fg_color=BG_BAR, hover_color="#2A1A1A",
            text_color=TEXT_MUTED, corner_radius=0,
            font=("Segoe UI", 12),
            command=self.hide_window,
        )
        close_btn.pack(side="right")

        for widget in (bar, title):
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._do_drag)

    def _build_content(self):
        content = ctk.CTkFrame(self._inner, fg_color=BG, corner_radius=0)
        content.pack(fill="both", expand=True)

        sidebar = RemindersSidebar(content)
        sidebar.pack(side="left", fill="y")

        ctk.CTkFrame(content, fg_color=DIVIDER, width=1, corner_radius=0).pack(
            side="left", fill="y"
        )

        main = ctk.CTkFrame(content, fg_color=BG, corner_radius=0)
        main.pack(side="left", fill="both", expand=True)

        greeting, wish = get_greeting()

        ctk.CTkLabel(
            main, text=greeting,
            font=("Segoe UI Light", 42),
            text_color=TEXT_MAIN,
        ).pack(pady=(150, 0))

        ctk.CTkLabel(
            main, text=wish,
            font=("Segoe UI", 13),
            text_color=TEXT_MUTED,
        ).pack(pady=(12, 0))

    def _build_status_bar(self):
        divider = ctk.CTkFrame(self._inner, fg_color=DIVIDER, height=1, corner_radius=0)
        divider.pack(fill="x", side="bottom")

        status = ctk.CTkFrame(self._inner, fg_color=BG, height=44, corner_radius=0)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)

        left = ctk.CTkFrame(status, fg_color=BG, corner_radius=0)
        left.pack(side="left", padx=20)

        ctk.CTkLabel(
            left, text="●", text_color=ACCENT,
            font=("Segoe UI", 14),
        ).pack(side="left")

        ctk.CTkLabel(
            left, text="  Listening",
            font=("Segoe UI", 11),
            text_color=TEXT_MUTED,
        ).pack(side="left")

        self.time_label = ctk.CTkLabel(
            status, text="",
            font=("Segoe UI", 11),
            text_color=TEXT_MUTED,
        )
        self.time_label.pack(side="right", padx=20)

    # ------------------------------------------------------------------
    # Fade
    # ------------------------------------------------------------------

    def _fade_in(self):
        def step(alpha):
            self.attributes("-alpha", alpha)
            if alpha < MAX_ALPHA:
                self.after(FADE_INTERVAL, step, alpha + (1.0 / FADE_STEPS))
            else:
                self.attributes("-alpha", MAX_ALPHA)

        step(MIN_ALPHA)

    def _fade_out(self, on_done):
        def step(alpha):
            self.attributes("-alpha", alpha)
            if alpha > MIN_ALPHA:
                self.after(FADE_INTERVAL, step, alpha - (1.0 / FADE_STEPS))
            else:
                self.attributes("-alpha", MIN_ALPHA)
                on_done()

        step(MAX_ALPHA)

    # ------------------------------------------------------------------
    # Behavior
    # ------------------------------------------------------------------

    def _update_clock(self):
        now = datetime.now(IST).strftime("%I:%M %p")
        self.time_label.configure(text=f"{now}  IST")
        self.after(1000, self._update_clock)

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_drag(self, event):
        x = self.winfo_x() + (event.x - self._drag_x)
        y = self.winfo_y() + (event.y - self._drag_y)
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    win = GarryWindow()
    win.show_window()
    win.mainloop()
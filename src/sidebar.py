"""
Garry - Reminders Sidebar
Left panel showing upcoming reminders.
(V1: display only. Add/edit comes in V2.)
"""

import customtkinter as ctk


SIDEBAR_BG   = "#0A0C10"
TEXT_MAIN    = "#E8EAED"
TEXT_MUTED   = "#8B949E"
ACCENT       = "#14B8A6"
DIVIDER      = "#242A33"

SIDEBAR_W    = 200


DUMMY_REMINDERS = [
    ("06:00 AM", "Wake up"),
    ("02:00 PM", "Review PR"),
    ("09:00 PM", "Read 10 pages"),
]


class RemindersSidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master,
            fg_color=SIDEBAR_BG,
            width=SIDEBAR_W,
            corner_radius=0,
        )
        self.pack_propagate(False)

        self._build_header()
        self._build_reminders()
        self._build_add_button()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=SIDEBAR_BG, corner_radius=0)
        header.pack(fill="x", pady=(20, 12), padx=16)

        ctk.CTkLabel(
            header,
            text="REMINDERS",
            font=("Segoe UI", 10, "bold"),
            text_color=TEXT_MUTED,
        ).pack(side="left")

    def _build_reminders(self):
        container = ctk.CTkFrame(self, fg_color=SIDEBAR_BG, corner_radius=0)
        container.pack(fill="x", padx=16)

        for time_str, label in DUMMY_REMINDERS:
            item = ctk.CTkFrame(container, fg_color=SIDEBAR_BG, corner_radius=0)
            item.pack(fill="x", pady=6)

            row = ctk.CTkFrame(item, fg_color=SIDEBAR_BG, corner_radius=0)
            row.pack(fill="x")

            ctk.CTkLabel(
                row,
                text="●",
                font=("Segoe UI", 9),
                text_color=ACCENT,
            ).pack(side="left", padx=(0, 6))

            ctk.CTkLabel(
                row,
                text=time_str,
                font=("Segoe UI", 10, "bold"),
                text_color=TEXT_MAIN,
            ).pack(side="left")

            ctk.CTkLabel(
                item,
                text=label,
                font=("Segoe UI", 11),
                text_color=TEXT_MUTED,
                anchor="w",
            ).pack(fill="x", padx=(16, 0), pady=(2, 0))

    def _build_add_button(self):
        btn = ctk.CTkButton(
            self,
            text="+  Add reminder",
            font=("Segoe UI", 11),
            fg_color="transparent",
            hover_color="#161A20",
            text_color=TEXT_MUTED,
            border_width=1,
            border_color=DIVIDER,
            corner_radius=4,
            height=32,
            state="disabled",
        )
        btn.pack(side="bottom", fill="x", padx=16, pady=16)
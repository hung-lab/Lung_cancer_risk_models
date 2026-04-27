"""
Chapter 6: Advanced Widgets for Dashboards
Example: Status Bars and Progress Indicators

This example demonstrates how to create professional status bars,
progress indicators, loading spinners, and notification systems
for dashboard applications.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
from datetime import datetime

# =============================================================================
# STATUS BAR COMPONENTS
# =============================================================================


class StatusBar(tk.Frame):
    """Professional status bar with multiple sections"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.status_sections = {}
        self.create_widgets()

    def create_widgets(self):
        """Create the status bar interface"""
        # Configure the status bar
        self.configure(relief="sunken", borderwidth=1)

        # Main status section (left)
        self.status_sections["main"] = tk.Label(
            self, text="Ready", anchor="w", relief="sunken", borderwidth=1
        )
        self.status_sections["main"].pack(
            side="left", fill="x", expand=True, padx=2, pady=1
        )

        # Progress section (center)
        self.status_sections["progress"] = tk.Label(
            self, text="", anchor="center", relief="sunken", borderwidth=1, width=15
        )
        self.status_sections["progress"].pack(side="left", padx=2, pady=1)

        # Time section (right)
        self.status_sections["time"] = tk.Label(
            self, text="", anchor="e", relief="sunken", borderwidth=1, width=20
        )
        self.status_sections["time"].pack(side="right", padx=2, pady=1)

        # Start time updates
        self.update_time()

    def set_status(self, message, section="main"):
        """Set status message for a specific section"""
        if section in self.status_sections:
            self.status_sections[section].configure(text=message)

    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.set_status(current_time, "time")
        self.after(1000, self.update_time)


class ProgressIndicator(tk.Frame):
    """Advanced progress indicator with multiple states"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar()
        self.is_indeterminate = False
        self.create_widgets()

    def create_widgets(self):
        """Create the progress indicator interface"""
        # Status label
        self.status_label = tk.Label(
            self, textvariable=self.status_var, font=("Arial", 9), anchor="w"
        )
        self.status_label.pack(fill="x", pady=(0, 2))

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            self,
            variable=self.progress_var,
            maximum=100,
            length=300,
            mode="determinate",
        )
        self.progress_bar.pack(fill="x", pady=(0, 2))

        # Percentage label
        self.percentage_label = tk.Label(
            self, text="0%", font=("Arial", 9, "bold"), anchor="e"
        )
        self.percentage_label.pack(anchor="e")

    def start_progress(self, status="Processing..."):
        """Start the progress indicator"""
        self.status_var.set(status)
        self.progress_var.set(0)
        self.is_indeterminate = False
        self.progress_bar.configure(mode="determinate")

    def update_progress(self, value, status=None):
        """Update progress value (0-100)"""
        self.progress_var.set(value)
        if status:
            self.status_var.set(status)
        self.percentage_label.configure(text=f"{int(value)}%")

    def start_indeterminate(self, status="Processing..."):
        """Start indeterminate progress"""
        self.status_var.set(status)
        self.is_indeterminate = True
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start(10)
        self.percentage_label.configure(text="")

    def stop_progress(self, status="Completed"):
        """Stop the progress indicator"""
        if self.is_indeterminate:
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
        self.status_var.set(status)
        self.progress_var.set(100)
        self.percentage_label.configure(text="100%")


class LoadingSpinner(tk.Canvas):
    """Animated loading spinner widget"""

    def __init__(self, parent, size=30, **kwargs):
        super().__init__(parent, width=size, height=size, **kwargs)
        self.size = size
        self.angle = 0
        self.is_spinning = False
        self.create_spinner()

    def create_spinner(self):
        """Create the spinner graphics"""
        # Clear canvas
        self.delete("all")

        # Calculate dimensions
        center = self.size // 2
        radius = (self.size - 4) // 2

        # Draw spinner segments
        for i in range(8):
            angle = i * 45 + self.angle
            start_angle = angle - 15
            end_angle = angle + 15

            # Calculate opacity based on position
            opacity = 1.0 - (i * 0.1)
            if opacity < 0.1:
                opacity = 0.1

            # Convert angle to radians
            start_rad = start_angle * 3.14159 / 180
            end_rad = end_angle * 3.14159 / 180

            # Calculate arc coordinates
            x1 = center + radius * 0.6 * (1 - abs(start_rad))
            y1 = center + radius * 0.6 * start_rad
            x2 = center + radius * (1 - abs(end_rad))
            y2 = center + radius * end_rad

            # Draw arc segment
            self.create_arc(
                center - radius,
                center - radius,
                center + radius,
                center + radius,
                start=start_angle,
                extent=30,
                fill="",
                outline="#3498DB",
                width=3,
                stipple="gray50" if opacity < 0.5 else "",
            )

    def start_spinning(self):
        """Start the spinner animation"""
        self.is_spinning = True
        self.animate()

    def stop_spinning(self):
        """Stop the spinner animation"""
        self.is_spinning = False

    def animate(self):
        """Animate the spinner"""
        if self.is_spinning:
            self.angle = (self.angle + 10) % 360
            self.create_spinner()
            self.after(50, self.animate)


class NotificationSystem(tk.Frame):
    """Notification system for displaying alerts and messages"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.notifications = []
        self.notification_id = 0
        self.create_widgets()

    def create_widgets(self):
        """Create the notification system interface"""
        # Notification area (initially empty)
        self.notification_area = tk.Frame(self)
        self.notification_area.pack(fill="both", expand=True)

    def show_notification(self, message, notification_type="info", duration=5000):
        """Show a notification message"""
        notification_id = self.notification_id
        self.notification_id += 1

        # Create notification frame
        notification_frame = tk.Frame(
            self.notification_area,
            relief="raised",
            borderwidth=1,
            bg=self.get_notification_color(notification_type),
        )
        notification_frame.pack(fill="x", padx=5, pady=2)

        # Icon and message
        icon_label = tk.Label(
            notification_frame,
            text=self.get_notification_icon(notification_type),
            font=("Arial", 12),
            bg=self.get_notification_color(notification_type),
            fg="white",
        )
        icon_label.pack(side="left", padx=5, pady=5)

        message_label = tk.Label(
            notification_frame,
            text=message,
            font=("Arial", 9),
            bg=self.get_notification_color(notification_type),
            fg="white",
            wraplength=300,
        )
        message_label.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # Close button
        close_btn = tk.Label(
            notification_frame,
            text="×",
            font=("Arial", 14, "bold"),
            bg=self.get_notification_color(notification_type),
            fg="white",
            cursor="hand2",
        )
        close_btn.pack(side="right", padx=5, pady=5)
        close_btn.bind(
            "<Button-1>", lambda e: self.close_notification(notification_frame)
        )

        # Store notification
        self.notifications.append(
            {
                "id": notification_id,
                "frame": notification_frame,
                "type": notification_type,
                "message": message,
            }
        )

        # Auto-close after duration
        if duration > 0:
            self.after(duration, lambda: self.close_notification(notification_frame))

        return notification_id

    def get_notification_color(self, notification_type):
        """Get color for notification type"""
        colors = {
            "info": "#3498DB",
            "success": "#2ECC71",
            "warning": "#F39C12",
            "error": "#E74C3C",
        }
        return colors.get(notification_type, colors["info"])

    def get_notification_icon(self, notification_type):
        """Get icon for notification type"""
        icons = {"info": "ℹ", "success": "✓", "warning": "⚠", "error": "✗"}
        return icons.get(notification_type, icons["info"])

    def close_notification(self, notification_frame):
        """Close a specific notification"""
        if notification_frame.winfo_exists():
            notification_frame.destroy()
            # Remove from notifications list
            self.notifications = [
                n for n in self.notifications if n["frame"] != notification_frame
            ]

    def clear_all_notifications(self):
        """Clear all notifications"""
        for notification in self.notifications:
            if notification["frame"].winfo_exists():
                notification["frame"].destroy()
        self.notifications.clear()


# =============================================================================
# DEMO APPLICATIONS
# =============================================================================


class StatusProgressDemo(tk.Frame):
    """Demo application showing status and progress features"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        """Create the demo interface"""
        # Title
        title_label = tk.Label(
            self,
            text="Status and Progress Indicators Demo",
            font=("Arial", 16, "bold"),
            fg="#2C3E50",
        )
        title_label.pack(pady=20)

        # Main content frame
        content_frame = tk.Frame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel - Controls
        left_panel = tk.LabelFrame(
            content_frame, text="Controls", font=("Arial", 12, "bold")
        )
        left_panel.pack(side="left", fill="y", padx=(0, 10))

        # Progress controls
        progress_frame = tk.LabelFrame(
            left_panel, text="Progress Controls", font=("Arial", 10)
        )
        progress_frame.pack(fill="x", padx=10, pady=10)

        # Start progress button
        start_btn = tk.Button(
            progress_frame, text="Start Progress", command=self.start_progress, width=15
        )
        start_btn.pack(pady=5)

        # Start indeterminate button
        indeterminate_btn = tk.Button(
            progress_frame,
            text="Start Indeterminate",
            command=self.start_indeterminate,
            width=15,
        )
        indeterminate_btn.pack(pady=5)

        # Stop progress button
        stop_btn = tk.Button(
            progress_frame, text="Stop Progress", command=self.stop_progress, width=15
        )
        stop_btn.pack(pady=5)

        # Status controls
        status_frame = tk.LabelFrame(
            left_panel, text="Status Controls", font=("Arial", 10)
        )
        status_frame.pack(fill="x", padx=10, pady=10)

        # Status messages
        status_messages = [
            "Ready",
            "Loading data...",
            "Processing request...",
            "Saving changes...",
            "Connection established",
            "Error occurred",
        ]

        for message in status_messages:
            btn = tk.Button(
                status_frame,
                text=message,
                command=lambda m=message: self.set_status(m),
                width=15,
            )
            btn.pack(pady=2)

        # Notification controls
        notification_frame = tk.LabelFrame(
            left_panel, text="Notifications", font=("Arial", 10)
        )
        notification_frame.pack(fill="x", padx=10, pady=10)

        # Notification buttons
        tk.Button(
            notification_frame,
            text="Info Message",
            command=lambda: self.show_notification(
                "This is an informational message.", "info"
            ),
            width=15,
        ).pack(pady=2)

        tk.Button(
            notification_frame,
            text="Success Message",
            command=lambda: self.show_notification(
                "Operation completed successfully!", "success"
            ),
            width=15,
        ).pack(pady=2)

        tk.Button(
            notification_frame,
            text="Warning Message",
            command=lambda: self.show_notification(
                "Please check your input data.", "warning"
            ),
            width=15,
        ).pack(pady=2)

        tk.Button(
            notification_frame,
            text="Error Message",
            command=lambda: self.show_notification(
                "An error occurred while processing.", "error"
            ),
            width=15,
        ).pack(pady=2)

        tk.Button(
            notification_frame,
            text="Clear All",
            command=self.clear_notifications,
            width=15,
        ).pack(pady=5)

        # Right panel - Display
        right_panel = tk.Frame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True)

        # Progress indicator
        progress_label = tk.Label(
            right_panel, text="Progress Indicator:", font=("Arial", 12, "bold")
        )
        progress_label.pack(anchor="w", pady=(0, 5))

        self.progress_indicator = ProgressIndicator(right_panel)
        self.progress_indicator.pack(fill="x", pady=(0, 20))

        # Loading spinner
        spinner_label = tk.Label(
            right_panel, text="Loading Spinner:", font=("Arial", 12, "bold")
        )
        spinner_label.pack(anchor="w", pady=(0, 5))

        spinner_frame = tk.Frame(right_panel)
        spinner_frame.pack(fill="x", pady=(0, 20))

        self.loading_spinner = LoadingSpinner(spinner_frame, size=40)
        self.loading_spinner.pack(side="left", padx=(0, 10))

        spinner_btn = tk.Button(
            spinner_frame, text="Toggle Spinner", command=self.toggle_spinner
        )
        spinner_btn.pack(side="left")

        # Notification area
        notification_label = tk.Label(
            right_panel, text="Notifications:", font=("Arial", 12, "bold")
        )
        notification_label.pack(anchor="w", pady=(0, 5))

        self.notification_system = NotificationSystem(right_panel)
        self.notification_system.pack(fill="both", expand=True)

        # Status bar at bottom
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x")

    def start_progress(self):
        """Start determinate progress"""
        self.progress_indicator.start_progress("Starting operation...")

        def progress_worker():
            for i in range(101):
                if i % 10 == 0:
                    self.after(
                        0,
                        self.progress_indicator.update_progress,
                        i,
                        f"Processing... {i}%",
                    )
                time.sleep(0.1)
            self.after(0, self.progress_indicator.stop_progress, "Operation completed!")

        thread = threading.Thread(target=progress_worker, daemon=True)
        thread.start()

    def start_indeterminate(self):
        """Start indeterminate progress"""
        self.progress_indicator.start_indeterminate("Processing in background...")

        def indeterminate_worker():
            time.sleep(3)
            self.after(
                0, self.progress_indicator.stop_progress, "Background task completed!"
            )

        thread = threading.Thread(target=indeterminate_worker, daemon=True)
        thread.start()

    def stop_progress(self):
        """Stop progress indicator"""
        self.progress_indicator.stop_progress("Stopped by user")

    def set_status(self, message):
        """Set status bar message"""
        self.status_bar.set_status(message)

    def show_notification(self, message, notification_type="info"):
        """Show a notification"""
        self.notification_system.show_notification(message, notification_type)

    def clear_notifications(self):
        """Clear all notifications"""
        self.notification_system.clear_all_notifications()

    def toggle_spinner(self):
        """Toggle the loading spinner"""
        if self.loading_spinner.is_spinning:
            self.loading_spinner.stop_spinning()
        else:
            self.loading_spinner.start_spinning()


# =============================================================================
# MAIN APPLICATION
# =============================================================================


class StatusProgressDemoApp:
    """Main application demonstrating status and progress features"""

    def __init__(self, root):
        self.root = root
        self.root.title("Status and Progress Indicators Demo")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")

        # Create demo
        self.demo = StatusProgressDemo(self.root)
        self.demo.pack(fill="both", expand=True)


def main():
    """Main application entry point"""
    # Create the main window
    root = tk.Tk()

    # Create the status/progress demo
    app = StatusProgressDemoApp(root)

    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

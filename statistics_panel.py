from tkinter import StringVar
from my_table import CustomTable
import customtkinter


class StatisticsPanel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure(fg_color=("white", "gray30"))
        self.title_font = ("Bahnschrift", 24)
        self.subtitle_font = ("Bahnschrift", 20)
        self.normal_font = ("Bahnschrift", 16)
        self.payments_frame = customtkinter.CTkFrame(
            self, fg_color=("Gray80", "Gray25"))
        self.sessions_frame = customtkinter.CTkFrame(
            self, fg_color=("Gray80", "Gray25"))

        self.total_amount = 0
        self.total_amount_strv = StringVar()

        self.cash_amount = 0
        self.cash_amount_strv = StringVar()

        self.paypal_amount_strv = StringVar()
        self.paypal_amount = 0

        self.card_amount_strv = StringVar()
        self.card_amount = 0

        self.bank_amount_strv = StringVar()
        self.bank_amount = 0

        self.receipts_amount_strv = StringVar()
        self.receipts_amount = 0

        self.unpaid_amount_strv = StringVar()
        self.unpaid_amount = 0

        self.num_of_all_sessions_strv = StringVar()
        self.num_of_all_sessions = 0

        self.num_of_cash_sessions_strv = StringVar()
        self.num_of_cash_sessions = 0

        self.num_of_paypal_sessions_strv = StringVar()
        self.num_of_paypal_sessions = 0

        self.num_of_card_sessions_strv = StringVar()
        self.num_of_card_sessions = 0

        self.num_of_bank_sessions_strv = StringVar()
        self.num_of_bank_sessions = 0

        self.num_of_receipts_sessions_strv = StringVar()
        self.num_of_receipts_sessions = 0

        self.num_of_unpaid_sessions_strv = StringVar()
        self.num_of_unpaid_sessions = 0

        # Payments Labels
        self.payments_label = customtkinter.CTkLabel(
            self.payments_frame, text="Πληρωμές", font=self.title_font)
        self.cash_price_sum_label = customtkinter.CTkLabel(
            self.payments_frame, text="Μετρητά:", font=self.subtitle_font, textvariable=self.cash_amount_strv)
        self.paypal_price_sum_label = customtkinter.CTkLabel(
            self.payments_frame, text="Paypal:", font=self.subtitle_font, textvariable=self.paypal_amount_strv)
        self.card_price_sum_label = customtkinter.CTkLabel(
            self.payments_frame, text="Κάρτα:", font=self.subtitle_font, textvariable=self.card_amount_strv)
        self.bank_price_sum_label = customtkinter.CTkLabel(
            self.payments_frame, text="Τράπεζα:", font=self.subtitle_font, textvariable=self.bank_amount_strv)
        self.unpaid_price_sum_label = customtkinter.CTkLabel(
            self.payments_frame, text="Ανεξόφλητα:", font=self.subtitle_font, textvariable=self.unpaid_amount_strv)
        self.total_price_sum_label = customtkinter.CTkLabel(
            self.payments_frame, text="Σύνολο:", font=self.subtitle_font,  textvariable=self.total_amount_strv)
        self.receipts_sum_label = customtkinter.CTkLabel(
            self.payments_frame, text="Αποδείξεις:", font=self.subtitle_font, textvariable=self.receipts_amount_strv)
        # Sessions Labels
        self.sessions_label = customtkinter.CTkLabel(
            self.sessions_frame, text="Συνεδρίες", font=self.title_font)
        self.total_sessions_sum_label = customtkinter.CTkLabel(
            self.sessions_frame, text="Συνεδρίες:", font=self.subtitle_font, textvariable=self.num_of_all_sessions_strv)
        self.cash_sessions_sum_label = customtkinter.CTkLabel(
            self.sessions_frame, text="Πληρωμή με μετρητά:", font=self.subtitle_font, textvariable=self.num_of_cash_sessions_strv)
        self.paypal_sessions_sum_label = customtkinter.CTkLabel(
            self.sessions_frame, text="Πληρωμή με Paypal:", font=self.subtitle_font, textvariable=self.num_of_paypal_sessions_strv)
        self.card_sessions_sum_label = customtkinter.CTkLabel(
            self.sessions_frame, text="Πληρωμή με κάρτα:", font=self.subtitle_font, textvariable=self.num_of_card_sessions_strv)
        self.bank_sessions_sum_label = customtkinter.CTkLabel(
            self.sessions_frame, text="Πληρωμή μέσω τράπεζας:", font=self.subtitle_font, textvariable=self.num_of_bank_sessions_strv)
        self.unpaid_sessions_sum_label = customtkinter.CTkLabel(
            self.sessions_frame, text="Ανεξόφλητες:", font=self.subtitle_font, textvariable=self.num_of_unpaid_sessions_strv)
        self.receipt_sessions_sum_label = customtkinter.CTkLabel(
            self.sessions_frame, text="Αποδείξεις:", font=self.subtitle_font, textvariable=self.num_of_receipts_sessions_strv)

        self.cash_percentage = 0
        self.paypal_percentage = 0
        self.card_percentage = 0
        self.bank_percentage = 0
        self.unpaid_percentage = 0
        self.receipts_percentage = 0

        self.cash_amount_percentage = 0
        self.paypal_amount_percentage = 0
        self.card_amount_percentage = 0
        self.bank_amount_percentage = 0
        self.unpaid_amount_percentage = 0
        self.receipts_amount_percentage = 0

        self.payment_widgets = [[self.payments_label],
                                [self.total_price_sum_label],
                                [self.cash_price_sum_label],
                                [self.paypal_price_sum_label],
                                [self.card_price_sum_label],
                                [self.bank_price_sum_label],
                                [self.receipts_sum_label],
                                [self.unpaid_price_sum_label]
                                ]
        self.session_widgets = [[self.sessions_label],
                                [self.total_sessions_sum_label],
                                [self.cash_sessions_sum_label],
                                [self.paypal_sessions_sum_label],
                                [self.card_sessions_sum_label],
                                [self.bank_sessions_sum_label],
                                [self.receipt_sessions_sum_label],
                                [self.unpaid_sessions_sum_label]
                                ]
        self.money_table = CustomTable(master=self.payments_frame, show_inactive=True, heading_names=(
            " ", "€", "%"), column_widths=(180, 150, 150), column_types=("text", "money", "percentage"))

        self.num_of_sessions_table = CustomTable(master=self.sessions_frame, show_inactive=True, heading_names=(
            " ", "Συνεδρίες", "%"), column_widths=(180, 150, 150), column_types=("text", "number", "percentage"))

        self.setup_tables()

        # self.pack_widgets()
        self.pack_tables()
        self.pack_frames()

    def format_money_integer(self, number):
        return f"{number:,}".replace(",", ".")+" €"

    def format_percentage(self, number):
        return f"{number}".replace(".", ",")+" %"

    def format_integer(self, number):
        return f"{number:,}".replace(",", ".")

    def setup_tables(self):
        # We need to unbind the <Configure> event in both tables because we are not using the searchboxes.
        self.money_table.table.unbind("<Configure>")
        self.num_of_sessions_table.table.unbind("<Configure>")
        # We need to set the command of the headings to None because we dont want sorting.
        for heading in self.money_table.heading_names:

            self.money_table.table.heading(heading, command=lambda: None)
        for heading in self.num_of_sessions_table.heading_names:

            self.num_of_sessions_table.table.heading(
                heading, command=lambda: None)
        # We dont need right click menus or double click events in the statistics panel.
        self.money_table.table.unbind("<Double-Button-1>")
        self.num_of_sessions_table.table.unbind("<Double-Button-1>")
        self.money_table.table.unbind("<Button-3>")
        self.num_of_sessions_table.table.unbind("<Button-3>")
        self.money_table.scrollbar.pack_forget()
        self.num_of_sessions_table.scrollbar.pack_forget()

    def pack_tables(self):
        for widget_a, widget_b in zip(self.money_table.search_entry_widgets, self.num_of_sessions_table.search_entry_widgets):
            widget_a.destroy()
            widget_b.destroy()
        self.money_table.searchboxes_frame.destroy()
        self.num_of_sessions_table.searchboxes_frame.destroy()

        self.money_table.pack(fill="x", expand=False,
                              side="left", padx=50, pady=10)
        self.num_of_sessions_table.pack(
            fill="x", expand=False, side="right", padx=50, pady=10)

    def pack_widgets(self):
        for row, widgets in enumerate(self.payment_widgets):
            for col, widget in enumerate(widgets):
                widget.pack(fill='none', expand=False, side="top")
        for row, widgets in enumerate(self.session_widgets):
            for col, widget in enumerate(widgets):
                widget.pack(fill='none', expand=False, side="top")

    def pack_frames(self):
        self.payments_frame.pack(
            fill="both", expand=True, side="left", anchor="center", padx=10, pady=10)
        self.sessions_frame.pack(
            fill="both", expand=True, side="right", anchor="center", padx=10, pady=10)

    def calculate_stats(self, data):

        self.reset_sums()
        self.reset_percentages()
        self.calculate_sums(data)
        self.calculate_percentages()
        self.set_texts()
        self.clear_tables()
        self.update_tables()

    def calculate_sums(self, data):
        for row in data:

            self.total_amount += int(row[3])
            self.num_of_all_sessions += 1
            if row[4] == "0":
                self.unpaid_amount += int(row[3])
                self.num_of_unpaid_sessions += 1
            elif row[4] == "1":
                self.cash_amount += int(row[3])
                self.num_of_cash_sessions += 1
            elif row[4] == "2":
                self.paypal_amount += int(row[3])
                self.num_of_paypal_sessions += 1
            elif row[4] == "3":
                self.card_amount += int(row[3])
                self.num_of_card_sessions += 1
            elif row[4] == "4":
                self.bank_amount += int(row[3])
                self.num_of_bank_sessions += 1
            if row[8] == "1":
                self.receipts_amount += int(row[9])
                self.num_of_receipts_sessions += 1

    def reset_percentages(self):
        self.cash_percentage = 0
        self.paypal_percentage = 0
        self.card_percentage = 0
        self.bank_percentage = 0
        self.unpaid_percentage = 0
        self.receipts_percentage = 0

        self.cash_amount_percentage = 0
        self.paypal_amount_percentage = 0
        self.card_amount_percentage = 0
        self.bank_amount_percentage = 0
        self.unpaid_amount_percentage = 0
        self.receipts_amount_percentage = 0

    def reset_sums(self):
        self.total_amount = 0
        self.cash_amount = 0
        self.paypal_amount = 0
        self.card_amount = 0
        self.bank_amount = 0
        self.unpaid_amount = 0
        self.receipts_amount = 0

        self.num_of_all_sessions = 0
        self.num_of_cash_sessions = 0
        self.num_of_paypal_sessions = 0
        self.num_of_card_sessions = 0
        self.num_of_bank_sessions = 0
        self.num_of_unpaid_sessions = 0
        self.num_of_receipts_sessions = 0

    def calculate_percentages(self):
        if self.total_amount == 0 or self.num_of_all_sessions == 0:
            self.reset_sums()
            self.reset_percentages()
            return
        self.cash_percentage = round(
            self.num_of_cash_sessions / self.num_of_all_sessions * 100, 1)
        self.paypal_percentage = round(
            self.num_of_paypal_sessions / self.num_of_all_sessions * 100, 1)
        self.card_percentage = round(
            self.num_of_card_sessions / self.num_of_all_sessions * 100, 1)
        self.bank_percentage = round(
            self.num_of_bank_sessions / self.num_of_all_sessions * 100, 1)
        self.unpaid_percentage = round(
            self.num_of_unpaid_sessions / self.num_of_all_sessions * 100, 1)
        self.receipts_percentage = round(
            self.num_of_receipts_sessions / self.num_of_all_sessions * 100, 1)

        self.cash_amount_percentage = round(
            self.cash_amount / self.total_amount * 100, 1)
        self.paypal_amount_percentage = round(
            self.paypal_amount / self.total_amount * 100, 1)
        self.card_amount_percentage = round(
            self.card_amount / self.total_amount * 100, 1)
        self.bank_amount_percentage = round(
            self.bank_amount / self.total_amount * 100, 1)
        self.unpaid_amount_percentage = round(
            self.unpaid_amount / self.total_amount * 100, 1)
        self.receipts_amount_percentage = round(
            self.receipts_amount / self.total_amount * 100, 1)

    def set_texts(self):
        self.total_amount_strv.set(f"Σύνολο: {self.total_amount}€")
        self.cash_amount_strv.set(
            f"Μετρητά: {self.cash_amount}€  {self.cash_amount_percentage}%")
        self.paypal_amount_strv.set(
            f"Paypal: {self.paypal_amount}€  {self.paypal_amount_percentage}%")
        self.card_amount_strv.set(
            f"Κάρτα: {self.card_amount}€  {self.card_amount_percentage}%")
        self.bank_amount_strv.set(
            f"Τράπεζα: {self.bank_amount}€  {self.bank_amount_percentage}%")
        self.receipts_amount_strv.set(
            f"Αποδείξεις: {self.receipts_amount}€  {self.receipts_amount_percentage}%")
        self.unpaid_amount_strv.set(
            f"Ανεξόφλητα: {self.unpaid_amount}€  {self.unpaid_amount_percentage}%")

        self.num_of_all_sessions_strv.set(
            f"Συνεδρίες: {self.num_of_all_sessions}")
        self.num_of_cash_sessions_strv.set(
            f"Συνεδρίες με μετρητά: {self.num_of_cash_sessions}  {self.cash_percentage}%")
        self.num_of_paypal_sessions_strv.set(
            f"Συνεδρίες με Paypal: {self.num_of_paypal_sessions}  {self.paypal_percentage}%")
        self.num_of_card_sessions_strv.set(
            f"Συνεδρίες με κάρτα: {self.num_of_card_sessions}  {self.card_percentage}%")
        self.num_of_bank_sessions_strv.set(
            f"Συνεδρίες με τράπεζα: {self.num_of_bank_sessions}  {self.bank_percentage}%")
        self.num_of_receipts_sessions_strv.set(
            f"Αποδείξεις: {self.num_of_receipts_sessions}  {self.receipts_percentage}%")
        self.num_of_unpaid_sessions_strv.set(
            f"Ανεξόφλητες: {self.num_of_unpaid_sessions}  {self.unpaid_percentage}%")

    def update_tables(self):
        money_data_list = []
        sessions_data_list = []

        money_data_list.append(("Μετρητά", self.format_money_integer(self.cash_amount),
                                self.format_percentage(self.cash_amount_percentage)))
        money_data_list.append(("Paypal", self.format_money_integer(self.paypal_amount),
                               self.format_percentage(self.paypal_amount_percentage)))
        money_data_list.append(("Κάρτα", self.format_money_integer(self.card_amount),
                                self.format_percentage(self.card_amount_percentage)))
        money_data_list.append(("Τράπεζα", self.format_money_integer(self.bank_amount),
                                self.format_percentage(self.bank_amount_percentage)))
        money_data_list.append(("Ανεξόφλητα", self.format_money_integer(self.unpaid_amount),
                                self.format_percentage(self.unpaid_amount_percentage)))
        money_data_list.append(("", "", ""))
        money_data_list.append(("Αποδείξεις", self.format_money_integer(self.receipts_amount),
                                self.format_percentage(self.receipts_amount_percentage)))
        money_data_list.append(
            ("Σύνολο", self.format_money_integer(self.total_amount), "100%"))
        money_data_list.append(("", "", ""))

        sessions_data_list.append(("Μετρητά", self.format_integer(self.num_of_cash_sessions),
                                   self.format_percentage(self.cash_percentage)))
        sessions_data_list.append(("Paypal", self.format_integer(self.num_of_paypal_sessions),
                                   self.format_percentage(self.paypal_percentage)))
        sessions_data_list.append(("Κάρτα", self.format_integer(self.num_of_card_sessions),
                                   self.format_percentage(self.card_percentage)))
        sessions_data_list.append(("Τράπεζα", self.format_integer(self.num_of_bank_sessions),
                                   self.format_percentage(self.bank_percentage)))
        sessions_data_list.append(("Ανεξόφλητες", self.format_integer(self.num_of_unpaid_sessions),
                                   self.format_percentage(self.unpaid_percentage)))
        sessions_data_list.append(("", "", ""))
        sessions_data_list.append(("Αποδείξεις", self.format_integer(self.num_of_receipts_sessions),
                                   self.format_percentage(self.receipts_percentage)))
        sessions_data_list.append(
            ("Σύνολο συνεδριών", self.format_integer(self.num_of_all_sessions), "100%"))
        sessions_data_list.append(("", "", ""))

        self.money_table.data = money_data_list
        self.money_table.filtered_data = money_data_list
        self.money_table.data_to_display = money_data_list
        self.num_of_sessions_table.data = sessions_data_list
        self.num_of_sessions_table.filtered_data = sessions_data_list
        self.num_of_sessions_table.data_to_display = sessions_data_list
        self.money_table.fill_table()
        self.num_of_sessions_table.fill_table()
        money_row_ids = self.money_table.table.get_children()
        sessions_row_ids = self.num_of_sessions_table.table.get_children()
        self.money_table.table.selection_set(money_row_ids[-2])
        self.num_of_sessions_table.table.selection_set(sessions_row_ids[-2])

    def clear_tables(self):
        for row in self.money_table.table.get_children():
            self.money_table.table.delete(row)
        for row in self.num_of_sessions_table.table.get_children():
            self.num_of_sessions_table.table.delete(row)


if __name__ == "__main__":
    appwindow = customtkinter.CTk()
    appwindow.title("Statistics Panel")
    appwindow.geometry("800x600")
    statistics_panel = StatisticsPanel(appwindow)
    statistics_panel.pack(fill="both", expand=True)
    appwindow.mainloop()

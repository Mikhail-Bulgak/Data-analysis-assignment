import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox, simpledialog

class ExcelApp:
    def __init__(self, root, frame_buttons, frame_table):
        self.root = root
        self.root.config(bg='#C9C5C5')  
        self.root.title("Excel Data Viewer")  
        
        # Загрузка данных
        self.df = None
        self.origin_df = None

        # UI элементы
        Button(frame_buttons, text="Загрузить файл Excel", width=25, height=2, bg='#B5B2B2', command=self.load_data).pack(side=TOP)
        Button(frame_buttons, text="Фильтр", width=25, height=2, bg='#B5B2B2', command=self.apply_filter).pack(side=TOP)
        Button(frame_buttons, text="Сортировка", width=25, height=2, bg='#B5B2B2', command=self.sort_data).pack(side=TOP)
        Button(frame_buttons, text="Отменить фильтр/сортировку", width=25, height=2, bg='#B5B2B2', command=self.drop_filter).pack(side=TOP)
        Button(frame_buttons, text="Сохранить в файл", width=25, height=2, bg='#B5B2B2', command=self.export_data).pack(side=TOP)
        
        self.tree = ttk.Treeview(frame_table, columns=(), show='headings')
        self.tree.grid(row=0, column=0, sticky=NSEW)

        xscrollbar = ttk.Scrollbar(frame_table,orient=HORIZONTAL,command=self.tree.xview)
        xscrollbar.grid(row=1, column=0, sticky=EW)
        self.tree.configure(xscrollcommand=xscrollbar.set)

        yscrollbar = ttk.Scrollbar(frame_table,orient=VERTICAL,command=self.tree.yview)
        yscrollbar.grid(row=0, column=1, sticky=NS)
        self.tree.configure(yscrollcommand=yscrollbar.set)

        

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            self.df = pd.read_excel(file_path)
            self.origin_df = pd.read_excel(file_path)
            self.update_tree()


    def update_tree(self):
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, stretch=NO, width=150, anchor=CENTER)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))
    

    def drop_filter(self):
        self.df = self.origin_df
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(self.df.columns)
        for column in self.tree["columns"]:
            self.tree.heading(column, text=column)
            self.tree.column(column, stretch=NO, width=150, anchor=CENTER)
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))


    def apply_filter(self):
        # Создадим окно фильтра        
        filter_window = tk.Tk()
        filter_window.title("Фильтр")
        filter_window.geometry('360x200')

        #Создание метки поля для фильтрации
        filter_column = tk.Label(filter_window, text="Выберите столбец:")
        filter_column.grid(column=0, row=0, sticky=W, padx=20, pady=10)

        #Создание выпадающего списка полей
        columns_list = list(self.df.columns)
        columns_combobox = ttk.Combobox(filter_window, values=columns_list)
        columns_combobox.grid(column=1, row=0, sticky=W, padx=20, pady=10)

        # Создание метки для выпадающего списка
        filter_label = tk.Label(filter_window, text="Выберите тип фильтра:")
        filter_label.grid(column=0, row=1, sticky=W, padx=20, pady=10)

        # Создание выпадающего списка
        filter_options = ["Больше", "Меньше", "Равно", "Больше или равно", "Меньше или равно", "Не равно", "Содержит"]
        filter_combobox = ttk.Combobox(filter_window, values=filter_options)
        filter_combobox.grid(column=1, row=1, sticky=W, padx=20, pady=10)
        filter_combobox.current(0)  # Устанавливаем "Больше" по умолчанию

        # Создание метки для значения
        value_label = tk.Label(filter_window, text="Введите значение:")
        value_label.grid(column=0, row=2, sticky=W, padx=20, pady=10)

        # Создание поля для ввода значения
        value_entry = tk.Entry(filter_window)
        value_entry.grid(column=1, row=2, sticky=W, padx=20, pady=10)

        def show_me():
            try:
                if columns_combobox.get() in self.df.columns:
                    if filter_combobox.get() == 'Больше':
                        filtered_df = self.df[self.df[columns_combobox.get()].astype(float) > float(value_entry.get())]
                        self.df = filtered_df
                        self.update_tree()
                        filter_window.destroy()
                    elif filter_combobox.get() == 'Меньше':
                        filtered_df = self.df[self.df[columns_combobox.get()].astype(float) < float(value_entry.get())]
                        self.df = filtered_df
                        self.update_tree()
                        filter_window.destroy()
                    elif filter_combobox.get() == 'Равно':
                        filtered_df = self.df[self.df[columns_combobox.get()].astype(float) == float(value_entry.get())]
                        self.df = filtered_df
                        self.update_tree()
                        filter_window.destroy()
                    elif filter_combobox.get() == 'Больше или равно':
                        filtered_df = self.df[self.df[columns_combobox.get()].astype(float) >= float(value_entry.get())]
                        self.df = filtered_df
                        self.update_tree()
                        filter_window.destroy()
                    elif filter_combobox.get() == 'Меньше или равно':
                        filtered_df = self.df[self.df[columns_combobox.get()].astype(float) <= float(value_entry.get())]
                        self.df = filtered_df
                        self.update_tree()
                        filter_window.destroy()
                    elif filter_combobox.get() == 'Не равно':
                        filtered_df = self.df[self.df[columns_combobox.get()].astype(float) != float(value_entry.get())]
                        self.df = filtered_df
                        self.update_tree() 
                        filter_window.destroy()
                    elif filter_combobox.get() == 'Содержит':
                        filtered_df = self.df[self.df[columns_combobox.get()].astype(str).str.contains(value_entry.get(), na=False)]
                        self.df = filtered_df
                        self.update_tree()
                        filter_window.destroy()
                    else:
                        messagebox.showerror("Ошибка", "Нельзя применить фильтр. Выберите другой.")
                else:
                    messagebox.showerror("Ошибка", "Нет столбца. Укажите столбец.")
            except ValueError:
                messagebox.showerror("Ошибка", "Нельзя применить фильтр. Выберите другой.")

        # Создание кнопки для применения фильтра
        Button(filter_window, text="Применить фильтр", command=show_me).grid(column=0, row=3, columnspan=2, padx=20, pady=10, sticky=NSEW)
           

    def sort_data(self):
        # Создадим окно сортировки        
        sort_window = tk.Tk()
        sort_window.title("Сортировка")
        sort_window.geometry('360x150')

        #Создание метки поля для сортировки
        sort_column = tk.Label(sort_window, text="Выберите столбец:")
        sort_column.grid(column=0, row=0, sticky=W, padx=15, pady=10)

        #Создание выпадающего списка полей
        columns_list = list(self.df.columns)
        columns_combobox = ttk.Combobox(sort_window, values=columns_list)
        columns_combobox.grid(column=1, row=0, sticky=W, padx=15, pady=10)

        # Создание метки для выпадающего списка
        sort_label = tk.Label(sort_window, text="Выберите тип сортировки:")
        sort_label.grid(column=0, row=1, sticky=W, padx=15, pady=10)

        # Создание выпадающего списка для сортировки
        sort_options = ["По возрастанию", "По убыванию"]
        sort_combobox = ttk.Combobox(sort_window, values=sort_options)
        sort_combobox.grid(column=1, row=1, sticky=W, padx=15, pady=10)

        def sort_me():
            try:
                if columns_combobox.get() in self.df.columns:
                    if sort_combobox.get() == "По возрастанию":
                        self.df = self.df.sort_values(by=columns_combobox.get(), ascending=True)
                        self.update_tree()
                        sort_window.destroy()
                    else:
                        self.df = self.df.sort_values(by=columns_combobox.get(), ascending=False)
                        self.update_tree()
                        sort_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Укажите столбец.")
            except:
                messagebox.showerror("Ошибка", "Нельзя применить сортировку.")

        # Создание кнопки для применения сортировки
        Button(sort_window, text="Применить сортировку", command=sort_me).grid(column=0, row=3, columnspan=2, padx=15, pady=10, sticky=NSEW)
        

    def export_data(self):
        export_all = messagebox.askyesno("Сохранить в файл", "Сохранить изменённые данные?")
        data_to_export = self.df if export_all else self.origin_df
        
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            data_to_export.to_excel(file_path, index=False)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены.")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1200x720')

    frame_buttons = Frame(root)
    frame_buttons.pack(side='left', fill='both')

    frame_table = Frame(root)
    frame_table.pack(side='right', fill='both')
    frame_table.grid_columnconfigure(0, weight=1)
    frame_table.grid_rowconfigure(0, weight=1)

    app = ExcelApp(root, frame_buttons, frame_table)
    root.mainloop()
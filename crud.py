from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pyodbc
from decouple import config
import sql

root = Tk()
root.title("Registro de empleados")
root.geometry("800x350")

# Variables de la tabla
id_t = StringVar()
nombre = StringVar()
cargo = StringVar()
salario = StringVar()

server = config('SERVER')
database = config('DATABASE')
username = config("USER")
password = config("PASSWORD")
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};' \
                   f'UID={username};PWD={password};Encrypt=yes;TrustServerCertificate=yes;'
try:
    conn = sql.connect(connectionString)
    miCursor = conn.cursor()
except pyodbc.Error as e:
    print("error connectandose a la base de datos")


def crear_tabla():
    columnas_tablas = ["ID INT PRIMARY KEY IDENTITY(1,1)", "NOMBRE VARCHAR(50) NOT NULL", "CARGO VARCHAR(50) NOT NULL",
                       "SALARIO INT NOT NULL"]

    try:
        # Crear la tabla solo si no existe
        sql.create_table("empleados", columnas_tablas, miCursor)
        messagebox.showinfo("Conexion", "Tabla creada exitosamente")

    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error al crear la base de datos o tabla: {e}")
        print("Error al crear la base de datos o tabla:", e)


# ==================Métodos CRUD============================
# Crear registro
def insertar_dato():
    nombre_columnas = ["NOMBRE", "CARGO", "SALARIO"]
    try:
        datos = nombre.get(), cargo.get(), salario.get()
        sql.insert_data("empleados", nombre_columnas, datos, miCursor)
        messagebox.showinfo("Exito", "Registro creado exitosamente")
    except pyodbc.Error as e:
        messagebox.showwarning("Error", f"Ocurrió un error al crear el registro: {e}")

    limpiarCampos()
    mostrar()


# Mostrar registros
def mostrar():
    registros = tree.get_children()

    for elemento in registros:
        tree.delete(elemento)

    try:
        rows = sql.get_all_data("empleados", miCursor)
        for row in rows:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3]))
        print("registros mostrados")
    except pyodbc.Error as e:
        print("Error al mostrar registros:", e)


# Actualizar registro
def actualizar():
    nombre_columnas = ["NOMBRE", "CARGO", "SALARIO"]
    try:
        datos = nombre.get(), cargo.get(), salario.get(), id_t.get()
        sql.update_data("empleados", nombre_columnas, datos, miCursor)
        messagebox.showinfo("Exito", "Registro actualizado exitosamente")
        mostrar()
    except pyodbc.Error as e:
        messagebox.showwarning("Error", f"Ocurrió un error al actualizar el registro: {e}")


# Eliminar registro
def eliminar():
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
            sql.delete_data("empleados", id_t.get(), miCursor)
    except pyodbc.Error as e:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al tratar de eliminar el registro")
        print(e)
        pass

    limpiarCampos()
    mostrar()


# ====================Funciones de los widgets de la ventana==============================
# Eliminar toda la base de datos
def eliminar_bd():
    if messagebox.askyesno(message="Los datos se perderán definitivamente, ¿desea continuar?", title="Advertencia"):
        miCursor.execute("DROP TABLE empleados")
    else:
        pass


def salir_aplicacion():
    valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir?")
    if valor == "yes":
        root.destroy()


def limpiarCampos():
    id_t.set("")
    nombre.set("")
    cargo.set("")
    salario.set("")


def AcercaDe():
    acerca = """
    Aplicacion CRUD SQL
    Version 1.0.0
    Tecnologia Python Tkinter
    """
    messagebox.showinfo(title="INFORMACION", message=acerca)


# ==================== widgets de la ventana==============================

menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear tabla de empleados", command=crear_tabla)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminar_bd)
menubasedat.add_command(label="Salir", command=salir_aplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=AcercaDe)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

# =======================Tabla=======================
tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2'))
tree.place(x=0, y=130)

tree.column('#0', width=100)
tree.heading('#0', text="id", anchor=CENTER)
tree.heading('#1', text="Nombre del empleado", anchor=CENTER)
tree.heading('#2', text="Cargo", anchor=CENTER)

tree.column('#3', width=100)
tree.heading('#3', text="Salario", anchor=CENTER)


def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)
    id_t.set(tree.item(item, "text"))
    nombre.set(tree.item(item, "values")[0])
    cargo.set(tree.item(item, "values")[1])
    salario.set(tree.item(item, "values")[2])


tree.bind("<Double-1>", seleccionarUsandoClick)

# ===========================Etiquetas y cajas de texto===========================
e1 = Entry(root, textvariable=id_t)

l2 = Label(root, text="Nombre")
l2.place(x=50, y=40)
e2 = Entry(root, textvariable=nombre, width=50)
e2.place(x=100, y=40)

l3 = Label(root, text="Cargo")
l3.place(x=50, y=70)
e3 = Entry(root, textvariable=cargo)
e3.place(x=100, y=70)

l4 = Label(root, text="Salario")
l4.place(x=280, y=70)
e4 = Entry(root, textvariable=salario, width=10)
e4.place(x=320, y=70)

l5 = Label(root, text="USD")
l5.place(x=380, y=70)

# =======================Botones============================
b1 = Button(root, text="Crear Registro", command=insertar_dato)
b1.place(x=50, y=90)
b2 = Button(root, text="Modificar Registro", command=actualizar)
b2.place(x=180, y=90)
b3 = Button(root, text="Mostrar Lista", command=mostrar)
b3.place(x=320, y=90)
b4 = Button(root, text="Eliminar Registro", bg="red", command=eliminar)
b4.place(x=450, y=90)


def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)
    id_t.set(tree.item(item, "text"))
    nombre.set(tree.item(item, "values")[0])
    cargo.set(tree.item(item, "values")[1])
    salario.set(tree.item(item, "values")[2])


tree.bind("<Double-1>", seleccionarUsandoClick)

root.config(menu=menubar)
root.mainloop()

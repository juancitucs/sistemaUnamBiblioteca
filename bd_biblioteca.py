import tkinter as tk
from tkinter import ttk, messagebox, Label, Entry, Button, Listbox, END, Toplevel
import mysql
from mysql.connector import Error
from tkcalendar import DateEntry


def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1",
            database="biblioteca_corregido",
            charset="utf8mb4",
            collation="utf8mb4_general_ci",
        )
        return conexion
    except Error as e:
        messagebox.showerror("Error", str(e))


def open_usuarios():
    window = tk.Toplevel()
    window.title("Lista Usuarios")

    usuario_tree = ttk.Treeview(
        window,
        columns=(
            "DNI",
            "Nombres",
            "Apellidos",
            "Correo",
            "Nro Celular",
            "Direccion",
            "Tipo de Usuario",
            "Estado",
        ),
        show="headings",
    )
    encabezados = [
        "DNI",
        "Nombres",
        "Apellidos",
        "Correo",
        "Nro Celular",
        "Direccion",
        "Tipo de Usuario",
        "Estado",
    ]
    for encabezado in encabezados:
        usuario_tree.heading(encabezado, text=encabezado)
        usuario_tree.column(encabezado, width=120, anchor=tk.W)
    usuario_tree.grid(column=0, row=1, columnspan=8, padx=10, pady=10)

    def cargar_usuario():
        for row in usuario_tree.get_children():
            usuario_tree.delete(row)

        conexion = conectar()  # Asumo que conectar() ya está implementado correctamente
        if conexion:
            cursor = conexion.cursor(buffered=True)  # No es necesario 'multi=True' aquí
            try:
                # Llama al procedimiento almacenado
                cursor.callproc("ObtenerUsuarios")

                # Recorre los resultados almacenados del procedimiento
                for result in cursor.stored_results():
                    for usuario in result.fetchall():  # Recupera los datos
                        usuario_tree.insert(
                            "", "end", values=usuario
                        )  # Llena el árbol con los datos

            except Error as e:
                messagebox.showerror(
                    "Error", f"No se pudieron cargar los usuarios:\n{e}"
                )
            finally:
                cursor.close()
                conexion.close()

    def registrar():
        window = tk.Toplevel()
        window.title("Registrar Usuarios")

        ttk.Label(window, text="DNI: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="Nombres: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_nom = ttk.Entry(window)
        entry_nom.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Apellidos: ").grid(column=0, row=2, pady=5, ipadx=5)
        entry_ape = ttk.Entry(window)
        entry_ape.grid(column=1, row=2, pady=5, ipadx=5)

        ttk.Label(window, text="Correo: ").grid(column=0, row=3, pady=5, ipadx=5)
        entry_correo = ttk.Entry(window)
        entry_correo.grid(column=1, row=3, pady=5, ipadx=5)

        ttk.Label(window, text="Nro Celular: ").grid(column=0, row=4, pady=5, ipadx=5)
        entry_nro = ttk.Entry(window)
        entry_nro.grid(column=1, row=4, pady=5, ipadx=5)

        ttk.Label(window, text="Dirección: ").grid(column=0, row=5, pady=5, ipadx=5)
        entry_direccion = ttk.Entry(window)
        entry_direccion.grid(column=1, row=5, pady=5, ipadx=5)

        def reg():
            if (
                not entry_dni.get()
                or not entry_nom.get()
                or not entry_ape.get()
                or not entry_nro.get()
                or not entry_correo.get()
                or not entry_direccion.get()
            ):
                messagebox.showerror("Error", "Se necesita llenar todos los campos")
                return
            conexion = conectar()
            cursor = conexion.cursor()
            valores = (
                entry_dni.get(),
                entry_nom.get(),
                entry_ape.get(),
                entry_correo.get(),
                entry_nro.get(),
                entry_direccion.get(),
            )
            try:
                cursor.callproc("ingresarUsuarios", valores)
                conexion.commit()
                limpiar()
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            except Error as e:
                messagebox.showerror("Error", str(e))
            finally:
                conexion.close()

        def limpiar():
            entry_dni.delete(0, tk.END)
            entry_nom.delete(0, tk.END)
            entry_ape.delete(0, tk.END)
            entry_correo.delete(0, tk.END)
            entry_nro.delete(0, tk.END)
            entry_direccion.delete(0, tk.END)

        ttk.Button(window, text="Registrar", command=reg).grid(
            column=1, row=7, pady=5, ipadx=5
        )

    def editar():
        window = tk.Toplevel()
        window.title("Editar Usuarios")

        ttk.Label(window, text="DNI: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="Nombres: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_nom = ttk.Entry(window)
        entry_nom.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Apellidos: ").grid(column=0, row=2, pady=5, ipadx=5)
        entry_ape = ttk.Entry(window)
        entry_ape.grid(column=1, row=2, pady=5, ipadx=5)

        ttk.Label(window, text="Correo: ").grid(column=0, row=3, pady=5, ipadx=5)
        entry_correo = ttk.Entry(window)
        entry_correo.grid(column=1, row=3, pady=5, ipadx=5)

        ttk.Label(window, text="Nro Celular: ").grid(column=0, row=4, pady=5, ipadx=5)
        entry_nro = ttk.Entry(window)
        entry_nro.grid(column=1, row=4, pady=5, ipadx=5)

        ttk.Label(window, text="Dirección: ").grid(column=0, row=5, pady=5, ipadx=5)
        entry_direccion = ttk.Entry(window)
        entry_direccion.grid(column=1, row=5, pady=5, ipadx=5)

        ttk.Label(window, text="Tipo de Usuario: ").grid(
            column=0, row=6, pady=5, ipadx=5
        )
        combo_tipo = ttk.Combobox(window, values=["estudiante", "docente", "externo"])
        combo_tipo.grid(column=1, row=6, pady=5, ipadx=5)
        combo_tipo.set("estudiante")

        ttk.Label(window, text="Cod Estudiante: ").grid(
            column=0, row=7, pady=5, ipadx=5
        )
        entry_cod_estudiante = ttk.Entry(window)
        entry_cod_estudiante.grid(column=1, row=7, pady=5, ipadx=5)

        ttk.Label(window, text="Ciclo: ").grid(column=0, row=8, pady=5, ipadx=5)
        combo_ciclo = ttk.Combobox(
            window, values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        )
        combo_ciclo.grid(column=1, row=8, pady=5, ipadx=5)
        combo_ciclo.set("")

        ttk.Label(window, text="Escuela Profesional: ").grid(
            column=0, row=9, pady=5, ipadx=5
        )
        combo_ep = ttk.Combobox(
            window,
            values=[
                "Ingeniería de Sistemas e Informatica",
                "Ingenieria Ambiental",
                "Ingieneria Pesquera",
                "Contabilidad",
                "Administración",
                "Derecho",
            ],
        )
        combo_ep.grid(column=1, row=9, pady=5, ipadx=5)
        combo_ep.set("")

        def limpiar():
            (entry_dni.delete(0, tk.END),)
            (entry_nom.delete(0, tk.END),)
            (entry_ape.delete(0, tk.END),)
            (entry_correo.delete(0, tk.END),)
            (entry_nro.delete(0, tk.END),)
            (entry_direccion.delete(0, tk.END),)
            (combo_tipo.delete(0, tk.END),)
            (entry_cod_estudiante.delete(0, tk.END),)
            (combo_ciclo.delete(0, tk.END),)
            (combo_ep.delete(0, tk.END),)
            entry_dni.delete(0, tk.END)

        def toggle_fields(event):
            if combo_tipo.get() == "estudiante":
                entry_cod_estudiante.config(state="normal")
                combo_ciclo.config(state="normal")
                combo_ep.config(state="normal")
            else:
                entry_cod_estudiante.config(state="disabled")
                combo_ciclo.config(state="disabled")
                combo_ep.config(state="disabled")

        combo_tipo.bind("<<ComboboxSelected>>", toggle_fields)

        def edit():
            if (
                not entry_dni.get()
                or not entry_nom.get()
                or not entry_ape.get()
                or not entry_correo.get()
                or not entry_nro.get()
                or not entry_direccion.get()
                or not combo_tipo.get()
            ):
                messagebox.showerror("Error", "Se necesita llenar todos los campos")
                return

            conexion = conectar()
            if conexion:
                cursor = conexion.cursor()
                if combo_tipo.get() == "estudiante":
                    valores = (
                        entry_nom.get(),
                        entry_ape.get(),
                        entry_correo.get(),
                        entry_nro.get(),
                        entry_direccion.get(),
                        combo_tipo.get(),
                        entry_cod_estudiante.get(),
                        combo_ciclo.get(),
                        combo_ep.get(),
                        entry_dni.get(),
                    )
                else:
                    valores = (
                        entry_nom.get(),
                        entry_ape.get(),
                        entry_correo.get(),
                        entry_nro.get(),
                        entry_direccion.get(),
                        combo_tipo.get(),
                        "",
                        "",
                        "",
                        entry_dni.get(),
                    )
                try:
                    cursor.callproc("ActualizarUsuario", valores)
                    conexion.commit()
                    limpiar()
                    messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                except Error as e:
                    messagebox.showerror(
                        "Error", f"Error al actualizar el usuario: {e}"
                    )
                finally:
                    conexion.close()

        ttk.Button(window, text="Guardar", command=edit).grid(
            column=1, row=10, pady=5, ipadx=5
        )

    def buscar():
        window = tk.Toplevel()
        window.title("Buscar Usuarios")

        ttk.Label(window, text="DNI: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="Nombres: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_nom = ttk.Entry(window)
        entry_nom.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Apellidos: ").grid(column=0, row=2, pady=5, ipadx=5)
        entry_ape = ttk.Entry(window)
        entry_ape.grid(column=1, row=2, pady=5, ipadx=5)

        ttk.Label(window, text="Correo: ").grid(column=0, row=3, pady=5, ipadx=5)
        entry_correo = ttk.Entry(window)
        entry_correo.grid(column=1, row=3, pady=5, ipadx=5)

        ttk.Label(window, text="Nro Celular: ").grid(column=0, row=4, pady=5, ipadx=5)
        entry_nro = ttk.Entry(window)
        entry_nro.grid(column=1, row=4, pady=5, ipadx=5)

        ttk.Label(window, text="Dirección: ").grid(column=0, row=5, pady=5, ipadx=5)
        entry_direccion = ttk.Entry(window)
        entry_direccion.grid(column=1, row=5, pady=5, ipadx=5)

        usuario_tree = ttk.Treeview(
            window,
            columns=(
                "DNI",
                "Nombres",
                "Apellidos",
                "Correo",
                "Nro Celular",
                "Direccion",
                "Tipo de Usuario",
                "Estado",
            ),
            show="headings",
        )
        encabezados = [
            "DNI",
            "Nombres",
            "Apellidos",
            "Correo",
            "Nro Celular",
            "Direccion",
            "Tipo de Usuario",
            "Estado",
        ]
        for encabezado in encabezados:
            usuario_tree.heading(encabezado, text=encabezado)
            usuario_tree.column(encabezado, width=120, anchor=tk.W)
        usuario_tree.grid(column=0, row=7, columnspan=8, padx=10, pady=10)

        def realizar_busqueda():
            for row in usuario_tree.get_children():
                usuario_tree.delete(row)

            conexion = conectar()
            if conexion:
                cursor = conexion.cursor()
                try:
                    # Crear una consulta dinámica basada en los campos llenados
                    query = """
                    SELECT dni, nombres, apellidos, correo, nro_celular, direccion, tipo_usuario, estado_bloqueo
                    FROM usuarios
                    WHERE 1=1
                    """
                    valores = []

                    if entry_dni.get():
                        query += " AND dni = %s"
                        valores.append(entry_dni.get())

                    if entry_nom.get():
                        query += " AND nombres LIKE %s"
                        valores.append(f"%{entry_nom.get()}%")

                    if entry_ape.get():
                        query += " AND apellidos LIKE %s"
                        valores.append(f"%{entry_ape.get()}%")

                    if entry_correo.get():
                        query += " AND correo LIKE %s"
                        valores.append(f"%{entry_correo.get()}%")

                    if entry_nro.get():
                        query += " AND nro_celular = %s"
                        valores.append(entry_nro.get())

                    if entry_direccion.get():
                        query += " AND direccion LIKE %s"
                        valores.append(f"%{entry_direccion.get()}%")

                    cursor.execute(query, valores)
                    for usuario in cursor.fetchall():
                        usuario_tree.insert("", tk.END, values=usuario)

                except Error as e:
                    messagebox.showerror(
                        "Error", f"No se pudo realizar la búsqueda:\n{e}"
                    )
                finally:
                    conexion.close()

        ttk.Button(window, text="Buscar", command=realizar_busqueda).grid(
            column=1, row=6, pady=10, ipadx=5
        )

    ttk.Button(window, text="Registrar", command=registrar).grid(
        column=1, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Editar", command=editar).grid(
        column=2, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Buscar", command=buscar).grid(
        column=3, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Actualizar", command=cargar_usuario).grid(
        column=4, row=0, pady=5, ipadx=5
    )
    cargar_usuario()


def open_prestamos():
    window = tk.Toplevel()
    window.title("Lista Prestamos")

    prestamos_tree = ttk.Treeview(
        window,
        columns=(
            "ID",
            "DNI",
            "Fecha Prest",
            "Fecha Devol",
            "Estado",
            "Cod libro",
            "Copias Adquiridas",
        ),
        show="headings",
    )
    encabezados = [
        "ID",
        "DNI",
        "Fecha Prest",
        "Fecha Devol",
        "Estado",
        "Cod libro",
        "Copias Adquiridas",
    ]
    for encabezado in encabezados:
        prestamos_tree.heading(encabezado, text=encabezado)
        prestamos_tree.column(encabezado, width=120, anchor=tk.W)
    prestamos_tree.grid(column=0, row=1, columnspan=7, padx=10, pady=10)

    def cargar_prestamos():
        for row in prestamos_tree.get_children():
            prestamos_tree.delete(row)
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                query = """
                SELECT *
                FROM prestamos
                """
                cursor.execute(query)
                for prestamos in cursor.fetchall():
                    prestamos_tree.insert("", tk.END, values=prestamos)
            except Error as e:
                messagebox.showerror(
                    "Error", f"No se pudieron cargar los prestamos:\n{e}"
                )
            finally:
                conexion.close()

    def registrar():
        window = tk.Toplevel()
        window.title("Registrar Prestamos")

        ttk.Label(window, text="DNI: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="Fecha Préstamo: ").grid(
            column=0, row=1, pady=5, ipadx=5
        )
        date_prestamo = DateEntry(
            window,
            width=20,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
        )
        date_prestamo.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Fecha Devolución: ").grid(
            column=0, row=2, pady=5, ipadx=5
        )
        date_devolucion = DateEntry(
            window,
            width=20,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
        )
        date_devolucion.grid(column=1, row=2, pady=5, ipadx=5)

        ttk.Label(window, text="Cod Libro: ").grid(column=0, row=3, pady=5, ipadx=5)
        entry_cod = ttk.Entry(window)
        entry_cod.grid(column=1, row=3, pady=5, ipadx=5)

        ttk.Label(window, text="Copias Adquiridas: ").grid(
            column=0, row=4, pady=5, ipadx=5
        )
        entry_copias = ttk.Entry(window)
        entry_copias.grid(column=1, row=4, pady=5, ipadx=5)

        def reg():
            if not entry_dni.get() or not entry_cod.get() or not entry_copias.get():
                messagebox.showerror("Error", "Se necesita llenar todos los campos")
                return
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO prestamos (dni, cod_libro, nro_copias_ad) VALUES(%s, %s, %s)"
            valores = (entry_dni.get(), entry_cod.get(), entry_copias.get())
            try:
                cursor.execute(sql, valores)
                conexion.commit()
                limpiar()
                messagebox.showinfo("Éxito", "Préstamo registrado exitosamente.")
            except Error as e:
                messagebox.showerror("Error", str(e))
            finally:
                conexion.close()

        def limpiar():
            entry_dni.delete(0, tk.END)
            entry_cod.delete(0, tk.END)
            entry_copias.delete(0, tk.END)

        ttk.Button(window, text="Registrar", command=reg).grid(
            column=1, row=7, pady=5, ipadx=5
        )

    def editar():
        window = tk.Toplevel()
        window.title("Editar Prestamo")

        ttk.Label(window, text="ID: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_id = ttk.Entry(window)
        entry_id.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="DNI: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Fecha Devolución: ").grid(
            column=0, row=2, pady=5, ipadx=5
        )
        date_devolucion = DateEntry(
            window,
            width=20,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
        )
        date_devolucion.grid(column=1, row=2, pady=5, ipadx=5)

        ttk.Label(window, text="Cod Libro: ").grid(column=0, row=3, pady=5, ipadx=5)
        entry_cod = ttk.Entry(window)
        entry_cod.grid(column=1, row=3, pady=5, ipadx=5)

        ttk.Label(window, text="Copias Adquiridas: ").grid(
            column=0, row=4, pady=5, ipadx=5
        )
        entry_copias = ttk.Entry(window)
        entry_copias.grid(column=1, row=4, pady=5, ipadx=5)

        def limpiar():
            entry_id.delete(0, tk.END)
            entry_dni.delete(0, tk.END)
            entry_cod.delete(0, tk.END)
            entry_copias.delete(0, tk.END)

        def edit():
            if (
                not entry_id.get()
                or not entry_dni.get()
                or not entry_cod.get()
                or not entry_copias.get()
            ):
                messagebox.showerror("Error", "Se necesita llenar todos los campos")
                return

            conexion = conectar()
            if conexion:
                cursor = conexion.cursor()
                sql = """
                        UPDATE prestamos 
                        SET dni=%s, fecha_dev=%s, cod_libro=%s, nro_copias_ad=%s
                        WHERE id_prestamos=%s
                    """
                valores = (
                    entry_dni.get(),
                    date_devolucion.get(),
                    entry_cod.get(),
                    entry_copias.get(),
                    entry_id.get(),
                )
                try:
                    cursor.execute(sql, valores)
                    conexion.commit()
                    limpiar()
                    messagebox.showinfo("Éxito", "Prestamo actualizado correctamente")
                except Error as e:
                    messagebox.showerror(
                        "Error", f"Error al actualizar el prestamo: {e}"
                    )
                finally:
                    conexion.close()

        ttk.Button(window, text="Guardar", command=edit).grid(
            column=1, row=6, pady=5, ipadx=5
        )

    def buscar():
        window = tk.Toplevel()
        window.title("Buscar Prestamo")

        ttk.Label(window, text="ID: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_id = ttk.Entry(window)
        entry_id.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="DNI: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Fecha Devolución: ").grid(
            column=0, row=2, pady=5, ipadx=5
        )
        date_devolucion = DateEntry(
            window,
            width=20,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
        )
        date_devolucion.grid(column=1, row=2, pady=5, ipadx=5)

        ttk.Label(window, text="Cod Libro: ").grid(column=0, row=3, pady=5, ipadx=5)
        entry_cod = ttk.Entry(window)
        entry_cod.grid(column=1, row=3, pady=5, ipadx=5)

        ttk.Label(window, text="Copias Adquiridas: ").grid(
            column=0, row=4, pady=5, ipadx=5
        )
        entry_copias = ttk.Entry(window)
        entry_copias.grid(column=1, row=4, pady=5, ipadx=5)

        prestamos_tree = ttk.Treeview(
            window,
            columns=(
                "ID",
                "DNI",
                "Fecha Devolución",
                "Código Libro",
                "Número de Copias",
            ),
            show="headings",
        )
        encabezados = [
            "ID",
            "DNI",
            "Fecha Devolución",
            "Código Libro",
            "Número de Copias",
        ]
        for encabezado in encabezados:
            prestamos_tree.heading(encabezado, text=encabezado)
            prestamos_tree.column(encabezado, width=140, anchor=tk.W)
        prestamos_tree.grid(column=0, row=6, columnspan=8, padx=10, pady=10)

        def realizar_busqueda():
            for row in prestamos_tree.get_children():
                prestamos_tree.delete(row)

            conexion = conectar()
            if conexion:
                cursor = conexion.cursor()
                try:
                    query = """
                        SELECT id_prestamos, dni, fecha_dev, cod_libro, nro_copias_ad
                        FROM prestamos
                        WHERE 1=1
                        """
                    valores = []

                    if entry_id.get():
                        query += " AND id_prestamos = %s"
                        valores.append(entry_id.get())

                    if entry_dni.get():
                        query += " AND dni = %s"
                        valores.append(entry_dni.get())

                    if date_devolucion.get_date():
                        query += " AND fecha_dev = %s"
                        valores.append(date_devolucion.get_date())

                    if entry_cod.get():
                        query += " AND cod_libro = %s"
                        valores.append(entry_cod.get())

                    if entry_copias.get():
                        query += " AND nro_copias_ad = %s"
                        valores.append(entry_copias.get())

                    cursor.execute(query, valores)
                    for prestamo in cursor.fetchall():
                        prestamos_tree.insert("", tk.END, values=prestamo)

                except Error as e:
                    messagebox.showerror(
                        "Error", f"No se pudo realizar la búsqueda:\n{e}"
                    )
                finally:
                    conexion.close()

        ttk.Button(window, text="Buscar", command=realizar_busqueda).grid(
            column=3, row=3, pady=5, ipadx=5
        )

    ttk.Button(window, text="Registrar", command=registrar).grid(
        column=1, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Editar", command=editar).grid(
        column=2, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Buscar", command=buscar).grid(
        column=3, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Actualizar", command=cargar_prestamos).grid(
        column=4, row=0, pady=5, ipadx=5
    )
    cargar_prestamos()


def open_devoluciones():
    window = tk.Toplevel()
    window.title("Lista Devoluciones")

    devoluciones_tree = ttk.Treeview(
        window,
        columns=("ID", "ID Prestamo", "DNI", "Estado del Libro", "Fecha de Devolucion"),
        show="headings",
    )
    encabezados = [
        "ID",
        "ID Prestamo",
        "DNI",
        "Estado del Libro",
        "Fecha de Devolucion",
    ]
    for encabezado in encabezados:
        devoluciones_tree.heading(encabezado, text=encabezado)
        devoluciones_tree.column(encabezado, width=120, anchor=tk.W)
    devoluciones_tree.grid(column=0, row=1, columnspan=5, padx=10, pady=10)

    def registrar():
        window = tk.Toplevel()
        window.title("Registrar Devoluciones")

        ttk.Label(window, text="DNI: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="ID Prestamo: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_ip = ttk.Entry(window)
        entry_ip.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Estado Libro: ").grid(column=0, row=2, pady=5, ipadx=5)
        combo_estado = ttk.Combobox(
            window, values=["En perfectas condiciones", "Dañado"]
        )
        combo_estado.grid(column=1, row=2, pady=5, ipadx=5)
        combo_estado.set("")

        ttk.Label(window, text="Fecha Devolucion: ").grid(
            column=0, row=3, pady=5, ipadx=5
        )
        date_dev = DateEntry(
            window,
            width=20,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
        )
        date_dev.grid(column=1, row=3, pady=5, ipadx=5)

        def reg():
            if (
                not entry_dni.get()
                or not combo_estado.get()
                or not entry_ip.get()
                or not date_dev.get()
            ):
                messagebox.showerror("Error", "Se necesita llenar todos los campos")
                return
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO devoluciones (dni, id_prest, estado_libro, fecha_dev) VALUES(%s, %s, %s, %s)"
            valores = (
                entry_dni.get(),
                entry_ip.get(),
                combo_estado.get(),
                date_dev.get(),
            )
            try:
                cursor.execute(sql, valores)
                conexion.commit()
                messagebox.showinfo("Éxito", "Devolucion registrada exitosamente.")
                limpiar()
            except Error as e:
                messagebox.showerror("Error", str(e))
            finally:
                conexion.close()

        def limpiar():
            entry_dni.delete(0, tk.END)
            entry_ip.delete(0, tk.END)
            combo_estado.delete(0, tk.END)

        ttk.Button(window, text="Registrar", command=reg).grid(
            column=1, row=5, pady=5, ipadx=5
        )

    def editar():
        window = tk.Toplevel()
        window.title("Editar Devoluciones")

        ttk.Label(window, text="ID: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_id = ttk.Entry(window)
        entry_id.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="ID Prestamo: ").grid(column=0, row=2, pady=5, ipadx=5)
        entry_ip = ttk.Entry(window)
        entry_ip.grid(column=1, row=2, pady=5, ipadx=5)

        ttk.Label(window, text="DNI: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Estado Libro: ").grid(column=0, row=3, pady=5, ipadx=5)
        combo_estado = ttk.Combobox(
            window, values=["En perfectas condiciones", "Dañado"]
        )
        combo_estado.grid(column=1, row=3, pady=5, ipadx=5)
        combo_estado.set("")

        ttk.Label(window, text="Fecha Devolucion: ").grid(
            column=0, row=4, pady=5, ipadx=5
        )
        date_dev = DateEntry(
            window,
            width=20,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
        )
        date_dev.grid(column=1, row=4, pady=5, ipadx=5)

        def limpiar():
            entry_id.delete(0, tk.END)
            entry_dni.delete(0, tk.END)
            entry_ip.delete(0, tk.END)
            combo_estado.delete(0, tk.END)

        def edit():
            if (
                not entry_id.get()
                or not entry_dni.get()
                or not combo_estado.get()
                or not entry_ip.get()
            ):
                messagebox.showerror("Error", "Se necesita llenar todos los campos")
                return
            conexion = conectar()
            if conexion:
                cursor = conexion.cursor()
                sql = """
                        UPDATE devoluciones
                        SET dni=%s, id_prest=%s, fecha_dev=%s, estado_libro=%s
                        WHERE id_dev=%s
                    """
                valores = (
                    entry_dni.get(),
                    entry_ip.get(),
                    date_dev.get(),
                    combo_estado.get(),
                    entry_id.get(),
                )
                try:
                    cursor.execute(sql, valores)
                    conexion.commit()
                    (limpiar(),)
                    messagebox.showinfo("Éxito", "Devolucion actualizada correctamente")
                except Error as e:
                    messagebox.showerror(
                        "Error", f"Error al actualizar el prestamo: {e}"
                    )
                finally:
                    conexion.close()

        ttk.Button(window, text="Guardar", command=edit).grid(
            column=1, row=5, pady=5, ipadx=5
        )

    def cargar_devoluciones():
        for row in devoluciones_tree.get_children():
            devoluciones_tree.delete(row)
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                query = """
                SELECT *
                FROM devoluciones
                """
                cursor.execute(query)
                for devoluciones in cursor.fetchall():
                    devoluciones_tree.insert("", tk.END, values=devoluciones)
            except Error as e:
                messagebox.showerror(
                    "Error", f"No se pudieron cargar las devoluciones:\n{e}"
                )
            finally:
                conexion.close()

    ttk.Button(window, text="Registrar", command=registrar).grid(
        column=1, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Editar", command=editar).grid(
        column=2, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Buscar", command=conectar).grid(
        column=3, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Actualizar", command=cargar_devoluciones).grid(
        column=4, row=0, pady=5, ipadx=5
    )
    cargar_devoluciones()


def open_libros():
    window = tk.Toplevel()
    window.title("Lista Libros")

    libros_tree = ttk.Treeview(
        window,
        columns=(
            "Cod Libro",
            "Libro",
            "Autor",
            "Año de Publicacion",
            "Edicion",
            "Copias",
        ),
        show="headings",
    )
    encabezados = [
        "Cod Libro",
        "Libro",
        "Autor",
        "Año de Publicacion",
        "Edicion",
        "Copias",
    ]
    for encabezado in encabezados:
        libros_tree.heading(encabezado, text=encabezado)
        libros_tree.column(encabezado, width=120, anchor=tk.W)
    libros_tree.grid(column=0, row=1, columnspan=6, padx=10, pady=10)

    def cargar_libros():
        for row in libros_tree.get_children():
            libros_tree.delete(row)
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                query = """
                SELECT cod_libro, nom_libro, nom_autor, año_public, edicion, copias_libro
                FROM libros
                """
                cursor.execute(query)
                for libros in cursor.fetchall():
                    libros_tree.insert("", tk.END, values=libros)
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los libros:\n{e}")
            finally:
                conexion.close()

    ttk.Button(window, text="Registrar", command=conectar).grid(
        column=1, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Editar", command=conectar).grid(
        column=2, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Eliminar", command=conectar).grid(
        column=3, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Buscar", command=conectar).grid(
        column=4, row=0, pady=5, ipadx=5
    )
    cargar_libros()


def open_infracciones():
    window = tk.Toplevel()
    window.title("Lista Infracciones")

    infracciones_tree = ttk.Treeview(
        window,
        columns=(
            "ID",
            "DNI",
            "Tipo",
            "ID Prest",
            "Fecha de la Infraccion",
            "Estado de Bloqueo",
        ),
        show="headings",
    )
    encabezados = [
        "ID",
        "DNI",
        "Tipo",
        "ID Prest",
        "Fecha de la Infraccion",
        "Estado de Bloqueo",
    ]
    for encabezado in encabezados:
        infracciones_tree.heading(encabezado, text=encabezado)
        infracciones_tree.column(encabezado, width=120, anchor=tk.W)
    infracciones_tree.grid(column=0, row=1, columnspan=5, padx=10, pady=10)

    def cargar_infracciones():
        for row in infracciones_tree.get_children():
            infracciones_tree.delete(row)
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()
            try:
                query = """
                SELECT id_infraccion, dni, tipo_infraccion, id_prest, fecha_infraccion, nivel_bloqueo
                FROM infracciones
                """
                cursor.execute(query)
                for infracciones in cursor.fetchall():
                    infracciones_tree.insert("", tk.END, values=infracciones)
            except Error as e:
                messagebox.showerror("Error", f"No se pudieron cargar los libros:\n{e}")
            finally:
                conexion.close()

    def registrar():
        window = tk.Toplevel()
        window.title("Registrar Infracciones")

        ttk.Label(window, text="DNI: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="ID Prestamo: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_ip = ttk.Entry(window)
        entry_ip.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="Tipo de Infraccion: ").grid(
            column=0, row=2, pady=5, ipadx=5
        )
        combo_tipo = ttk.Combobox(window, values=["retraso", "mal_estado", "otro"])
        combo_tipo.grid(column=1, row=2, pady=5, ipadx=5)
        combo_tipo.set("")

        ttk.Label(window, text="Fecha Infraccion: ").grid(
            column=0, row=3, pady=5, ipadx=5
        )
        date_infraccion = DateEntry(
            window,
            width=20,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
        )
        date_infraccion.grid(column=1, row=3, pady=5, ipadx=5)

        ttk.Label(window, text="Nivel de Bloqueo: ").grid(
            column=0, row=4, pady=5, ipadx=5
        )
        combo_nivel = ttk.Combobox(
            window, values=["1_dia", "1_semana", "1_mes", "permanente"]
        )
        combo_nivel.grid(column=1, row=4, pady=5, ipadx=5)
        combo_nivel.set("")

        ttk.Label(window, text="Observaciones: ").grid(column=0, row=5, pady=5, ipadx=5)
        entry_observaciones = ttk.Entry(window)
        entry_observaciones.grid(column=1, row=5, pady=5, ipadx=5)

        def reg():
            if (
                not entry_dni.get()
                or not combo_tipo.get()
                or not combo_nivel.get()
                or not entry_observaciones.get()
                or not entry_ip.get()
            ):
                messagebox.showerror("Error", "Se necesita llenar todos los campos")
                return
            conexion = conectar()
            cursor = conexion.cursor()
            sql = "INSERT INTO infracciones (dni, tipo_infraccion, id_prest, nivel_bloqueo, observaciones) VALUES(%s, %s, %s, %s, %s)"
            valores = (
                entry_dni.get(),
                combo_tipo.get(),
                entry_ip.get(),
                combo_nivel.get(),
                entry_observaciones.get(),
            )
            try:
                cursor.execute(sql, valores)
                conexion.commit()
                messagebox.showinfo("Éxito", "Infraccion registrado exitosamente.")
                limpiar()
            except Error as e:
                messagebox.showerror("Error", str(e))
            finally:
                conexion.close()

        def limpiar():
            entry_dni.delete(0, tk.END)
            entry_ip.delete(0, tk.END)
            combo_tipo.delete(0, tk.END)
            combo_nivel.delete(0, tk.END)
            entry_observaciones.delete(0, tk.END)

        ttk.Button(window, text="Registrar", command=reg).grid(
            column=1, row=6, pady=5, ipadx=5
        )

    def editar():
        window = tk.Toplevel()
        window.title("Editar Infracciones")

        ttk.Label(window, text="ID: ").grid(column=0, row=0, pady=5, ipadx=5)
        entry_id = ttk.Entry(window)
        entry_id.grid(column=1, row=0, pady=5, ipadx=5)

        ttk.Label(window, text="DNI: ").grid(column=0, row=1, pady=5, ipadx=5)
        entry_dni = ttk.Entry(window)
        entry_dni.grid(column=1, row=1, pady=5, ipadx=5)

        ttk.Label(window, text="ID Prestamo: ").grid(column=0, row=2, pady=5, ipadx=5)
        entry_ip = ttk.Entry(window)
        entry_ip.grid(column=1, row=2, pady=5, ipadx=5)

        ttk.Label(window, text="Tipo de Infraccion: ").grid(
            column=0, row=3, pady=5, ipadx=5
        )
        combo_tipo = ttk.Combobox(window, values=["retraso", "mal_estado", "otro"])
        combo_tipo.grid(column=1, row=3, pady=5, ipadx=5)
        combo_tipo.set("")

        ttk.Label(window, text="Fecha Infraccion: ").grid(
            column=0, row=4, pady=5, ipadx=5
        )
        date_infraccion = DateEntry(
            window,
            width=20,
            background="darkblue",
            foreground="white",
            date_pattern="yyyy-mm-dd",
        )
        date_infraccion.grid(column=1, row=4, pady=5, ipadx=5)

        ttk.Label(window, text="Nivel de Bloqueo: ").grid(
            column=0, row=5, pady=5, ipadx=5
        )
        combo_nivel = ttk.Combobox(
            window, values=["1_dia", "1_semana", "1_mes", "permanente"]
        )
        combo_nivel.grid(column=1, row=5, pady=5, ipadx=5)
        combo_nivel.set("")

        ttk.Label(window, text="Observaciones: ").grid(column=0, row=6, pady=5, ipadx=5)
        entry_observaciones = ttk.Entry(window)
        entry_observaciones.grid(column=1, row=6, pady=5, ipadx=5)

        def limpiar():
            entry_id.delete(0, tk.END)
            entry_dni.delete(0, tk.END)
            entry_ip.delete(0, tk.END)
            combo_tipo.delete(0, tk.END)
            combo_nivel.delete(0, tk.END)
            entry_observaciones.delete(0, tk.END)

        def edit():
            if (
                not entry_id.get()
                or not entry_dni.get()
                or not combo_tipo.get()
                or not entry_ip.get()
                or not combo_nivel.get()
                or not entry_observaciones.get()
            ):
                messagebox.showerror("Error", "Se necesita llenar todos los campos")
                return

            conexion = conectar()
            if conexion:
                cursor = conexion.cursor()
                sql = """
                        UPDATE infracciones 
                        SET dni=%s, tipo_infraccion=%s, id_prest=%s, fecha_infraccion=%s, nivel_bloqueo=%s, observaciones=%s
                        WHERE id_infraccion=%s
                    """
                valores = (
                    entry_dni.get(),
                    combo_tipo.get(),
                    entry_ip.get(),
                    date_infraccion.get(),
                    combo_nivel.get(),
                    entry_observaciones.get(),
                    entry_id.get(),
                )
                try:
                    cursor.execute(sql, valores)
                    conexion.commit()
                    (limpiar(),)
                    messagebox.showinfo("Éxito", "Infraccion actualizado correctamente")
                except Error as e:
                    messagebox.showerror(
                        "Error", f"Error al actualizar el prestamo: {e}"
                    )
                finally:
                    conexion.close()

        ttk.Button(window, text="Guardar", command=edit).grid(
            column=1, row=7, pady=5, ipadx=5
        )

    ttk.Button(window, text="Registrar", command=registrar).grid(
        column=1, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Editar", command=editar).grid(
        column=2, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Buscar", command=conectar).grid(
        column=3, row=0, pady=5, ipadx=5
    )
    ttk.Button(window, text="Actualizar", command=cargar_infracciones).grid(
        column=4, row=0, pady=5, ipadx=5
    )
    cargar_infracciones()


app = tk.Tk()
app.title("Menú Principal")
app.geometry("200x350")
app.resizable(False, False)

menu_frame = ttk.Frame(app, padding="20")
menu_frame.grid(column=0, row=0, sticky="NSEW")
ttk.Label(menu_frame, text="Menú Principal", font=("Helvetica", 16, "bold")).grid(
    column=0, row=0, pady=20
)
menu_frame.columnconfigure(0, weight=1)
menu_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)

ttk.Button(menu_frame, text="Gestionar Usuarios", command=open_usuarios).grid(
    column=0, row=1, pady=10, ipadx=10
)
ttk.Button(menu_frame, text="Gestionar Prestamos", command=open_prestamos).grid(
    column=0, row=2, pady=10, ipadx=10
)
ttk.Button(menu_frame, text="Gestionar Devoluciones", command=open_devoluciones).grid(
    column=0, row=3, pady=10, ipadx=10
)
ttk.Button(menu_frame, text="Gestionar Libros", command=open_libros).grid(
    column=0, row=4, pady=10, ipadx=10
)
ttk.Button(menu_frame, text="Gestionar Infraccion", command=open_infracciones).grid(
    column=0, row=5, pady=10, ipadx=10
)

app.mainloop()

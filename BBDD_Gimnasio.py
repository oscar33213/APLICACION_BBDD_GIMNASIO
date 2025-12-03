import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class DBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Base de Datos")

        
        try:
            self.conn = psycopg2.connect(
                host="/", #HOST DONDE SE ALOJA
                database="/", # NOMBRE BASE DE DATOS
                user="/", # USUARIO
                password="/" # CONTRASEÑA DE LA BBDD
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{e}")
            exit()

        
        self.create_alumnos_frame()
        self.create_empleados_frame()
        self.create_servicios_frame()
        self.create_asignar_frame()

        
        self.mostrar_alumnos()
        self.mostrar_empleados()
        self.mostrar_servicios()
        self.mostrar_alumnos_clases()

    # -------------------- ALUMNOS --------------------
    def create_alumnos_frame(self):
        frame = tk.LabelFrame(self.root, text="ALUMNOS")
        frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        tk.Label(frame, text="Nombre:").grid(row=0, column=0)
        self.entry_nombre = tk.Entry(frame); self.entry_nombre.grid(row=0, column=1)
        tk.Label(frame, text="Apellido1:").grid(row=1, column=0)
        self.entry_ape1 = tk.Entry(frame); self.entry_ape1.grid(row=1, column=1)
        tk.Label(frame, text="Apellido2:").grid(row=2, column=0)
        self.entry_ape2 = tk.Entry(frame); self.entry_ape2.grid(row=2, column=1)
        tk.Label(frame, text="Teléfono:").grid(row=3, column=0)
        self.entry_telefono = tk.Entry(frame); self.entry_telefono.grid(row=3, column=1)
        tk.Label(frame, text="Dirección:").grid(row=4, column=0)
        self.entry_direccion = tk.Entry(frame); self.entry_direccion.grid(row=4, column=1)
        self.var_premium = tk.BooleanVar()
        tk.Checkbutton(frame, text="Premium", variable=self.var_premium).grid(row=5, column=0, columnspan=2)

        tk.Button(frame, text="Agregar Alumno", command=self.agregar_alumno).grid(row=6, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Editar Alumno", command=self.editar_alumno).grid(row=7, column=0, columnspan=2)
        tk.Button(frame, text="Eliminar Alumno", command=self.eliminar_alumno).grid(row=8, column=0, columnspan=2, pady=5)

        self.tree_alumnos = ttk.Treeview(frame, columns=("ID","Nombre","Ape1","Ape2","Telefono","Direccion","Premium"), show="headings")
        for col in self.tree_alumnos["columns"]:
            self.tree_alumnos.heading(col, text=col)
        self.tree_alumnos.grid(row=9, column=0, columnspan=2)
        self.tree_alumnos.bind("<<TreeviewSelect>>", self.seleccionar_alumno)

    def agregar_alumno(self):
        try:
            self.cursor.execute("""
                INSERT INTO ALUMNOS (NOMBRE_ABONADO, APE1_ABONADO, APE2_ABONADO, TELEFONO, DIRECCION, USER_PREMIUM)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.entry_nombre.get(), self.entry_ape1.get(), self.entry_ape2.get(),
                self.entry_telefono.get(), self.entry_direccion.get(), self.var_premium.get()))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Alumno añadido")
            self.mostrar_alumnos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.conn.rollback()

    def editar_alumno(self):
        selected = self.tree_alumnos.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un alumno")
            return
        alumno_id = self.tree_alumnos.item(selected[0])['values'][0]
        try:
            self.cursor.execute("""
                UPDATE ALUMNOS
                SET NOMBRE_ABONADO=%s, APE1_ABONADO=%s, APE2_ABONADO=%s, TELEFONO=%s, DIRECCION=%s, USER_PREMIUM=%s
                WHERE ID=%s
            """, (self.entry_nombre.get(), self.entry_ape1.get(), self.entry_ape2.get(),
                self.entry_telefono.get(), self.entry_direccion.get(), self.var_premium.get(), alumno_id))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Alumno editado")
            self.mostrar_alumnos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.conn.rollback()

    def eliminar_alumno(self):
        selected = self.tree_alumnos.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona un alumno")
            return
        alumno_id = self.tree_alumnos.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", "¿Eliminar alumno y sus asignaciones?"):
            try:
                self.cursor.execute("DELETE FROM ALUMNOS_CLASES WHERE alumno_id=%s", (alumno_id,))
                self.cursor.execute("DELETE FROM ALUMNOS WHERE ID=%s", (alumno_id,))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Alumno eliminado")
                self.mostrar_alumnos()
                self.mostrar_alumnos_clases()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.conn.rollback()

    def seleccionar_alumno(self, event):
        selected = self.tree_alumnos.selection()
        if selected:
            values = self.tree_alumnos.item(selected[0])['values']
            self.entry_nombre.delete(0, tk.END); self.entry_nombre.insert(0, values[1])
            self.entry_ape1.delete(0, tk.END); self.entry_ape1.insert(0, values[2])
            self.entry_ape2.delete(0, tk.END); self.entry_ape2.insert(0, values[3])
            self.entry_telefono.delete(0, tk.END); self.entry_telefono.insert(0, values[4])
            self.entry_direccion.delete(0, tk.END); self.entry_direccion.insert(0, values[5])
            self.var_premium.set(values[6])

    def mostrar_alumnos(self):
        for i in self.tree_alumnos.get_children(): self.tree_alumnos.delete(i)
        self.cursor.execute("SELECT * FROM ALUMNOS")
        for row in self.cursor.fetchall():
            self.tree_alumnos.insert("", tk.END, values=row)

    # -------------------- EMPLEADOS --------------------
    def create_empleados_frame(self):
        frame = tk.LabelFrame(self.root, text="EMPLEADOS")
        frame.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        tk.Label(frame, text="Nombre:").grid(row=0, column=0)
        self.entry_emp_nombre = tk.Entry(frame); self.entry_emp_nombre.grid(row=0, column=1)
        tk.Label(frame, text="Apellido1:").grid(row=1, column=0)
        self.entry_emp_ape1 = tk.Entry(frame); self.entry_emp_ape1.grid(row=1, column=1)
        tk.Label(frame, text="Apellido2:").grid(row=2, column=0)
        self.entry_emp_ape2 = tk.Entry(frame); self.entry_emp_ape2.grid(row=2, column=1)
        tk.Label(frame, text="Teléfono:").grid(row=3, column=0)
        self.entry_emp_telefono = tk.Entry(frame); self.entry_emp_telefono.grid(row=3, column=1)
        tk.Label(frame, text="Dirección:").grid(row=4, column=0)
        self.entry_emp_direccion = tk.Entry(frame); self.entry_emp_direccion.grid(row=4, column=1)
        tk.Label(frame, text="Nomina:").grid(row=5, column=0)
        self.entry_emp_nomina = tk.Entry(frame); self.entry_emp_nomina.grid(row=5, column=1)
        tk.Label(frame, text="Rol:").grid(row=6, column=0)
        self.entry_emp_rol = tk.Entry(frame); self.entry_emp_rol.grid(row=6, column=1)

        tk.Button(frame, text="Agregar", command=self.agregar_empleado).grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Editar", command=self.editar_empleado).grid(row=8, column=0, columnspan=2)
        tk.Button(frame, text="Eliminar", command=self.eliminar_empleado).grid(row=9, column=0, columnspan=2, pady=5)

        self.tree_empleados = ttk.Treeview(frame, columns=("ID","Nombre","Ape1","Ape2","Telefono","Direccion","Nomina","Rol"), show="headings")
        for col in self.tree_empleados["columns"]: self.tree_empleados.heading(col, text=col)
        self.tree_empleados.grid(row=10, column=0, columnspan=2)
        self.tree_empleados.bind("<<TreeviewSelect>>", self.seleccionar_empleado)

    def agregar_empleado(self):
        try:
            self.cursor.execute("""
                INSERT INTO EMPLEADOS (NOMBRE, APE1, APE2, TELEFONO, DIRECCION, NOMINA, ROL)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (self.entry_emp_nombre.get(), self.entry_emp_ape1.get(), self.entry_emp_ape2.get(),
                self.entry_emp_telefono.get(), self.entry_emp_direccion.get(), self.entry_emp_nomina.get(),
                self.entry_emp_rol.get()))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Empleado agregado")
            self.mostrar_empleados()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.conn.rollback()

    def editar_empleado(self):
        selected = self.tree_empleados.selection()
        if not selected: messagebox.showwarning("Aviso", "Selecciona un empleado"); return
        emp_id = self.tree_empleados.item(selected[0])['values'][0]
        try:
            self.cursor.execute("""
                UPDATE EMPLEADOS SET NOMBRE=%s, APE1=%s, APE2=%s, TELEFONO=%s, DIRECCION=%s, NOMINA=%s, ROL=%s
                WHERE ID=%s
            """, (self.entry_emp_nombre.get(), self.entry_emp_ape1.get(), self.entry_emp_ape2.get(),
                self.entry_emp_telefono.get(), self.entry_emp_direccion.get(), self.entry_emp_nomina.get(),
                self.entry_emp_rol.get(), emp_id))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Empleado editado")
            self.mostrar_empleados()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.conn.rollback()

    def eliminar_empleado(self):
        selected = self.tree_empleados.selection()
        if not selected: messagebox.showwarning("Aviso", "Selecciona un empleado"); return
        emp_id = self.tree_empleados.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", "Eliminar empleado y servicios asociados?"):
            try:
                self.cursor.execute("DELETE FROM SERVICIOS WHERE INSTRUCTOR=%s", (emp_id,))
                self.cursor.execute("DELETE FROM EMPLEADOS WHERE ID=%s", (emp_id,))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Empleado eliminado")
                self.mostrar_empleados()
                self.mostrar_servicios()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.conn.rollback()

    def seleccionar_empleado(self, event):
        selected = self.tree_empleados.selection()
        if selected:
            values = self.tree_empleados.item(selected[0])['values']
            self.entry_emp_nombre.delete(0, tk.END); self.entry_emp_nombre.insert(0, values[1])
            self.entry_emp_ape1.delete(0, tk.END); self.entry_emp_ape1.insert(0, values[2])
            self.entry_emp_ape2.delete(0, tk.END); self.entry_emp_ape2.insert(0, values[3])
            self.entry_emp_telefono.delete(0, tk.END); self.entry_emp_telefono.insert(0, values[4])
            self.entry_emp_direccion.delete(0, tk.END); self.entry_emp_direccion.insert(0, values[5])
            self.entry_emp_nomina.delete(0, tk.END); self.entry_emp_nomina.insert(0, values[6])
            self.entry_emp_rol.delete(0, tk.END); self.entry_emp_rol.insert(0, values[7])

    def mostrar_empleados(self):
        for i in self.tree_empleados.get_children(): self.tree_empleados.delete(i)
        self.cursor.execute("SELECT * FROM EMPLEADOS")
        for row in self.cursor.fetchall():
            self.tree_empleados.insert("", tk.END, values=row)

    # -------------------- SERVICIOS --------------------
    def create_servicios_frame(self):
        frame = tk.LabelFrame(self.root, text="SERVICIOS")
        frame.grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        tk.Label(frame, text="Nombre Servicio:").grid(row=0, column=0)
        self.entry_servicio_nombre = tk.Entry(frame); self.entry_servicio_nombre.grid(row=0, column=1)
        tk.Label(frame, text="ID Instructor:").grid(row=1, column=0)
        self.entry_servicio_instructor = tk.Entry(frame); self.entry_servicio_instructor.grid(row=1, column=1)
        tk.Button(frame, text="Agregar", command=self.agregar_servicio).grid(row=2, column=0, columnspan=2)
        tk.Button(frame, text="Eliminar", command=self.eliminar_servicio).grid(row=3, column=0, columnspan=2, pady=5)

        self.tree_servicios = ttk.Treeview(frame, columns=("ID","Nombre Servicio","Instructor"), show="headings")
        for col in self.tree_servicios["columns"]: self.tree_servicios.heading(col, text=col)
        self.tree_servicios.grid(row=4, column=0, columnspan=2)
        self.tree_servicios.bind("<<TreeviewSelect>>", self.seleccionar_servicio)

    def agregar_servicio(self):
        try:
            self.cursor.execute("INSERT INTO SERVICIOS (NOMBRE_SERVICIO, INSTRUCTOR) VALUES (%s,%s)",
                                (self.entry_servicio_nombre.get(), self.entry_servicio_instructor.get()))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Servicio agregado")
            self.mostrar_servicios()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.conn.rollback()

    def eliminar_servicio(self):
        selected = self.tree_servicios.selection()
        if not selected: messagebox.showwarning("Aviso", "Selecciona un servicio"); return
        serv_id = self.tree_servicios.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmar", "Eliminar servicio y sus asignaciones?"):
            try:
                self.cursor.execute("DELETE FROM ALUMNOS_CLASES WHERE servicio_id=%s", (serv_id,))
                self.cursor.execute("DELETE FROM SERVICIOS WHERE ID=%s", (serv_id,))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Servicio eliminado")
                self.mostrar_servicios()
                self.mostrar_alumnos_clases()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.conn.rollback()

    def seleccionar_servicio(self, event):
        selected = self.tree_servicios.selection()
        if selected:
            values = self.tree_servicios.item(selected[0])['values']
            self.entry_servicio_nombre.delete(0, tk.END); self.entry_servicio_nombre.insert(0, values[1])
            self.entry_servicio_instructor.delete(0, tk.END); self.entry_servicio_instructor.insert(0, values[2].split()[0]) # ID real no mostrado

    def mostrar_servicios(self):
        for i in self.tree_servicios.get_children(): self.tree_servicios.delete(i)
        self.cursor.execute("""
            SELECT s.ID, s.NOMBRE_SERVICIO, e.NOMBRE || ' ' || e.APE1 || ' ' || e.APE2
            FROM SERVICIOS s JOIN EMPLEADOS e ON s.INSTRUCTOR = e.ID
        """)
        for row in self.cursor.fetchall():
            self.tree_servicios.insert("", tk.END, values=row)

    # -------------------- ASIGNAR ALUMNOS --------------------
    def create_asignar_frame(self):
        frame = tk.LabelFrame(self.root, text="ASIGNAR ALUMNO A CLASE")
        frame.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
        tk.Label(frame, text="ID Alumno:").grid(row=0, column=0)
        self.entry_asignar_alumno = tk.Entry(frame); self.entry_asignar_alumno.grid(row=0, column=1)
        tk.Label(frame, text="ID Servicio:").grid(row=1, column=0)
        self.entry_asignar_servicio = tk.Entry(frame); self.entry_asignar_servicio.grid(row=1, column=1)
        tk.Button(frame, text="Asignar", command=self.asignar_alumno_clase).grid(row=2, column=0, columnspan=2)
        tk.Button(frame, text="Quitar", command=self.quitar_alumno_clase).grid(row=3, column=0, columnspan=2, pady=5)

        self.tree_alumnos_clases = ttk.Treeview(frame, columns=("Alumno","Clase"), show="headings")
        for col in self.tree_alumnos_clases["columns"]: self.tree_alumnos_clases.heading(col, text=col)
        self.tree_alumnos_clases.grid(row=4, column=0, columnspan=2)

    def asignar_alumno_clase(self):
        try:
            self.cursor.execute("INSERT INTO ALUMNOS_CLASES (alumno_id, servicio_id) VALUES (%s,%s)",
                                (self.entry_asignar_alumno.get(), self.entry_asignar_servicio.get()))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Alumno asignado")
            self.mostrar_alumnos_clases()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.conn.rollback()

    def quitar_alumno_clase(self):
        try:
            self.cursor.execute("DELETE FROM ALUMNOS_CLASES WHERE alumno_id=%s AND servicio_id=%s",
                                (self.entry_asignar_alumno.get(), self.entry_asignar_servicio.get()))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Alumno quitado de clase")
            self.mostrar_alumnos_clases()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.conn.rollback()

    def mostrar_alumnos_clases(self):
        for i in self.tree_alumnos_clases.get_children(): self.tree_alumnos_clases.delete(i)
        self.cursor.execute("""
            SELECT a.NOMBRE_ABONADO || ' ' || a.APE1_ABONADO || ' ' || a.APE2_ABONADO AS Alumno,
            s.NOMBRE_SERVICIO AS Clase
            FROM ALUMNOS_CLASES ac
            JOIN ALUMNOS a ON ac.alumno_id = a.ID
            JOIN SERVICIOS s ON ac.servicio_id = s.ID
        """)
        for row in self.cursor.fetchall():
            self.tree_alumnos_clases.insert("", tk.END, values=row)
            



if __name__ == "__main__":
    root = tk.Tk()
    app = DBApp(root)
    root.mainloop()
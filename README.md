# Documentación del Proyecto: Gestión Base de Datos con Tkinter y PostgreSQL

## 📌 Descripción
Este proyecto implementa una aplicación gráfica en **Python** utilizando **Tkinter** para la gestión de una base de datos PostgreSQL. Permite administrar **alumnos**, **empleados**, **servicios** y la asignación de alumnos a clases, todo desde una interfaz amigable.

⚠️ **Nota importante**: El código compartido no está listo para funcionar directamente con un simple copypaste.  
Es necesario **introducir correctamente los parámetros de conexión** en la función `psycopg2.connect()`.  
En particular, los valores de **`host`** y **`password`** deben ser facilitados por el **Administrador de la base de datos**. El resto de parámetros (`database`, `user`) ya vienen configurados en el código y pueden mantenerse, siempre que coincidan con la configuración del entorno.

---

## ⚙️ Tecnologías utilizadas
- **Python 3**
- **Tkinter** (interfaz gráfica)
- **ttk** (widgets avanzados)
- **messagebox** (ventanas emergentes)
- **psycopg2** (conexión a PostgreSQL)

---

## 🗂️ Estructura de la aplicación
La aplicación se organiza en diferentes secciones (frames):

1. **Alumnos**
   - Agregar, editar y eliminar alumnos.
   - Campos: Nombre, Apellido1, Apellido2, Teléfono, Dirección, Premium.
   - Visualización en `Treeview`.

2. **Empleados**
   - Agregar, editar y eliminar empleados.
   - Campos: Nombre, Apellido1, Apellido2, Teléfono, Dirección, Nómina, Rol.
   - Visualización en `Treeview`.

3. **Servicios**
   - Agregar y eliminar servicios.
   - Campos: Nombre del servicio, ID del instructor.
   - Relación con empleados (instructor asignado).
   - Visualización en `Treeview`.

4. **Asignación de alumnos a clases**
   - Asignar y quitar alumnos de servicios.
   - Campos: ID Alumno, ID Servicio.
   - Visualización en `Treeview`.

---

## 📊 Tablas en la base de datos
La aplicación interactúa con las siguientes tablas:

- **ALUMNOS**
  - `ID`, `NOMBRE_ABONADO`, `APE1_ABONADO`, `APE2_ABONADO`, `TELEFONO`, `DIRECCION`, `USER_PREMIUM`

- **EMPLEADOS**
  - `ID`, `NOMBRE`, `APE1`, `APE2`, `TELEFONO`, `DIRECCION`, `NOMINA`, `ROL`

- **SERVICIOS**
  - `ID`, `NOMBRE_SERVICIO`, `INSTRUCTOR` (relación con `EMPLEADOS`)

- **ALUMNOS_CLASES**
  - `alumno_id` (FK a `ALUMNOS`)
  - `servicio_id` (FK a `SERVICIOS`)

---

## 🔑 Funcionalidades principales
- **Conexión a PostgreSQL**: mediante `psycopg2.connect()`.
- **CRUD completo**:
  - Alumnos: insertar, actualizar, eliminar.
  - Empleados: insertar, actualizar, eliminar.
  - Servicios: insertar, eliminar.
  - Asignaciones: insertar, eliminar.
- **Interfaz gráfica**:
  - Formularios de entrada.
  - Botones de acción.
  - Tablas (`Treeview`) para mostrar registros.
- **Mensajes emergentes**:
  - Confirmaciones de éxito.
  - Advertencias y errores.
  - Confirmación antes de eliminar registros.

---

## 🚀 Flujo de ejecución
1. Se inicializa la aplicación con `Tk()`.
2. Se establece la conexión a la base de datos (**introduciendo el `host` y la `password` proporcionados por el Administrador**).
3. Se crean los frames de **Alumnos**, **Empleados**, **Servicios** y **Asignaciones**.
4. Se cargan los datos iniciales desde la base de datos.
5. El usuario interactúa con la interfaz para realizar operaciones CRUD.
6. Los cambios se reflejan en la base de datos y en la interfaz.

---

## 📌 Ejemplo de uso
1. **Agregar alumno**:
   - Completar los campos en el formulario de alumnos.
   - Pulsar **Agregar Alumno**.
   - El registro se guarda en la tabla `ALUMNOS` y se muestra en el `Treeview`.

2. **Asignar alumno a clase**:
   - Introducir el `ID Alumno` y `ID Servicio`.
   - Pulsar **Asignar**.
   - Se crea un registro en `ALUMNOS_CLASES`.

---

## 🛠️ Manejo de errores
- Uso de `try/except` para capturar excepciones.
- Rollback automático en caso de error en la base de datos.
- Mensajes de error mostrados con `messagebox.showerror`.

---
## ⚖️ Licencia y distribución

Este proyecto **no está permitido para copia ni distribución sin autorización expresa**.  
En caso de querer reutilizarlo o modificarlo, se deberá crear un **FORK** autorizado por el Administrador o el propietario del código.

---

## ▶️ Ejecución
```bash
python BBDD_Gimnasio.py




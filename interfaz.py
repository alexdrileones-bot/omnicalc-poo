import customtkinter as ctk
from tkinter import messagebox
from modelos import ConversionDatos, ConversionTemperatura, CalculoSubredIP
from servicios import CalculadoraServicio


class OmniCalcApp(ctk.CTk):
    """Interfaz gráfica de usuario desacoplada de la lógica de cálculo."""

    def __init__(self):
        super().__init__()
        self.title("OmniCalc — Conversor Técnico y Redes POO")
        self.geometry("780x540")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.__servicio = CalculadoraServicio()
        self.__construir_ui()
        self.__actualizar_opciones_categoria("Almacenamiento Digital")

    def __construir_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel izquierdo: Controles de cálculo
        panel_izq = ctk.CTkFrame(self, corner_radius=12)
        panel_izq.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="nsew")

        ctk.CTkLabel(
            panel_izq, text="OmniCalc", font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(20, 2))
        ctk.CTkLabel(
            panel_izq, text="Conversor Técnico Multidominio", text_color="gray70"
        ).pack(pady=(0, 18))

        ctk.CTkLabel(panel_izq, text="Categoría:", anchor="w").pack(fill="x", padx=24)
        self.combo_categoria = ctk.CTkOptionMenu(
            panel_izq,
            values=["Almacenamiento Digital", "Temperatura", "Subred IPv4 (CIDR)"],
            command=self.__actualizar_opciones_categoria,
        )
        self.combo_categoria.pack(fill="x", padx=24, pady=(4, 14))

        # Selectores de unidad origen y destino
        frame_unidades = ctk.CTkFrame(panel_izq, fg_color="transparent")
        frame_unidades.pack(fill="x", padx=24, pady=(0, 14))
        frame_unidades.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(frame_unidades, text="De:", anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(frame_unidades, text="A:", anchor="w").grid(row=0, column=1, sticky="w", padx=(8, 0))

        self.combo_origen = ctk.CTkOptionMenu(frame_unidades, values=["MB"])
        self.combo_origen.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        self.combo_destino = ctk.CTkOptionMenu(frame_unidades, values=["GB"])
        self.combo_destino.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(4, 0))

        # Entrada de dato
        self.lbl_entrada = ctk.CTkLabel(panel_izq, text="Valor a convertir:", anchor="w")
        self.lbl_entrada.pack(fill="x", padx=24)

        self.entry_valor = ctk.CTkEntry(panel_izq, placeholder_text="Ej: 2048")
        self.entry_valor.pack(fill="x", padx=24, pady=(4, 16))
        self.entry_valor.bind("<Return>", lambda _: self.__ejecutar_calculo())

        self.btn_calcular = ctk.CTkButton(
            panel_izq,
            text="Calcular",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.__ejecutar_calculo,
        )
        self.btn_calcular.pack(fill="x", padx=24, pady=(0, 18))

        # Caja de resultado destacado
        caja_res = ctk.CTkFrame(panel_izq, corner_radius=8)
        caja_res.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        ctk.CTkLabel(caja_res, text="Resultado:", font=ctk.CTkFont(size=12), text_color="gray70").pack(
            anchor="w", padx=12, pady=(8, 0)
        )
        self.lbl_resultado = ctk.CTkLabel(
            caja_res,
            text="—",
            font=ctk.CTkFont(size=15, weight="bold"),
            wraplength=300,
            justify="left",
        )
        self.lbl_resultado.pack(anchor="w", padx=12, pady=(4, 10))

        # Panel derecho: Historial LIFO
        panel_der = ctk.CTkFrame(self, corner_radius=12)
        panel_der.grid(row=0, column=1, padx=(8, 16), pady=16, sticky="nsew")

        ctk.CTkLabel(
            panel_der, text="Historial Reciente", font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10))

        self.textbox_historial = ctk.CTkTextbox(panel_der, state="disabled", wrap="word")
        self.textbox_historial.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        frame_acciones = ctk.CTkFrame(panel_der, fg_color="transparent")
        frame_acciones.pack(fill="x", padx=16, pady=(0, 20))
        frame_acciones.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            frame_acciones, text="Deshacer último", fg_color="#3B4252", command=self.__deshacer
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            frame_acciones, text="Limpiar todo", fg_color="#A63A50", hover_color="#872D40", command=self.__limpiar
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

    def __actualizar_opciones_categoria(self, categoria: str):
        if categoria == "Almacenamiento Digital":
            unidades = ["Bits", "Bytes", "KB", "MB", "GB", "TB"]
            self.combo_origen.configure(values=unidades, state="normal")
            self.combo_destino.configure(values=unidades, state="normal")
            self.combo_origen.set("MB")
            self.combo_destino.set("GB")
            self.lbl_entrada.configure(text="Valor numérico a convertir:")
            self.entry_valor.configure(placeholder_text="Ej: 2048")
        elif categoria == "Temperatura":
            unidades = ["Celsius", "Fahrenheit", "Kelvin"]
            self.combo_origen.configure(values=unidades, state="normal")
            self.combo_destino.configure(values=unidades, state="normal")
            self.combo_origen.set("Celsius")
            self.combo_destino.set("Fahrenheit")
            self.lbl_entrada.configure(text="Temperatura a convertir:")
            self.entry_valor.configure(placeholder_text="Ej: 30")
        else:
            self.combo_origen.configure(values=["IPv4/CIDR"], state="disabled")
            self.combo_destino.configure(values=["Subred"], state="disabled")
            self.combo_origen.set("IPv4/CIDR")
            self.combo_destino.set("Subred")
            self.lbl_entrada.configure(text="Dirección IPv4 con prefijo CIDR:")
            self.entry_valor.configure(placeholder_text="Ej: 192.168.10.25/24")

    def __ejecutar_calculo(self):
        categoria = self.combo_categoria.get()
        dato = self.entry_valor.get()

        try:
            if categoria == "Almacenamiento Digital":
                operacion = ConversionDatos(self.combo_origen.get(), self.combo_destino.get())
            elif categoria == "Temperatura":
                operacion = ConversionTemperatura(self.combo_origen.get(), self.combo_destino.get())
            else:
                operacion = CalculoSubredIP()

            resultado = self.__servicio.procesar(operacion, dato)
            self.lbl_resultado.configure(text=resultado)
            self.__refrescar_historial()
        except ValueError as error:
            messagebox.showwarning("Dato inválido", str(error))

    def __refrescar_historial(self):
        registros = self.__servicio.obtener_historial()
        self.textbox_historial.configure(state="normal")
        self.textbox_historial.delete("1.0", "end")
        if not registros:
            self.textbox_historial.insert("end", "Aún no hay operaciones registradas.")
        else:
            self.textbox_historial.insert("end", "\n\n".join(registros))
        self.textbox_historial.configure(state="disabled")

    def __deshacer(self):
        if self.__servicio.deshacer_ultimo():
            self.__refrescar_historial()
        else:
            messagebox.showinfo("Historial vacío", "No hay operaciones recientes para deshacer.")

    def __limpiar(self):
        self.__servicio.limpiar_historial()
        self.lbl_resultado.configure(text="—")
        self.__refrescar_historial()
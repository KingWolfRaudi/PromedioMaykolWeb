import flet as ft

def main(page: ft.Page):
    # Configuración de la ventana web
    page.title = "Calculadora de Notas Estudiantiles"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30 
    # NUEVO: Permitimos que la página tenga "scroll" si el contenido no cabe en la pantalla
    page.scroll = ft.ScrollMode.AUTO 

    # --- DATOS POR DEFECTO ---
    escala_por_defecto = [
        {"letra": "A", "min": 17},
        {"letra": "B", "min": 13},
        {"letra": "C", "min": 11},
        {"letra": "C - (D)", "min": 10}
    ]

    # --- PANEL IZQUIERDO: CONFIGURACIÓN DE ESCALA ---
    campos_letras = []
    campos_mins = []

    for i in range(4):
        campos_letras.append(ft.TextField(value=escala_por_defecto[i]["letra"], width=120, text_align=ft.TextAlign.CENTER, disabled=True))
        campos_mins.append(ft.TextField(value=str(escala_por_defecto[i]["min"]), width=80, text_align=ft.TextAlign.CENTER, disabled=True))

    def toggle_candado(e):
        nuevo_estado = not campos_letras[0].disabled
        for i in range(4):
            campos_letras[i].disabled = nuevo_estado
            if i < 3: 
                campos_mins[i].disabled = nuevo_estado
                
        boton_candado.icon = ft.Icons.LOCK if nuevo_estado else ft.Icons.LOCK_OPEN
        boton_guardar_escala.visible = not nuevo_estado
        page.update()

    def guardar_escala(e):
        try:
            for i in range(3):
                int(campos_mins[i].value)
        except ValueError:
            mostrar_error("Los valores mínimos deben ser números.")
            return

        toggle_candado(None)
        page.snack_bar = ft.SnackBar(ft.Text("¡Escala guardada para esta sesión!"), bgcolor=ft.Colors.GREEN_700)
        page.snack_bar.open = True
        page.update()

    def restaurar_escala(e):
        for i in range(4):
            campos_letras[i].value = escala_por_defecto[i]["letra"]
            campos_mins[i].value = str(escala_por_defecto[i]["min"])
            
        page.snack_bar = ft.SnackBar(ft.Text("Escala restaurada a sus valores por defecto"), bgcolor=ft.Colors.BLUE_700)
        page.snack_bar.open = True
        page.update()

    boton_candado = ft.IconButton(icon=ft.Icons.LOCK, on_click=toggle_candado, tooltip="Desbloquear para editar")
    boton_restaurar = ft.IconButton(icon=ft.Icons.RESTORE, on_click=restaurar_escala, tooltip="Restaurar valores por defecto", icon_color=ft.Colors.BLUE_400)
    boton_guardar_escala = ft.Button(content=ft.Row([ft.Icon(ft.Icons.SAVE), ft.Text("Guardar Cambios")], tight=True), on_click=guardar_escala, visible=False)

    filas_escala = []
    for i in range(4):
        filas_escala.append(ft.Row([campos_letras[i], ft.Text(">="), campos_mins[i]], alignment=ft.MainAxisAlignment.CENTER))

    panel_izquierdo = ft.Column(
        controls=[
            ft.Row([ft.Text("Escala de Notas", size=20, weight=ft.FontWeight.BOLD), boton_candado, boton_restaurar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(color=ft.Colors.WHITE24),
            *filas_escala,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            boton_guardar_escala
        ],
        width=350, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # --- PANEL DERECHO: CALCULADORA ---
    total_input = ft.TextField(label="Total de Ejercicios", text_align=ft.TextAlign.CENTER, width=250)
    aciertos_input = ft.TextField(label="Cantidad de Aciertos", text_align=ft.TextAlign.CENTER, width=250)
    
    resultado_texto = ft.Text(size=18, text_align=ft.TextAlign.CENTER)
    letra_texto = ft.Text(size=60, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    def mostrar_error(mensaje):
        letra_texto.value = "!"
        letra_texto.color = ft.Colors.RED_500
        resultado_texto.value = mensaje
        resultado_texto.color = ft.Colors.RED_500
        page.update()

    def calcular_nota(e):
        resultado_texto.value = ""
        resultado_texto.color = None 
        letra_texto.value = ""
        
        texto_total = total_input.value.strip()
        texto_aciertos = aciertos_input.value.strip()

        if not texto_total or not texto_aciertos:
            mostrar_error("Los campos no pueden estar vacíos.")
            return 
        try:
            total = int(texto_total)
            aciertos = int(texto_aciertos)
            if total <= 0:
                mostrar_error("El total debe ser mayor a 0.")
                return
            if aciertos < 0 or aciertos > total:
                mostrar_error(f"Aciertos inválidos (0 - {total}).")
                return
        except ValueError:
            mostrar_error("Ingresa solo números enteros.")
            return

        nota_numerica = round((aciertos / total) * 10 + 10)
        
        if nota_numerica < 10:
            nota_numerica = 10

        escala_leida = []
        for i in range(4):
            escala_leida.append({"letra": campos_letras[i].value, "min": int(campos_mins[i].value)})

        if nota_numerica >= escala_leida[0]["min"]:
            letra = escala_leida[0]["letra"]
            color = ft.Colors.GREEN_400
        elif nota_numerica >= escala_leida[1]["min"]:
            letra = escala_leida[1]["letra"]
            color = ft.Colors.GREEN_400
        elif nota_numerica >= escala_leida[2]["min"]:
            letra = escala_leida[2]["letra"]
            color = ft.Colors.ORANGE_400
        else:
            letra = escala_leida[3]["letra"]
            color = ft.Colors.RED_400

        resultado_texto.value = f"Tu nota es: {nota_numerica}/20"
        resultado_texto.color = None 
        letra_texto.value = f"{letra}"
        letra_texto.color = color
        page.update()

    total_input.on_submit = calcular_nota
    aciertos_input.on_submit = calcular_nota

    def limpiar_campos(e):
        total_input.value = ""
        aciertos_input.value = ""
        resultado_texto.value = ""
        letra_texto.value = ""
        page.update()

    boton_calcular = ft.Button(content=ft.Row([ft.Icon(ft.Icons.CALCULATE), ft.Text("Calcular")], tight=True), on_click=calcular_nota, style=ft.ButtonStyle(padding=20))
    boton_limpiar = ft.Button(content=ft.Row([ft.Icon(ft.Icons.DELETE_SWEEP), ft.Text("Limpiar")], tight=True), on_click=limpiar_campos, style=ft.ButtonStyle(padding=20, color=ft.Colors.RED_400))

    def alternar_tema(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    # CORRECCIÓN: Le damos un ancho fijo (width=400) en lugar de usar expand=True
    panel_derecho = ft.Column(
        controls=[
            ft.Text("Calculadora", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            total_input,
            aciertos_input,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            ft.Row([boton_limpiar, boton_calcular], alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
            resultado_texto,
            letra_texto
        ],
        width=400, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # CORRECCIÓN: Quitamos el VerticalDivider y agregamos spacing=50
    contenedor_principal = ft.Row(
        controls=[
            panel_izquierdo,
            panel_derecho
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
        wrap=True,
        spacing=50 
    )

    page.add(
        ft.Row([ft.Switch(label="Modo Oscuro", value=True, on_change=alternar_tema)], alignment=ft.MainAxisAlignment.END),
        contenedor_principal
    )

ft.run(main, view=ft.AppView.WEB_BROWSER)
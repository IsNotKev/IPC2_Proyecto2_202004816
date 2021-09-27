
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import xml.etree.ElementTree as ET
from Lista import Lista
from graphviz import Digraph,Graph
import pathlib
import webbrowser
from PIL import Image,ImageTk

class Linea(object):
    def __init__(self,no,comp,tiempo):
        self.no = no
        self.comp = comp
        self.tiempo = tiempo

class Producto(object):
    def __init__(self,nombre,elaboracion):
        self.nombre = nombre
        self.elaboracion = elaboracion

class Componente(object):
    def __init__(self,linea,columna):
        self.linea = linea
        self.columna = columna

class Simulacion(object):
    def __init__(self,nombre,productos):
        self.nombre = nombre 
        self.productos = productos

if __name__ == "__main__":

    lineas = Lista()
    productos = Lista()
    simulaciones = Lista()
    p = Lista()

    window = Tk()

    ancho_ventana = 750
    alto_ventana = 350  

    x_ventana = window.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = window.winfo_screenheight() // 2 - alto_ventana // 2

    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
    window.geometry(posicion)
    window.config(background='#FBF3D6')
    window.resizable(0,0)
    window.title("Digital Intelligence, S. A.")

    menubar = Menu(window)
    window['menu'] = menubar


    def cconfiguracion():
        global lineas
        global productos
        global simulaciones

        lineas = Lista()
        productos = Lista()
        simulaciones = Lista()

        filename = askopenfilename()

        extension = filename.split('.')
        if extension[len(extension)-1] != 'xml' and extension[len(extension)-1] != 'XML':
            messagebox.showerror(title='Error', message='Por Favor Cargue Un Archivo Con Extensión XML')
            combo.configure(values=[''])
            combo.current(0)
        else:
            doc = ET.parse(filename)
            root = doc.getroot()
            #cantlineas = int((root.findall('CantidadLineasProduccion'))[0].text)
            listadolineas = root.findall('ListadoLineasProduccion')
            lineasproduccion = listadolineas[0].findall('LineaProduccion')
            for l in lineasproduccion:
                no = int((l.findall('Numero'))[0].text)
                comp = int((l.findall('CantidadComponentes'))[0].text)
                tiempo = int((l.findall('TiempoEnsamblaje'))[0].text)

                nlinea = Linea(no,comp,tiempo)

                lineas.agregar(nlinea)

            listadoprdcs = root.findall('ListadoProductos')
            prdcs = listadoprdcs[0].findall('Producto')



            for p in prdcs:
                nombre = (p.findall('nombre'))[0].text
                elaboracion = (p.findall('elaboracion'))[0].text
                elaboracion = elaboracion.strip()

                cs = elaboracion.split(' ')

                elab = Lista()

                for c in cs:
                    fila = int(c[1])
                    columna = int(c[4])
                    nComponente = Componente(fila,columna)
                    elab.agregar(nComponente)
                

                nombre = nombre.strip()
                
                nproducto = Producto(nombre,elab)
                productos.agregar(nproducto)

                values = list(combo["values"])
                combo["values"] = values + [nombre]
            combo.current(0)
            messagebox.showinfo(title='Carga De Configuración',message='Arhivo Leido Correctamente.')



    def csimulacion():
        global lineas
        global simulaciones
        if lineas.tamano() == 0:        
            messagebox.showerror(title='Error', message='Cargue Una Configuración de Máquina Para Cargar Simulación.')
        else:
            filename = askopenfilename()
            extension = filename.split('.')
            if extension[len(extension)-1] != 'xml' and extension[len(extension)-1] != 'XML':
                messagebox.showerror(title='Error', message='Por Favor Cargue Un Archivo Con Extensión XML')
            else:
                doc = ET.parse(filename)
                root = doc.getroot()
                nombre = (root.findall('Nombre'))[0].text
                nombre = nombre.strip()

                listap = root.findall('ListadoProductos')
                products = listap[0].findall('Producto')

                listado = Lista()
                lista.delete(0,'end')

                columns = []
                for x in range(0,lineas.tamano()+1):
                    columns.append('#' + str(x+1))
                tree = ttk.Treeview(tab2, show='headings', height=30, columns=columns)
                tree.grid(row=0, column=0, columnspan=2, sticky = tk.W+tk.E+tk.N+tk.S)
                tab2.grid_rowconfigure(0, weight=1)
                tab2.grid_columnconfigure(0, weight=1)
                tab2.grid_columnconfigure(1, weight=1)
                tree.column('#1', width=50, minwidth=50, stretch=tk.NO)
                tree.heading('#1', text='Tiempo', anchor=tk.CENTER)
                c = ''
                for x in range(0,lineas.tamano()):
                    c+= '<th scope="col">Fila'+str(x+1)+'</th>' 
                    tree.column('#' + str(x+2), width=140, minwidth=140, stretch=tk.NO)
                    tree.heading('#' + str(x+2), text='Fila ' + str(x+1), anchor=tk.CENTER)



                tiempototal = 0
                contiempo = 0

                #Creando Archivo De Salida
                data = ET.Element('SalidaSimulacion')    
                nn = ET.SubElement(data,'Nombre')  
                nn.text = nombre
                listadoProductos = ET.SubElement(data,'ListadoProductos')

                ruta = str(pathlib.Path(__file__).parent.absolute())
                ruta += '\\'
                ruta += nombre
                ruta += '.html'

                archivo = open(ruta,'w')
                archivo.write('<!DOCTYPE><html><head><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous"><title>'+nombre+'</title></head><body style="width:75%;margin:auto;">')
                archivo.write('<br><br><center><table class="table"><tbody>')

                archivo.write('<tr><th scope="col">Tiempo</th>')
                archivo.write(c)
                archivo.write('</tr>')

                for p in products:
                    name = p.text
                    name = name.strip()
                    listado.agregar(name)

                    p = productos.proceso(name)
                    ac = p.cabeza
                    
                    while ac != None:
                        aa = ac.obtenerDato()
                        te = '- Linea ' + str(aa.linea) + ', Componente ' + str(aa.columna)
                        lista.insert('end',te)
                        ac = ac.obtenerSiguiente()


                    producto1 = ET.SubElement(listadoProductos,'Producto')
                    nn2 = ET.SubElement(producto1,'Nombre')
                    nn2.text = name
                    
                    process = productos.analizarProducto(name,lineas)

                    ttamano = process.cabeza.obtenerDato().movs.tamano()
                    tiempototal += ttamano

                    ttiempo = ET.SubElement(producto1,'TiempoTotal')
                    ttiempo.text = str(ttamano) 

                    elaboracionoptima = ET.SubElement(producto1,'ElaboracionOptima')

                    for x in range(0,ttamano):    
                        contiempo += 1
                        val = []
                        val.append(contiempo)
                        gg = process.cabeza

                        cfil = 0

                        tiempoxfila = ET.SubElement(elaboracionoptima,'Tiempo')
                        tiempoxfila.set('NoSegundo',str(contiempo))

                        c1 = '<tr><th>'
                        c1 += str(contiempo)
                        c1 += '</th>'

                        while gg != None:
                            cfil += 1
                            ss = gg.obtenerDato().movs.cabeza
                   
                            while ss != None:
                                if (ss.obtenerDato().tiempo) == (x+1):
                                    val.append(ss.obtenerDato().accion)  
                                    linea = ET.SubElement(tiempoxfila,'LineaEnsamblaje')
                                    linea.set('NoLinea',str(cfil))
                                    linea.text = ss.obtenerDato().accion  

                                    c1 += '<td>'
                                    c1 +=(ss.obtenerDato().accion)
                                    c1 += '</td>'

                                ss = ss.obtenerSiguiente()                                      
                            gg = gg.obtenerSiguiente()  
                        tree.insert("", contiempo-1, text="", values=val)
                        c1 += '</tr>'
                        archivo.write(c1)

                       

                    #values = list(combo["values"])
                    #combo["values"] = values + [nombre]

                
                archivo.write("""</tbody></table></center></body></html>""")
                archivo.close()
                #webbrowser.open_new_tab(ruta)


                # create a new XML file with the results
                mydata = ET.tostring(data)
                myfile = open(nombre + '.xml', "wb")
                myfile.write(mydata)
                myfile.close()
                

                tp.config(text='Tiempo: ' + str(tiempototal) + 's')

                vsb = ttk.Scrollbar(tab2, orient="vertical", command=tree.yview)
                vsb.grid(row=0, column=2, sticky='ns')

                tree.configure(yscrollcommand=vsb.set)

                hsb = ttk.Scrollbar(tab2, orient="horizontal", command=tree.xview)
                hsb.grid(row = 1, column=0, columnspan=2, sticky = tk.W+tk.E)
                tree.configure(xscrollcommand = hsb.set)

                nsimulacion = Simulacion(nombre,listado)
                simulaciones.agregar(nsimulacion)
                

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Cargar Configuración",command=cconfiguracion)
    filemenu.add_command(label="Cargar Simulación",command=csimulacion)

    def graficar():
        global p
        dot = Digraph(comment='Grafica de la pila...!!')
        dot.attr(rankdir='LR')
        contador = 0
        actualPro = p.cabeza
        while actualPro != None:
            contador += 1
            dot.node(str(contador), 'L'+str(actualPro.obtenerDato().linea)+'C'+str(actualPro.obtenerDato().columna))
            actualPro = actualPro.obtenerSiguiente()
            if(contador >1):
                dot.edge(str(contador-1), str(contador))
        dot.render(combo.get(), format="pdf", view=True)


    def html():
        process = productos.analizarProducto(combo.get(),lineas)

        ruta = str(pathlib.Path(__file__).parent.absolute())
        ruta += '\\'
        ruta += combo.get()
        ruta += '.html'

        archivo = open(ruta,'w')

        archivo.write('<!DOCTYPE><html><head><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous"><title>'+combo.get()+'</title></head><body style="width:75%;margin:auto;">')
        archivo.write('<br><br><center><table class="table"><tbody>')

        tmn = process.tamano()
        archivo.write('<tr><th scope="col">Tiempo</th>')
        c = ''
        for x in range(0,tmn):
           c+= '<th scope="col">Fila'+str(x+1)+'</th>' 
        archivo.write(c)
        archivo.write('</tr>')

        ttamano = process.cabeza.obtenerDato().movs.tamano()
        for x in range(0,ttamano):    
            c1 = '<tr><th>'
            c1 += str(x+1)
            c1 += '</th>'
            gg = process.cabeza   
            while gg != None:   
                ss = gg.obtenerDato().movs.cabeza
                while ss != None:
                    if (ss.obtenerDato().tiempo) == (x+1):
                        c1 += '<td>'
                        c1 +=(ss.obtenerDato().accion)
                        c1 += '</td>'
                              
                    ss = ss.obtenerSiguiente()  
                        
                gg = gg.obtenerSiguiente()  
            c1 += '</tr>'
            archivo.write(c1)
        

        archivo.write("""</tbody></table></center></body></html>""")
        archivo.close()

        webbrowser.open_new_tab(ruta)


    reportmenu = Menu(menubar, tearoff=0)
    reportmenu.add_command(label="Generar Reporte HTML",command=html)
    reportmenu.add_command(label="Generar Reporte De Secuencia",command=graficar)

    
    def mostrarInfo():
        messagebox.showinfo(title='Información del Estudiante', message='- Kevin Steve Martinez Lemus\n- 202004816 \n- Introducción a la Programación y Computación 2 Sección "C"\n- Ingenieria en Ciencias y Sistemas\n- 4to Semestre')
    def aplicacion():
        messagebox.showinfo(title='Acerca de la Aplicación',message='Esta aplicación permite simular el funcionamiento de una máquina con “n” líneas de ensamblaje y cada línea de ensamblaje con “m” posibles componentes a seleccionar de forma que pueda predecir el tiempo “óptimo” para elaborar cualquier producto que pueda ser ensamblado en la máquina.')
    ayuda = Menu(menubar, tearoff=0)
    ayuda.add_command(label='Información del Estudiante',command=mostrarInfo)
    ayuda.add_command(label='Acerca de la Aplicación',command=aplicacion)

    menubar.add_cascade(label="Archivo", menu=filemenu)
    menubar.add_cascade(label="Reportes", menu=reportmenu)
    menubar.add_cascade(label="Ayuda", menu=ayuda)
    menubar.add_cascade(label="Salir", command=window.quit)

    #Combo
    #####################################################3
    combo = ttk.Combobox(window,state="readonly",font=("Arial",9,'bold'),height=1)
    combo.grid(row=0,column=0,padx=50,pady=40)

    #BotonAnalizar
    #################################################################################################
    def analizar():
        global p
        if combo.get() == '':
            messagebox.showerror(title='Error',message='Por Favor Cargue Archivos Para Analizar')
        else:
            p = productos.proceso(combo.get())
            ac = p.cabeza
            lista.delete(0,'end')
            while ac != None:
                aa = ac.obtenerDato()
                te = '- Linea ' + str(aa.linea) + ', Componente ' + str(aa.columna)
                lista.insert('end',te)
                ac = ac.obtenerSiguiente()
            process = productos.analizarProducto(combo.get(),lineas)
            tiem = process.cabeza.obtenerDato().movs.tamano()
            tmn = process.tamano()
            columns = []
            for x in range(0,tmn+1):
                columns.append('#' + str(x+1))

            tree = ttk.Treeview(tab2, show='headings', height=30, columns=columns)
            tree.grid(row=0, column=0, columnspan=2, sticky = tk.W+tk.E+tk.N+tk.S)
            tab2.grid_rowconfigure(0, weight=1)
            tab2.grid_columnconfigure(0, weight=1)
            tab2.grid_columnconfigure(1, weight=1)

            tree.column('#1', width=50, minwidth=50, stretch=tk.NO)
            tree.heading('#1', text='Tiempo', anchor=tk.CENTER)
            for x in range(0,tmn):
                tree.column('#' + str(x+2), width=140, minwidth=140, stretch=tk.NO)
                tree.heading('#' + str(x+2), text='Fila ' + str(x+1), anchor=tk.CENTER)
            
            tp.config(text='Tiempo: ' + str(tiem) + 's')

               

            #Creando Archivo De Salida
            data = ET.Element('SalidaSimulacion')    
            nombre = ET.SubElement(data,'Nombre')  
            nombre.text = combo.get()

            ttamano = process.cabeza.obtenerDato().movs.tamano()

            tiempoTotal = ET.SubElement(data,'TiempoTotal')
            tiempoTotal.text = str(ttamano)

            elaboracionOptima = ET.SubElement(data,'ElaboracionOptima')

            for x in range(0,ttamano):    
                val = []
                val.append(x+1)
                gg = process.cabeza

                tiempo = ET.SubElement(elaboracionOptima,'Tiempo')
                tiempo.set('NoSegundo',str(x+1))
                
                cfil = 0

                while gg != None:
                    cfil += 1
                    ss = gg.obtenerDato().movs.cabeza
                    while ss != None:
                        if (ss.obtenerDato().tiempo) == (x+1):
                            val.append(ss.obtenerDato().accion) 
                            linea = ET.SubElement(tiempo,'LineaEnsamblaje')
                            linea.set('NoLinea',str(cfil))
                            linea.text = ss.obtenerDato().accion
                                  
                        ss = ss.obtenerSiguiente()  
                            
                    gg = gg.obtenerSiguiente()  
                tree.insert("", x, text="", values=val)

            
            # create a new XML file with the results
            mydata = ET.tostring(data)
            myfile = open(combo.get() + '.xml', "wb")
            myfile.write(mydata)
            myfile.close()
                

        
            #for idx in range(100):
            #    tree.insert("", idx, text="", values=([str(idx)],[str(idx)]))
            vsb = ttk.Scrollbar(tab2, orient="vertical", command=tree.yview)
            vsb.grid(row=0, column=2, sticky='ns')

            tree.configure(yscrollcommand=vsb.set)

            hsb = ttk.Scrollbar(tab2, orient="horizontal", command=tree.xview)
            hsb.grid(row = 1, column=0, columnspan=2, sticky = tk.W+tk.E)
            tree.configure(xscrollcommand = hsb.set)

    btnDoubleMirror = Button(window, text="Analizar", command=analizar,height=1,width=15,foreground='#FFFFFF',background='#000000',font=("Arial",9,'bold'))
    btnDoubleMirror.grid(row=0,column=1,padx=0)

    #Listado de Componentes
    #################################################################################################
    lbl = Label(window,text='Componentes Necesarios',font=("Arial",10,'bold'),bg='#FBF3D6')
    lbl.grid(row=1,column=0, sticky='e',ipadx=10)

    lista = Listbox(window,height=5,width=25,font=("Arial",9,'bold'))
    lista.grid(row=2,column=0, sticky='e')
    #for i in range(100):
    #    lista.insert("end", str(i))

    sb = Scrollbar(window,command=lista.yview)
    sb.grid(row=2,column=1,ipady=15, sticky='w')
    lista.config(yscrollcommand=sb.set)

    #Tabla
    #################################################################################################
    note_book = ttk.Notebook(window,width=300,height=200)
    note_book.grid(row=0,column=2,rowspan=5,columnspan=3, sticky='sn',padx=45,pady=45)
    tab2 = ttk.Frame(note_book)

    note_book.add(tab2, text="Tabla", compound=tk.TOP)
    #columns = ('#1', '#2', '#3', '#4', '#5', '#6')
    #tree = ttk.Treeview(tab2, show='headings', height=30, columns=columns)
    #tree.grid(row=0, column=0, columnspan=2, sticky = tk.W+tk.E+tk.N+tk.S)
    #tab2.grid_rowconfigure(0, weight=1)
    #tab2.grid_columnconfigure(0, weight=1)
    #tab2.grid_columnconfigure(1, weight=1)
    #tree.column("#1", width=100, minwidth=100, stretch=tk.NO)
    #tree.column("#2", width=100, minwidth=100, stretch=tk.NO)
    #tree.column("#3", width=100, minwidth=100)
    #tree.column("#4", width=100, minwidth=100, stretch=tk.NO)
    #tree.column("#5", width=100, minwidth=100, stretch=tk.NO)
    #tree.column("#6", width=100, minwidth=100, stretch=tk.NO)
    #tree.heading('#1', text='Estudio', anchor=tk.CENTER)
    #tree.heading('#2', text='Costo', anchor=tk.CENTER)
    #tree.heading('#3', text='Maquila', anchor=tk.CENTER)
    #tree.heading('#4', text='Aaaaaaa', anchor=tk.CENTER)
    #tree.heading('#5', text='Bbbbbbb', anchor=tk.CENTER)
    #tree.heading('#6', text='Ccccccc', anchor=tk.CENTER)
#
    #for idx in range(100):
    #    tree.insert("", idx, text="", values=([str(idx)],[str(idx)]))
    #vsb = ttk.Scrollbar(tab2, orient="vertical", command=tree.yview)
    #vsb.grid(row=0, column=2, sticky='ns')
#
    #tree.configure(yscrollcommand=vsb.set)

    #hsb = ttk.Scrollbar(tab2, orient="horizontal", command=tree.xview)
    #hsb.grid(row = 1, column=0, columnspan=2, sticky = tk.W+tk.E)
    #tree.configure(xscrollcommand = hsb.set)

    #Texto
    tp = Label(window,text='Tiempo: ',font=("Arial",10,'bold'),bg='#FBF3D6')
    tp.grid(row=3,column=2, sticky='e')

    
    window.mainloop()
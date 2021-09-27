from tkinter.constants import NO
from Nodo import Nodo
from graphviz import Digraph,Graph


class LineaMovimiento:
    def __init__(self,no,movs,ultimo):
        self.no = no
        self.movs = movs
        self.ultimo = ultimo

class Movimiento(object):
    def __init__(self,tiempo,accion):
        self.tiempo = tiempo
        self.accion = accion

class Lista:
    def __init__(self):
        self.cabeza = None
        self.ultimo = None

    def agregar(self, item):
        if not self.cabeza:
            self.cabeza = Nodo(item)
            self.ultimo = Nodo(item)
            return
        curr = self.cabeza
        while curr.siguiente:
            curr = curr.siguiente
        curr.siguiente=Nodo(item)
        self.ultimo = Nodo(item)

    def tamano(self):
        actual = self.cabeza
        contador = 0
        if actual != None:
            while actual != None:
                contador = contador + 1
                actual = actual.obtenerSiguiente()
        return contador


    def analizarProducto(self,nombre,filas):
        movimientos = Lista()
        actual = self.cabeza
        while actual != None:

            aux = actual.obtenerDato()
            if aux.nombre == nombre:
                proce = aux.elaboracion
                actualPro = proce.cabeza
                tiempoAnterior = 0

                while actualPro != None:
                    encontrado = False
                    procesoActual = actualPro.obtenerDato()
                    actualfila = filas.cabeza
                    while actualfila != None:
                        f = actualfila.obtenerDato()
                        if f.no == procesoActual.linea:
                            tesamblaje = f.tiempo
                        actualfila = actualfila.obtenerSiguiente()

                    if movimientos.tamano() == 0:
                        encontrado = True
                        pxf = Lista()
                        for t in range(0,procesoActual.columna):
                            nMov = Movimiento(t+1,'Mover - Componente ' + str(t+1))
                            pxf.agregar(nMov)
                        for e in range(0,tesamblaje):
                            nMov = Movimiento(e + procesoActual.columna +1,'Ensamblar - Componente ' + str(procesoActual.columna))
                            pxf.agregar(nMov)

                        nLinea = LineaMovimiento(procesoActual.linea,pxf,procesoActual.columna) 
                        movimientos.agregar(nLinea)     
                        tiempoAnterior = pxf.tamano()
                    else:
                        actualMov = movimientos.cabeza
                        while actualMov != None:

                            br = actualMov.obtenerDato()

                            if br.no == procesoActual.linea:
                                encontrado = True
                                movdelinea = br.movs
                                u = br.ultimo
                                if br.ultimo > procesoActual.columna:    

                                    tt = movdelinea.tamano()
                                    while True:
                                        tt += 1
                                        if movdelinea.tamano() >= tiempoAnterior:
                                            break
                                        else:
                                            nMov = Movimiento(tt,'No Hacer Nada')
                                            movdelinea.agregar(nMov)
                                
                                    ttemp = u - procesoActual.columna
                                    for t in range(0,ttemp):
                                        u -= 1
                                        nMov = Movimiento(1+movdelinea.tamano(),'Mover - Componente ' + str(u))
                                        movdelinea.agregar(nMov)

                                    tt = movdelinea.tamano()
                                    while True:
                                        tt += 1
                                        if movdelinea.tamano() >= tiempoAnterior:
                                            break
                                        else:
                                            nMov = Movimiento(tt,'No Hacer Nada')
                                            movdelinea.agregar(nMov)

                                    for e in range(0,tesamblaje):
                                        nMov = Movimiento(1+movdelinea.tamano(),'Ensamblar - Componente ' + str(procesoActual.columna))
                                        movdelinea.agregar(nMov)
                                    tiempoAnterior = movdelinea.tamano()
                                    br.ultimo = procesoActual.columna
                                elif br.ultimo < procesoActual.columna:
                                    tt = movdelinea.tamano()
                                    while True:
                                        tt += 1
                                        if movdelinea.tamano() >= tiempoAnterior:
                                            break
                                        else:
                                            nMov = Movimiento(tt,'No Hacer Nada')
                                            movdelinea.agregar(nMov)
                                
                                    ttemp = procesoActual.columna - u
                                    for t in range(0,ttemp):
                                        u += 1
                                        nMov = Movimiento(1+movdelinea.tamano(),'Mover - Componente ' + str(u))
                                        movdelinea.agregar(nMov)

                                    tt = movdelinea.tamano()
                                    while True:
                                        tt += 1
                                        if movdelinea.tamano() >= tiempoAnterior:
                                            break
                                        else:
                                            nMov = Movimiento(tt,'No Hacer Nada')
                                            movdelinea.agregar(nMov)

                                    for e in range(0,tesamblaje):
                                        nMov = Movimiento(1+movdelinea.tamano(),'Ensamblar - Componente ' + str(procesoActual.columna))
                                        movdelinea.agregar(nMov)
                                    tiempoAnterior = movdelinea.tamano()
                                    br.ultimo = procesoActual.columna
                                    
                            actualMov = actualMov.obtenerSiguiente()
                    
                    if encontrado == False:
                        pxf = Lista()
                        for t in range(0,procesoActual.columna):
                            nMov = Movimiento(t+1,'Mover - Componente ' + str(t+1))
                            pxf.agregar(nMov)

                        tt = pxf.tamano()
                        while True:
                            tt += 1
                            if pxf.tamano() >= tiempoAnterior:
                                break
                            else:     
                                nMov = Movimiento(tt,'No Hacer Nada')
                                pxf.agregar(nMov)


                        for e in range(0,tesamblaje):
                            nMov = Movimiento(1+pxf.tamano(),'Ensamblar - Componente ' + str(procesoActual.columna))
                            pxf.agregar(nMov)

                        nLinea = LineaMovimiento(procesoActual.linea,pxf,procesoActual.columna) 
                        movimientos.agregar(nLinea)     
                        tiempoAnterior = pxf.tamano()

                    
                    actualPro = actualPro.obtenerSiguiente()

            actual = actual.obtenerSiguiente()
        mayor = 0
        a = movimientos.cabeza
        while a != None:
            mov = (a.obtenerDato()).movs
            if mov.tamano() > mayor:
                mayor = mov.tamano()
            am = mov.cabeza
            a = a.obtenerSiguiente()

        a = movimientos.cabeza
        while a != None:
            mov = (a.obtenerDato()).movs
            if mov.tamano()<mayor:
                v = mayor - mov.tamano()
                tt = mov.tamano()
                for x in range(0,v):
                    #print(tt+x+1)
                    nMov = Movimiento(tt+x+1,'No Hacer Nada')
                    mov.agregar(nMov)

            a = a.obtenerSiguiente()

        #a = movimientos.cabeza   
        #while a != None:
        #    print('Linea ' + str((a.obtenerDato()).no))
        #    mov = (a.obtenerDato()).movs
        #    if mov.tamano() > mayor:
        #        mayor = mov.tamano()
        #    am = mov.cabeza
#
        #    while am != None:
        #        mm = am.obtenerDato()
        #        print(mm.tiempo,mm.accion)
        #        am = am.obtenerSiguiente()
#
        #    a = a.obtenerSiguiente()

        return movimientos

    def proceso(self,nombre):
        actual = self.cabeza
        while actual != None:
            aux = actual.obtenerDato()
            if aux.nombre == nombre:
                proce = aux.elaboracion
                return proce
            actual = actual.obtenerSiguiente()

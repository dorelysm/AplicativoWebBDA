from flask import Flask, redirect, request, jsonify, json, session, render_template, make_response

from config.bd import app, db
from sqlalchemy import select
from flask_bcrypt import check_password_hash

from modelos.Benefactores import Benefactor, BenefactorSchema
from modelos.Usuario import Usuario, UsuarioSchema
from modelos.Beneficiarios import Beneficiario, BeneficiarioSchema
from modelos.Bodega import Bodega, BodegaSchema
from modelos.Categoria import Categoria, CategoriaSchema
from modelos.Subcategoria import Subcategoria, SubcategoriaSchema
from modelos.Vehiculos import Vehiculo, VehiculoSchema
from modelos.Producto import Producto, ProductoSchema
from modelos.Entradas import Entrada, EntradaSchema
from modelos.Salidas import Salida, SalidaSchema
from modelos.Informe import Informe, InformeSchema
from modelos.productos_inventario import Producto_inventario, Producto_inventarioSchema
from modelos.productos_salida import Producto_salida, Producto_salidaSchema

Benefactor_schema = BenefactorSchema()
Benefactores_schema = BenefactorSchema(many=True)

Usuario_schema = UsuarioSchema()
Usuarios_schema = UsuarioSchema(many=True)

Beneficiario_schema = BeneficiarioSchema()
Beneficiarios_schema = BeneficiarioSchema(many=True)

Bodega_schema = BodegaSchema()
Bodegas_schema = BodegaSchema(many=True)

Categoria_schema = CategoriaSchema()
Categorias_schema = CategoriaSchema(many=True)

Subcategoria_schema = SubcategoriaSchema()
Subcategorias_schema = SubcategoriaSchema(many=True)

Vehiculo_schema = VehiculoSchema()
Vehiculos_schema = VehiculoSchema(many=True)

Producto_schema = ProductoSchema()
Productos_schema = ProductoSchema(many=True)

Entrada_schema = EntradaSchema()
Entradas_schema = EntradaSchema(many=True)

Salida_schema = SalidaSchema()
Salidas_schema = SalidaSchema(many=True)

Informe_schema = InformeSchema()
Informes_schema = InformeSchema(many=True)

Producto_inventario_schema = Producto_inventarioSchema()
Productos_inventario_schema = Producto_inventarioSchema(many=True)

Usuarios_schema = UsuarioSchema()
Usuarios_schema = UsuarioSchema(many=True)

Producto_salida_schema = Producto_salidaSchema()
Productos_salida_schema = Producto_salidaSchema(many=True)

productos_lista = []

@app.route('/', methods=['GET'])
def index():  
    return render_template("login.html")

@app.route('/ingresar', methods=['POST'])
def ingresar():
    email = request.form['email']
    password = request.form['password']
    """
    user = db.session.query(Usuario.id).filter(Usuario.email == email, Usuario.password == password).all()
    resultado = Usuarios_schema.dump(user)

    if len(resultado)>0:
        session['usuario'] = email
        return redirect('/inicio')
    else:
        return redirect('/')
    """
    # Busca al usuario por su dirección de correo electrónico
    user = Usuario.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password_hash, password):
        # Verifica si el usuario existe y si la contraseña coincide
        session['usuario'] = email
        session['rol'] = 1
        return redirect('/inicio')
    else:
        return redirect('/')
    
@app.route('/inicio', methods=['GET'])
def inicio():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/cerrar')
def cerrar():
    session.pop('usuario',None)
    return redirect('/')

#METODOS PARA VER PAGINAS

@app.route('/pagina_entradas/', methods=['GET', 'POST'])
def pagina_entradas():
    if 'usuario' in session:
        all_entradas = db.session.query(Entrada.id, Entrada.fecha, Entrada.proceso_de_inventarios, Vehiculo.matricula, Entrada.num_factura, Entrada.num_documento_siigo, Entrada.observaciones, Entrada.tipo, Entrada.ingresado_al_sistema, Benefactor.nombre).join(Benefactor, Entrada.id_benefactor == Benefactor.id).join(Vehiculo, Entrada.id_vehiculo == Vehiculo.id).all()
        pagina_entradas_response = []
        for resultado_entradas in all_entradas:
            pagina_entradas_response.append({
                "id" : resultado_entradas.id,
                "benefactor" : resultado_entradas.nombre,
                "fecha" : resultado_entradas.fecha,
                "proceso_de_inventarios" : resultado_entradas.proceso_de_inventarios,
                "id_vehiculo" : resultado_entradas.matricula,
                "num_factura" : resultado_entradas.num_factura,
                "num_documento_siigo" : resultado_entradas.num_documento_siigo,
                "observaciones" : resultado_entradas.observaciones,
                "tipo" : resultado_entradas.tipo,
                "ingresado_al_sistema" : resultado_entradas.ingresado_al_sistema
            })
        return render_template('entradas.html', entradas = pagina_entradas_response, 
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/cargar_entradas_por_fecha', methods=['GET', 'POST'])
def cargar_entradas_por_fecha():
    if 'usuario' in session:
        fecha_sel = request.form['fecha_datepicker']
        entradas = Entrada.query.filter_by(fecha = fecha_sel)
        resultado_entradas = Entradas_schema.dump(entradas)
        return render_template('entradas.html', entradas = resultado_entradas, 
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/ver_productos_entrada', methods=['GET'] ) 
def ver_productos_entrada():
    id = request.args.get('id')
    productos = Producto_inventario.query.get(id)
    return Producto_inventario_schema.dump(productos)
    
@app.route('/cargar_salidas_por_fecha', methods=['GET', 'POST'])
def cargar_salidas_por_fecha():
    if 'usuario' in session:
        fecha_sel = request.form['fecha_datepicker']
        salidas = Salida.query.filter_by(fecha = fecha_sel)
        resultado_salidas = Salidas_schema.dump(salidas)
        return render_template('salidas.html', salidas = resultado_salidas, 
                               usuario = session['usuario'])
    else:
        return redirect('/')

@app.route('/pagina_salidas', methods=['GET'])
def pagina_salidas():
    if 'usuario' in session:
        all_salidas = db.session.query(Salida.id, Salida.fecha, Salida.observaciones, Salida.tipo, Salida.aporte_solidario, Salida.ingresado_siigo, Salida.num_doc_siigo, Beneficiario.nombre).join(Beneficiario, Salida.id_beneficiario == Beneficiario.num_beneficiario).all()
        pagina_salidas_response = []
        for resultado_salidas in all_salidas:
            pagina_salidas_response.append({
                "id" : resultado_salidas.id,
                "fecha" : resultado_salidas.fecha,
                "observaciones" : resultado_salidas.observaciones,
                "tipo" : resultado_salidas.tipo,
                "aporte_solidario" : resultado_salidas.aporte_solidario,
                "ingresado_siigo" : resultado_salidas.ingresado_siigo,
                "num_doc_siigo" : resultado_salidas.num_doc_siigo,
                "benefactor" : resultado_salidas.nombre,
            })
        return render_template('salidas.html', salidas = pagina_salidas_response, usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/pagina_bodegas', methods=['GET'])
def pagina_bodegas():
    if 'usuario' in session:
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        all_categorias = Categoria.query.all()
        resultado_categorias = Categorias_schema.dump(all_categorias)
        
        #categorias = Categoria.query.filter_by(id_bodega = bodega)
        
        all_subcategorias = Subcategoria.query.all()
        resultado_subcategorias = Subcategorias_schema.dump(all_subcategorias)
        all_productos = Producto.query.all()
        resultado_productos = Productos_schema.dump(all_productos)
        
        return render_template('pproductos.html', bodegas = resultado_bodegas, 
                               categorias = resultado_categorias, 
                               subcategorias = resultado_subcategorias, 
                               productos = resultado_productos,
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/pagina_benefactores', methods=['GET'])
def pagina_benefactores():
    if 'usuario' in session:
        all_benefactores = Benefactor.query.all()
        resultado_benefactores = Benefactores_schema.dump(all_benefactores)
        return render_template('pagina_benefactores.html', benefactores = resultado_benefactores, usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/pagina_beneficiarios', methods=['GET'])
def pagina_beneficiarios():
    if 'usuario' in session:
        all_beneficiarios = Beneficiario.query.all()
        resultado_beneficiarios = Beneficiarios_schema.dump(all_beneficiarios)
        return render_template('pagina_beneficiarios.html', beneficiarios = resultado_beneficiarios, usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/pagina_productos', methods=['GET'])
def pagina_productos():
    if 'usuario' in session:
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        all_categorias = Categoria.query.all()
        resultado_categorias = Categorias_schema.dump(all_categorias)
        all_subcategorias = Subcategoria.query.all()
        resultado_subcategorias = Subcategorias_schema.dump(all_subcategorias)
        all_productos = Producto.query.all()
        resultado_productos = Productos_schema.dump(all_productos)
        return render_template('productos.html', bodegas = resultado_bodegas, 
                               categorias = resultado_categorias, 
                               subcategorias = resultado_subcategorias, 
                               productos = resultado_productos,
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/cargar_categorias_por_bodega', methods=['GET', 'POST'])
def cargar_categorias_por_bodega():
    if 'usuario' in session:
        nombre_bodega_sel = request.form['bodega']
        bodega_sel = Bodega.query.filter_by(nombre = nombre_bodega_sel).first()
        categorias = Categoria.query.filter_by(id_bodega = bodega_sel.id)
        
        resultado_categorias = Categorias_schema.dump(categorias)
        
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        all_subcategorias = Subcategoria.query.all()
        resultado_subcategorias = Subcategorias_schema.dump(all_subcategorias)
        all_productos = Producto.query.all()
        resultado_productos = Productos_schema.dump(all_productos)
        return render_template('productos.html', bodegas = resultado_bodegas,
                               subcategorias = resultado_subcategorias,
                               productos = resultado_productos,
                               categorias = resultado_categorias,
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/cargar_subcategorias_por_categoria', methods=['GET', 'POST'])
def cargar_subcategorias_por_categoria():
    if 'usuario' in session:
        nombre_categoria_sel = request.form['categoria']
        categoria_sel = Categoria.query.filter_by(descripcion = nombre_categoria_sel).first()
        subcategorias = Subcategoria.query.filter_by(categoria = categoria_sel.id)
        resultado_subcategorias = Subcategorias_schema.dump(subcategorias)
        
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        all_categorias = Categoria.query.all()
        resultado_categorias = Categorias_schema.dump(all_categorias)
        all_productos = Producto.query.all()
        resultado_productos = Productos_schema.dump(all_productos)
        return render_template('productos.html', bodegas = resultado_bodegas,
                               subcategorias = resultado_subcategorias,
                               productos = resultado_productos,
                               categorias = resultado_categorias,
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/cargar_productos_por_subcategoria', methods=['GET', 'POST'])
def cargar_productos_por_subcategoria():
    if 'usuario' in session:
        nombre_subcategoria_sel = request.form['subcategoria']
        subcategoria_sel = Subcategoria.query.filter_by(descripcion = nombre_subcategoria_sel).first()
        productos = Producto.query.filter_by(subcategoria = subcategoria_sel.id)
        resultado_productos = Productos_schema.dump(productos)
        
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        all_categorias = Categoria.query.all()
        resultado_categorias = Categorias_schema.dump(all_categorias)
        all_subcategorias = Subcategoria.query.all()
        resultado_subcategorias = Subcategorias_schema.dump(all_subcategorias)
        
        return render_template('productos.html', bodegas = resultado_bodegas,
                               subcategorias = resultado_subcategorias,
                               productos = resultado_productos,
                               categorias = resultado_categorias,
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/pagina_informes', methods=['GET'])
def pagina_informes():
    if 'usuario' in session:
        all_informes = Informe.query.all()
        resultado_informes = Informes_schema.dump(all_informes)
        
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        return render_template('informes.html', informes = resultado_informes, 
                               bodegas = resultado_bodegas, usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/informes_por_mes', methods=['GET', 'POST'])
def informes_por_mes():
    if 'usuario' in session:
        mes = request.form['mes']
        año = request.form['año']
        
        all_informes = Informe.query.filter_by(mes = mes, año = año).all()
        resultado_informes = Informes_schema.dump(all_informes)
        
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        
        #suma_num_kgm = db.session.query(db.func.sum(Producto_inventario.peso)).scalar()

        all_entradas = Entrada.query(Entrada.peso, Bodega.nombre, Categoria.descripcion, \
            Subcategoria.descripcion).join(Producto_inventario, )
        resultado_entradas = Entradas_schema.dump(all_entradas)
        
        for i in resultado_entradas:
            donacion_entrante = 0
            donacion_entrante = donacion_entrante + i['peso']
                
        return render_template('informes.html', informes = resultado_informes, 
                               bodegas = resultado_bodegas, donacion_entrante = donacion_entrante,
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/pagina_inventario', methods=['GET'])
def pagina_inventario():
    if 'usuario' in session:
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        all_categorias = Categoria.query.all()
        resultado_categorias = Categorias_schema.dump(all_categorias)
        all_subcategorias = Subcategoria.query.all()
        resultado_subcategorias = Subcategorias_schema.dump(all_subcategorias)
        all_productos = Producto.query.all()
        resultado_productos = Productos_schema.dump(all_productos)
        all_producto_inventario = Producto_inventario.query.all()
        resultado_productos_inventario = Productos_inventario_schema.dump(all_producto_inventario)
        return render_template('inventario.html', usuario = session['usuario'],
                               bodegas = resultado_bodegas, categorias = resultado_categorias,
                               subcategorias = resultado_subcategorias, productos = resultado_productos,
                               productos_inventario = resultado_productos_inventario)
    else:
        return redirect('/')
    
@app.route('/inventario_por_bodega', methods=['GET', 'POST'])
def inventario_por_bodega():
    if 'usuario' in session:
        nombre_bodega = request.form['bodega']
        bodega = Bodega.query.filter_by(nombre = nombre_bodega).first()
        
        #categorias_de_bodega = Categoria.query.filter_by(id_bodega=bodega.id).all()
        productos_inventario_en_bodega = Producto_inventario.query\
            .join(Producto).join(Subcategoria).join(Categoria).join(Bodega)\
                .filter(Bodega.id == bodega.id).all()
        
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        
        return render_template('inventario.html', usuario = session['usuario'],
                               bodegas = resultado_bodegas,
                               productos_inventario = productos_inventario_en_bodega)
    else:
        return redirect('/')
    
@app.route('/pagina_usuarios', methods=['GET'])
def pagina_usuarios():
    if 'usuario' in session:
        all_usuarios = Usuario.query.all()
        resultado_usuarios = Usuarios_schema.dump(all_usuarios)
        return render_template('usuarios.html', usuarios = resultado_usuarios, usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/pagina_nueva_entrada', methods=['GET'])
def pagina_nueva_entrada():
    if 'usuario' in session:
        all_entradas = Entrada.query.all()
        resultado_entradas = Entradas_schema.dump(all_entradas)
        all_productos = Producto.query.all()
        resultado_productos = Productos_schema.dump(all_productos)
        all_benefactores = Benefactor.query.all()
        resultado_benefactores = Benefactores_schema.dump(all_benefactores)
        all_vehiculos = Vehiculo.query.all()
        resultado_vehiculos = Vehiculos_schema.dump(all_vehiculos)
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        all_categorias = Categoria.query.all()
        resultado_categorias = Categorias_schema.dump(all_categorias)
        all_subcategorias = Subcategoria.query.all()
        resultado_subcategorias = Subcategorias_schema.dump(all_subcategorias)
        
        productos = db.session.query(Producto_inventario.id, \
            Producto_inventario.cantidad_unidades, Producto_inventario.peso, \
                Producto_inventario.vencimiento, Producto.descripcion).all()
        response = []
        for resultado in productos:
            response.append({
                "id" : resultado.id,
                "cantidad_unidades" : resultado.cantidad_unidades,
                "peso" : resultado.peso,
                "vencimiento" : resultado.vencimiento,
                "descripcion" : resultado.descripcion,
            })
        
        return render_template('nueva_entrada.html', entradas = resultado_entradas, 
                               productos = resultado_productos, 
                               benefactores = resultado_benefactores, vehiculos = resultado_vehiculos,
                               productos_inventario = response, 
                               bodegas = resultado_bodegas,
                               categorias = resultado_categorias,
                               subcategorias = resultado_subcategorias,
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/pagina_nueva_salida', methods=['GET'])
def pagina_nueva_salida():
    if 'usuario' in session:
        all_salidas = Salida.query.all()
        resultado_salidas = Salidas_schema.dump(all_salidas)
        all_beneficiarios = Beneficiario.query.all()
        resultado_beneficiarios = Beneficiarios_schema.dump(all_beneficiarios)
        all_producto_inventario = Producto_inventario.query.all()
        resultado_productos_inventario = Productos_inventario_schema.dump(all_producto_inventario)
        all_bodegas = Bodega.query.all()
        resultado_bodegas = Bodegas_schema.dump(all_bodegas)
        all_categorias = Categoria.query.all()
        resultado_categorias = Categorias_schema.dump(all_categorias)
        all_subcategorias = Subcategoria.query.all()
        resultado_subcategorias = Subcategorias_schema.dump(all_subcategorias)
        all_producto_salida = Producto_salida.query.all()
        resultado_productos_salida = Productos_salida_schema.dump(all_producto_salida)
        #sel = select(producto_inventario, producto).where()
        
        return render_template('nueva_salida.html', salidas = resultado_salidas, 
                               beneficiarios = resultado_beneficiarios,
                               productos_inventario = resultado_productos_inventario,
                               bodegas = resultado_bodegas,
                               categorias = resultado_categorias,
                               subcategorias = resultado_subcategorias,
                               productos_salida = resultado_productos_salida,
                               usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/cargar_productos_por_entrada', methods=['GET', 'POST'])
def cargar_productos_por_entrada():
    if 'usuario' in session:
        entrada = request.form['entrada_para_lista']
        
        productos = db.session.query(Producto_inventario.id, \
            Producto_inventario.cantidad_unidades, Producto_inventario.peso, \
                Producto_inventario.vencimiento, Producto.descripcion)\
                    .join(Producto_inventario, Producto.id == Producto_inventario.id_producto).filter_by(id_entrada = entrada).all()
        response = []
        for resultado in productos:
            response.append({
                "id" : resultado.id,
                "cantidad_unidades" : resultado.cantidad_unidades,
                "peso" : resultado.peso,
                "vencimiento" : resultado.vencimiento,
                "descripcion" : resultado.descripcion,
            })
        
        """
        carrito = Producto_inventario.query.filter_by(id_entrada = entrada)
        resultado_carrito = Productos_inventario_schema.dump(carrito)
        """
        all_entradas = Entrada.query.all()
        resultado_entradas = Entradas_schema.dump(all_entradas)
        all_productos = Producto.query.all()
        resultado_productos = Productos_schema.dump(all_productos)
        all_benefactores = Benefactor.query.all()
        resultado_benefactores = Benefactores_schema.dump(all_benefactores)
        all_vehiculos = Vehiculo.query.all()
        resultado_vehiculos = Vehiculos_schema.dump(all_vehiculos)
        
        return render_template('nueva_entrada.html', productos_inventario = response,
                               entradas = resultado_entradas, productos = resultado_productos, 
                               benefactores = resultado_benefactores, vehiculos = resultado_vehiculos,
                               usuario = session['usuario'])
    else:
        return redirect('/')

#METODOS GUARDAR/NUEVO

@app.route('/guardar_entrada', methods=['POST'] )
#@jwt_required()
def guardar_entrada():
    nombre_benefactor = request.form['benefactor']
    fecha = request.form['fecha_datepicker']
    observaciones = request.form['observaciones']
    proceso_de_inventarios = request.form['proceso_de_inventarios']
    matricula_vehiculo = request.form['vehiculo']
    num_factura = request.form['num_factura']
    ingresado_al_sistema = request.form['ingresado_al_sistema']
    tipo = request.form['tipo']
    num_documento_siigo = request.form['num_documento_siigo']
    
    benefactor = Benefactor.query.filter_by(nombre=nombre_benefactor).first()
    vehiculo = Vehiculo.query.filter_by(matricula=matricula_vehiculo).first()
    
    nueva_donacion = Entrada(id_benefactor=benefactor.id, fecha=fecha,
                             observaciones=observaciones, 
                             proceso_de_inventarios=proceso_de_inventarios,
                             id_vehiculo=vehiculo.id, num_factura=num_factura, 
                             ingresado_al_sistema=ingresado_al_sistema,
                             tipo=tipo, num_documento_siigo=num_documento_siigo)

    db.session.add(nueva_donacion)
    db.session.commit()
    return redirect('/pagina_nueva_entrada')

@app.route('/guardar_salida', methods=['POST'] )
def guardar_salida():
    nombre_beneficiario = request.form['beneficiario']
    fecha = request.form['fecha_datepicker']
    tipo = request.form['tipo']
    ingresado_siigo = request.form['siigo']
    num_doc_siigo = request.form['num_doc_siigo']
    observaciones = request.form['observaciones']
    
    beneficiario = Beneficiario.query.filter_by(nombre=nombre_beneficiario).first()
    
    nueva_donacion = Salida(id_beneficiario = beneficiario.num_beneficiario, 
                            fecha = fecha, tipo = tipo, 
                            ingresado_siigo = ingresado_siigo, 
                            num_doc_siigo = num_doc_siigo, 
                            observaciones = observaciones)

    db.session.add(nueva_donacion)
    db.session.commit()
    return redirect('/pagina_nueva_salida')

@app.route('/nuevo_beneficiario', methods=['POST'] )
def guardar_beneficiario():
    nombre = request.form['nombre']
    cc = request.form['cc']
    contacto = request.form['contacto']
    direccion = request.form['direccion']
    
    Nuevo_beneficiario = Beneficiario(nombre, cc, contacto, direccion)

    db.session.add(Nuevo_beneficiario)
    db.session.commit()
    return redirect('/pagina_nueva_salida')

@app.route('/nueva_bodega', methods=['POST'] )
def guardar_bodega():
    nombre = request.form['nombre']
    
    Nuevo_bodega = Bodega(nombre)

    db.session.add(Nuevo_bodega)
    db.session.commit()
    return redirect('/pagina_productos')

@app.route('/nueva_categoria', methods=['POST'] )
def guardar_categoria():
    nombre_bodega = request.form['bodega']
    descripcion = request.form['descripcion']
    
    bodega = Bodega.query.filter_by(nombre=nombre_bodega).first()
    #print(bodega.id)
    Nuevo_categoria = Categoria(bodega.id, descripcion)

    db.session.add(Nuevo_categoria)
    db.session.commit()
    return redirect('/pagina_productos')

@app.route('/nueva_subcategoria', methods=['POST'] )
def guardar_subcategoria():
    nombre_categoria = request.form['categoria']
    descripcion = request.form['descripcion']
    
    categoria = Categoria.query.filter_by(descripcion=nombre_categoria).first()
    
    Nuevo_subcategoria = Subcategoria(categoria.id, descripcion)

    db.session.add(Nuevo_subcategoria)
    db.session.commit()
    return redirect('/pagina_productos')

@app.route('/nuevo_producto', methods=['POST'] )
def guardar_producto():
    nombre_subcategoria = request.form['subcategoria']
    descripcion = request.form['descripcion']
    peso = request.form['peso']
    
    subcategoria = Subcategoria.query.filter_by(descripcion = nombre_subcategoria).first()
    
    Nuevo_producto = Producto(subcategoria.id, descripcion, peso)

    db.session.add(Nuevo_producto)
    db.session.commit()
    return redirect('/pagina_productos')

@app.route('/nuevo_vehiculo', methods=['POST'] )
def guardar_vehiculo():
    matricula = request.form['matricula']
    tipo = request.form['tipo']
    capacidad = request.form['capacidad']
    empresa = request.form['empresa']
    
    Nuevo_vehiculo = Vehiculo(matricula, tipo, capacidad, empresa)

    db.session.add(Nuevo_vehiculo)
    db.session.commit()
    return redirect('/pagina_nueva_entrada')

@app.route('/nuevo_usuario', methods=['POST'] )
def guardar_usuario():
    email = request.form['email']
    password = request.form['password']
    nombre = request.form['nombre']
    cedula = request.form['cedula']
    rol = request.form['rol']
    
    Nuevo_usuario = Usuario(email, password, nombre, cedula, rol)

    db.session.add(Nuevo_usuario)
    db.session.commit()
    return redirect('/pagina_usuarios')

@app.route('/nuevo_benefactor', methods=['POST'] )
def guardar_benefactor():
    nombre = request.form['nombre']
    nit = request.form['nit']
    contacto = request.form['contacto']
    direccion = request.form['direccion']
    
    Nuevo_benefactor = Benefactor(nombre, nit, contacto, direccion)

    db.session.add(Nuevo_benefactor)
    db.session.commit()
    return redirect('/pagina_nueva_entrada')

@app.route('/nuevo_producto_inventario', methods=['POST'] )
def guardar_producto_inventario():
    id_entrada = request.form['entrada']
    desc_producto = request.form['producto']
    cantidad = request.form['cantidad_unidades']
    peso = request.form['peso']
    vencimiento = request.form['vencimiento_datepicker']
    print(desc_producto)
    #entrada = Entrada.query.filter_by()
    producto = Producto.query.filter_by(descripcion = desc_producto).first()

    Nuevo_producto_inventario = Producto_inventario(id_entrada=id_entrada ,id_producto=producto.id, 
                                                    cantidad_unidades=cantidad, peso=peso, 
                                                    vencimiento=vencimiento)

    db.session.add(Nuevo_producto_inventario)
    
    entrada = Entrada.query.get(id_entrada)
    entrada.peso = entrada.peso + int(peso)
    
    db.session.commit()
    return redirect('/pagina_nueva_entrada')

@app.route('/nuevo_producto_salida', methods=['POST'] )
def nuevo_producto_salida():
    id_salida = request.form['salida']
    id_producto_inventario = request.form['producto_inventario']
    cantidad = request.form['cantidad_unidades']
    peso = request.form['peso']
    aporte_solidario = request.form['aporte_solidario']
    
    #producto_inventario = Producto_inventario.query.filter_by(id=producto).first()

    nuevo_producto_salida = Producto_salida(id_salida=id_salida, 
                                            id_producto_inventario=id_producto_inventario, 
                                            cantidad_unidades=cantidad, 
                                            peso=peso, 
                                            aporte_solidario=aporte_solidario)

    db.session.add(nuevo_producto_salida)
    db.session.commit()
    
    #Restar a producto_inventario la cantidad y el peso de la nueva donacion

    producto = Producto_inventario.query.get(id_producto_inventario)
    
    producto.peso = producto.peso - int(peso)
    producto.cantidad_unidades = producto.cantidad_unidades - int(cantidad)

    db.session.commit()
    
    return redirect('/pagina_nueva_salida')
    
#METODOS ELIMINAR

@app.route('/eliminar_entrada', methods=['GET'] )
def eliminar():
    id = request.args.get('id')
    
    #all_producto_inventario = Producto_inventario.query.all()
    all_producto_inventario = Producto_inventario.query.filter_by(id_entrada = id)
    
    #resultado_productos_inventario = Productos_inventario_schema.dump(all_producto_inventario)
    print(all_producto_inventario)
    
    for i in all_producto_inventario:
        if i.id_entrada == id:
            db.session.delete(i)
    
    entradas = Entrada.query.get(id)
    db.session.delete(entradas)
    db.session.commit()
    return Entrada_schema.dump(entradas)

@app.route('/eliminar_salida', methods=['GET'] )
def eliminar_salida():
    id = request.args.get('id')
    salidas = Salida.query.get(id)
    db.session.delete(salidas)
    db.session.commit()
    return Salida_schema.dump(salidas)

@app.route('/eliminar_producto', methods=['GET'] )
def eliminar_producto():
    id = request.args.get('id')
    productos = Producto.query.get(id)
    db.session.delete(productos)
    db.session.commit()
    return Producto_schema.dump(productos)

@app.route('/eliminar_producto_inventario', methods=['GET'] )
def eliminar_producto_inventario():
    id = request.args.get('id')
    producto = Producto_inventario.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return Producto_inventario_schema.dump(producto)

@app.route('/eliminar_producto_salida', methods=['GET'] )
def eliminar_producto_salida():
    id = request.args.get('id')
    producto = Producto_salida.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return Producto_salida_schema.dump(producto)

@app.route('/eliminar_bodega', methods=['GET'] )
def eliminar_bodega():
    id = request.args.get('id')
    bodegas = Bodega.query.get(id)
    db.session.delete(bodegas)
    db.session.commit()
    return Bodega_schema.dump(bodegas)

@app.route('/eliminar_benefactor', methods=['GET'] )
def eliminar_benefactor():
    id = request.args.get('id')
    benefactores = Benefactor.query.get(id)
    db.session.delete(benefactores)
    db.session.commit()
    return Benefactor_schema.dump(benefactores)

@app.route('/eliminar_beneficiario', methods=['GET'] )
def eliminar_beneficiario():
    id = request.args.get('id')
    beneficiarios = Beneficiario.query.get(id)
    db.session.delete(beneficiarios)
    db.session.commit()
    return Beneficiario_schema.dump(beneficiarios)

@app.route('/eliminar_categoria', methods=['GET'] )
def eliminar_categoria():
    id = request.args.get('id')
    categorias = Categoria.query.get(id)
    db.session.delete(categorias)
    db.session.commit()
    return Categoria_schema.dump(categorias)

@app.route('/eliminar_subcategoria', methods=['GET'] )
def eliminar_subcategoria():
    id = request.args.get('id')
    subcategorias = Subcategoria.query.get(id)
    db.session.delete(subcategorias)
    db.session.commit()
    return Subcategoria_schema.dump(subcategorias)

@app.route('/eliminar_vehiculo', methods=['GET'] )
def eliminar_vehiculo():
    id = request.args.get('id')
    vehiculos = Vehiculo.query.get(id)
    db.session.delete(vehiculos)
    db.session.commit()
    return Vehiculo_schema.dump(vehiculos)

@app.route('/eliminar_usuario', methods=['GET'] )
def eliminar_usuario():
    id = request.args.get('id')
    usuarios = Usuario.query.get(id)
    db.session.delete(usuarios)
    db.session.commit()
    return Usuario_schema.dump(usuarios)

@app.route('/eliminar_informe', methods=['GET'] )
def eliminar_informe():
    id = request.args.get('id')
    informes = Informe.query.get(id)
    db.session.delete(informes)
    db.session.commit()
    return Informe_schema.dump(informes)

#METODOS GET LISTA

@app.route('/entradas', methods=['GET', 'POST'] )
def entradas():
    id = request.args.get('id')
    entradas = Entrada.query.get(id)
    restul_entradas = Entrada_schema.dump(entradas)
    return jsonify(restul_entradas)

@app.route('/salidas', methods=['GET', 'POST'] )
def salidas():
    id = request.args.get('id')
    salidas = Salida.query.get(id)
    restul_salida = Salida_schema.dump(salidas)
    return jsonify(restul_salida)

@app.route('/benefactores', methods=['GET'] )
def benefactores():
    id = request.args.get('id')
    benefactores = Benefactor.query.get(id)
    restul_benefactor = Benefactor_schema.dump(benefactores)
    return jsonify(restul_benefactor)

@app.route('/beneficiarios', methods=['GET'] )
def beneficiarios():
    id = request.args.get('num_beneficiario')
    beneficiarios = Beneficiario.query.get(id)
    restul_beneficiario = Beneficiario_schema.dump(beneficiarios)
    return jsonify(restul_beneficiario)

@app.route('/bodegas', methods=['GET'] )
def bodegas():
    id = request.args.get('id')
    bodegas = Bodega.query.get(id)
    restul_bodega = Bodega_schema.dump(bodegas)
    return jsonify(restul_bodega)

@app.route('/categorias', methods=['GET'] )
def categorias():
    id = request.args.get('id')
    categorias = Categoria.query.get(id)
    restul_categoria = Categoria_schema.dump(categorias)
    return jsonify(restul_categoria)

@app.route('/categorias_de_bodega', methods=['GET'] ) #Nueva
def categorias_de_bodega():
    id = request.args.get('id')
    bodega = request.args.get('bodega_id')
    #Subcategoria.query.filter_by(descripcion = nombre_subcategoria).first()
    categorias = Categoria.query.filter_by(id_bodega = bodega)
    restul_categoria = Categoria_schema.dump(categorias)
    return jsonify(restul_categoria)

@app.route('/subcategorias', methods=['GET'] )
def subcategorias():
    id = request.args.get('id')
    subcategorias = Subcategoria.query.get(id)
    restul_subcategoria = Subcategoria_schema.dump(subcategorias)
    return jsonify(restul_subcategoria)

@app.route('/vehiculos', methods=['GET'] )
def vehiculos():
    id = request.args.get('id')
    vehiculos = Vehiculo.query.get(id)
    restul_vehiculo = Vehiculo_schema.dump(vehiculos)
    return jsonify(restul_vehiculo)

@app.route('/productos', methods=['GET'] )
def productos():
    id = request.args.get('id')
    productos = Producto.query.get(id)
    restul_producto = Producto_schema.dump(productos)
    return jsonify(restul_producto)

@app.route('/productos_inventario', methods=['GET'] )
def productos_inventario():
    id = request.args.get('id')
    productos = Producto_inventario.query.get(id)
    restul_producto = Producto_inventario_schema.dump(productos)
    return jsonify(restul_producto)

@app.route('/productos_salida', methods=['GET'] )
def productos_salida():
    id = request.args.get('id')
    productos = Producto_salida.query.get(id)
    restul_producto = Producto_salida_schema.dump(productos)
    return jsonify(restul_producto)

@app.route('/informes', methods=['GET'] )
def informes():
    id = request.args.get('id')
    informes = Informe.query.get(id)
    restul_informe = Informe_schema.dump(informes)
    return jsonify(restul_informe)

@app.route('/usuarios', methods=['GET'] )
def usuarios():
    id = request.args.get('id')
    usuarios = Usuario.query.get(id)
    restul_usuario = Usuario_schema.dump(usuarios)
    return jsonify(restul_usuario)

#METODOS ACTUALIZAR

@app.route('/actualizar_entrada', methods=['POST'] )
def actualizar_entrada():
    id = request.form['id']
    id_benefactor = request.form['id_benefactor']
    fecha = request.form['fecha']
    observaciones = request.form['observaciones']
    proceso_de_inventarios = request.form['proceso_de_inventarios']
    id_vehiculo = request.form['id_vehiculo']
    num_factura = request.form['num_factura']
    ingresado_al_sistema = request.form['ingresado_al_sistema']
    tipo = request.form['tipo']
    num_documento_siigo = request.form['num_documento_siigo']

    entrada = Entrada.query.get(id)
    entrada.id_benefactor = id_benefactor
    entrada.fecha = fecha
    entrada.observaciones = observaciones
    entrada.proceso_de_inventarios = proceso_de_inventarios
    entrada.id_vehiculo = id_vehiculo
    entrada.num_factura = num_factura
    entrada.ingresado_al_sistema = ingresado_al_sistema
    entrada.tipo = tipo
    entrada.num_documento_siigo = num_documento_siigo

    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/actualizar_salida', methods=['POST'] )
def actualizar_salida():
    id = request.form['id']
    id_beneficiario = request.form['id_beneficiario']
    fecha = request.form['fecha']
    tipo = request.form['tipo']
    num_doc_siigo = request.form['num_doc_siigo']
    observaciones = request.form['observaciones']

    salida = Salida.query.get(id)
    
    salida.id_beneficiario = id_beneficiario
    salida.fecha = fecha
    salida.tipo = tipo
    salida.num_doc_siigo = num_doc_siigo
    salida.observaciones = observaciones

    db.session.commit()
    return redirect('/pagina_salidas')

@app.route('/actualizar_producto_inventario', methods=['POST'] )
def actualizar_producto_inventario():
    id = request.form['id']
    id_entrada = request.form['id_entrada']
    id_producto = request.form['id_producto']
    cantidad_unidades = request.form['cantidad_unidades']
    peso = request.form['peso']
    vencimiento = request.form['vencimiento']

    producto = Producto_inventario.query.get(id)
    
    producto.id_entrada = id_entrada
    producto.id_producto = id_producto
    producto.cantidad_unidades = cantidad_unidades
    producto.peso = peso
    producto.vencimiento = vencimiento

    db.session.commit()
    return redirect('/pagina_nueva_entrada')

@app.route('/actualizar_producto_salida', methods=['POST'] )
def actualizar_producto_salida():
    id = request.form['id']
    id_salida = request.form['id_salida']
    id_producto_inventario = request.form['id_producto_inventario']
    cantidad = request.form['cantidad_unidades']
    peso = request.form['peso']
    aporte_solidario = request.form['aporte_solidario']
    
    producto = Producto_salida.query.get(id)
    
    producto.id_salida = id_salida
    producto.id_producto_inventario = id_producto_inventario
    producto.cantidad_unidades = cantidad
    producto.peso = peso
    producto.aporte_solidario = aporte_solidario

    db.session.commit()
    return redirect('/pagina_nueva_salida')

@app.route('/actualizar_bodega', methods=['POST'] )
def actualizar_bodega():
    id = request.form['id']
    nombre = request.form['nombre']

    bodega = Bodega.query.get(id)
    bodega.id = id
    bodega.nombre = nombre

    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/actualizar_benefactor', methods=['POST'] )
def actualizar_benefactor():
    id = request.form['id']
    nombre = request.form['nombre']
    contacto = request.form['contacto']
    direccion = request.form['direccion']

    benefactor = Benefactor.query.get(id)
    benefactor.id = id
    benefactor.nombre = nombre
    benefactor.contacto = contacto
    benefactor.direccion = direccion

    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/actualizar_beneficiario', methods=['POST'] )
def actualizar_beneficiario():
    num_beneficiario = request.form['num_beneficiario']
    nombre = request.form['nombre']
    contacto = request.form['contacto']
    direccion = request.form['direccion']

    beneficiario = Beneficiario.query.get(num_beneficiario)
    beneficiario.num_beneficiario = num_beneficiario
    beneficiario.nombre = nombre
    beneficiario.contacto = contacto
    beneficiario.direccion = direccion

    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/actualizar_categoria', methods=['POST'] )
def actualizar_categoria():
    id = request.form['id']
    id_bodega = request.form['id_bodega']
    descripcion = request.form['descripcion']

    categoria = Categoria.query.get(id)
    categoria.id = id
    categoria.id_bodega = id_bodega
    categoria.descripcion = descripcion

    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/actualizar_subcategoria', methods=['POST'] )
def actualizar_subcategoria():
    id = request.form['id']
    categoria = request.form['categoria']
    descripcion = request.form['descripcion']

    subcategoria = Subcategoria.query.get(id)
    subcategoria.id = id
    subcategoria.categoria = categoria
    subcategoria.descripcion = descripcion

    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/actualizar_vehiculo', methods=['POST'] )
def actualizar_vehiculo():
    id = request.form['id']
    matricula = request.form['matricula']
    conductor = request.form['conductor']

    vehiculo = Vehiculo.query.get(id)
    vehiculo.id = id
    vehiculo.matricula = matricula
    vehiculo.conductor = conductor

    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/actualizar_producto', methods=['POST'] )
def actualizar_producto():
    id = request.form['id']
    subcategoria = request.form['subcategoria']
    descripcion = request.form['descripcion']
    peso = request.form['peso']

    producto = Producto.query.get(id)
    producto.id = id
    producto.subcategoria = subcategoria
    producto.descripcion = descripcion
    producto.peso = peso
    
    db.session.commit()
    return redirect('/pagina_productos')
    
@app.route('/actualizar_usuario', methods=['POST'] )
def actualizar_usuario():
    id = request.form['id']
    email = request.form['email']
    password = request.form['password']

    usuario = Usuario.query.get(id)
    usuario.id = id
    usuario.email = email
    usuario.password = password

    db.session.commit()
    return redirect('/pagina_entradas')


    


if __name__ == "__main__":
    app.run(debug=True)


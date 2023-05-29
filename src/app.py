from flask import Flask, redirect, request, jsonify, json, session, render_template, make_response

from config.bd import app, db

from modelos.Benefactores import Benefactor, BenefactorSchema
from modelos.Usuario import Usuario, UsuarioSchema
from modelos.Beneficiarios import Beneficiario, BeneficiarioSchema
from modelos.Categoria import Categoria, CategoriaSchema
from modelos.Bodega import Bodega, BodegaSchema
from modelos.Subcategoria import Subcategoria, SubcategoriaSchema
from modelos.Vehiculos import Vehiculo, VehiculoSchema
from modelos.Entradas import Entrada, EntradaSchema
from modelos.Salidas import Salida, SalidaSchema
from modelos.Mermas import Merma, MermaSchema


Benefactor_schema = BenefactorSchema()
Benefactores_schema = BenefactorSchema(many=True)

Usuario_schema = UsuarioSchema()
Usuarios_schema = UsuarioSchema(many=True)

Beneficiario_schema = BeneficiarioSchema()
Beneficiarios_schema = BeneficiarioSchema(many=True)

Categoria_schema = CategoriaSchema()
Categorias_schema = CategoriaSchema(many=True)

Entrada_schema = EntradaSchema()
Entradas_schema = EntradaSchema(many=True)

Salida_schema = SalidaSchema()
Salidas_schema = SalidaSchema(many=True)

Bodega_schema = BodegaSchema()
Bodegas_schema = BodegaSchema(many=True)

Subcategoria_schema = SubcategoriaSchema()
Subcategorias_schema = SubcategoriaSchema(many=True)

Vehiculo_schema = VehiculoSchema()
Vehiculos_schema = VehiculoSchema(many=True)

Merma_schema = MermaSchema()
Mermas_schema = MermaSchema(many=True)

@app.route('/', methods=['GET'])
def index():  
    return render_template("login.html")

@app.route('/ingresar', methods=['POST'])
def ingresar():
    email = request.form['email']
    password = request.form['password']
    user = db.session.query(Usuario.id).filter(Usuario.email == email, Usuario.password == password).all()
    resultado = Usuarios_schema.dump(user)

    if len(resultado)>0:
        session['usuario'] = email
        return redirect('/inicio')
    else:
        return redirect('/')
    
@app.route('/inicio', methods=['GET'])
def inicio():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario = session['usuario'])

@app.route('/pagina_entradas', methods=['GET'])
def pagina_entradas():
    if 'usuario' in session:
        all_entradas = Entrada.query.all()
        resultado_entradas = Entradas_schema.dump(all_entradas)
        return render_template('entradas.html', entradas = resultado_entradas, usuario = session['usuario'])
    else:
        return redirect('/')

@app.route('/pagina_salidas', methods=['GET'])
def pagina_salidas():
    if 'usuario' in session:
        all_salidas = Salida.query.all()
        resultado_salidas = Salidas_schema.dump(all_salidas)
        return render_template('pagina_salidas.html', salidas = resultado_salidas, usuario = session['usuario'])
    else:
        return redirect('/')
    
@app.route('/cerrar')
def cerrar():
    session.pop('usuario',None)
    return redirect('/')

@app.route('/guardar_entrada', methods=['POST'] )
#@jwt_required()
def guardar_entrada():
    id_benefactor = request.form['id_benefactor']
    id_categoria = request.form['id_categoria']
    fecha = request.form['fecha']
    cantidad_peso = request.form['cantidad_peso']
    cantidad_unidades = request.form['cantidad_unidades']
    unidad_de_medida = request.form['unidad_de_medida']
    bodega = request.form['bodega']
    observaciones = request.form['observaciones']
    proceso_de_inventarios = request.form['proceso_de_inventarios']
    id_vehiculo = request.form['id_vehiculo']
    num_factura = request.form['num_factura']
    ingresado_al_sistema = request.form['ingresado_al_sistema']
    tipo = request.form['tipo']
    num_documento_siigo = request.form['num_documento_siigo']
    cantidad_averiada_vencida_kg = request.form['cantidad_averiada_vencida_kg']
    cantidad_buen_estado_kg = request.form['cantidad_buen_estado_kg']
    cantidad_aprobada_kg = request.form['cantidad_aprobada_kg']
    
    nueva_donacion = Entrada(id_benefactor=id_benefactor, id_categoria=id_categoria,
                             fecha=fecha, cantidad_peso=cantidad_peso,
                             cantidad_unidades=cantidad_unidades, unidad_de_medida=unidad_de_medida,
                             bodega=bodega, observaciones=observaciones, proceso_de_inventarios=proceso_de_inventarios,
                             id_vehiculo=id_vehiculo, num_factura=num_factura, ingresado_al_sistema=ingresado_al_sistema,
                             tipo=tipo, num_documento_siigo=num_documento_siigo,
                             cantidad_averiada_vencida_kg=cantidad_averiada_vencida_kg,
                             cantidad_buen_estado_kg=cantidad_buen_estado_kg,
                             cantidad_aprobada_kg=cantidad_aprobada_kg)

    db.session.add(nueva_donacion)
    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/eliminar_entrada', methods=['GET'] )
def eliminar():
    id = request.args.get('id')
    entradas = Entrada.query.get(id)
    db.session.delete(entradas)
    db.session.commit()
    return Entrada_schema.dump(entradas)

@app.route('/entradas', methods=['GET'] )
def entradas():
    id = request.args.get('id')
    entradas = Entrada.query.get(id)
    restul_entradas = Entrada_schema.dump(entradas)
    return jsonify(restul_entradas)

@app.route('/actualizar_entrada', methods=['POST'] )
def actualizar():
    id = request.form['id']
    #print('id: ', id)
    id_benefactor = request.form['id_benefactor']
    id_categoria = request.form['id_categoria']
    fecha = request.form['fecha']
    cantidad_peso = request.form['cantidad_peso']
    cantidad_unidades = request.form['cantidad_unidades']
    unidad_de_medida = request.form['unidad_de_medida']
    bodega = request.form['bodega']
    observaciones = request.form['observaciones']
    proceso_de_inventarios = request.form['proceso_de_inventarios']
    id_vehiculo = request.form['id_vehiculo']
    num_factura = request.form['num_factura']
    ingresado_al_sistema = request.form['ingresado_al_sistema']
    tipo = request.form['tipo']
    num_documento_siigo = request.form['num_documento_siigo']
    cantidad_averiada_vencida_kg = request.form['cantidad_averiada_vencida_kg']
    cantidad_buen_estado_kg = request.form['cantidad_buen_estado_kg']
    cantidad_aprobada_kg = request.form['cantidad_aprobada_kg']

    entrada = Entrada.query.get(id)
    entrada.id_benefactor = id_benefactor
    entrada.id_categoria = id_categoria
    entrada.fecha = fecha
    entrada.cantidad_peso = cantidad_peso
    entrada.cantidad_unidades = cantidad_unidades
    entrada.unidad_de_medida = unidad_de_medida
    entrada.bodega = bodega
    entrada.observaciones = observaciones
    entrada.proceso_de_inventarios = proceso_de_inventarios
    entrada.id_vehiculo = id_vehiculo
    entrada.num_factura = num_factura
    entrada.ingresado_al_sistema = ingresado_al_sistema
    entrada.tipo = tipo
    entrada.num_documento_siigo = num_documento_siigo
    entrada.cantidad_averiada_vencida_kg = cantidad_averiada_vencida_kg
    entrada.cantidad_buen_estado_kg = cantidad_buen_estado_kg
    entrada.cantidad_aprobada_kg = cantidad_aprobada_kg

    db.session.commit()
    return redirect('/pagina_entradas')

@app.route('/guardar_salida', methods=['POST'] )
def guardar_salida():
    id_beneficiario = request.form['id_beneficiario']
    id_entrada = request.form['id_entrada']
    fecha = request.form['fecha']
    bodega = request.form['bodega']
    cantidad_peso = request.form['cantidad_peso']
    cantidad_unidades = request.form['cantidad_unidades']
    unidad_de_medida = request.form['unidad_de_medida']
    aporte_solidario = request.form['aporte_solidario']
    observaciones = request.form['observaciones']
    
    nueva_donacion = Salida(id_beneficiario, id_entrada, fecha, bodega, cantidad_peso, cantidad_unidades, unidad_de_medida, aporte_solidario, observaciones)

    db.session.add(nueva_donacion)
    db.session.commit()
    return redirect('/pagina_salidas')

@app.route('/eliminar_salida', methods=['GET'] )
def eliminar_salida():
    id = request.args.get('id')
    salidas = Salida.query.get(id)
    db.session.delete(salidas)
    db.session.commit()
    return Salida_schema.dump(salidas)

@app.route('/salidas', methods=['GET'] )
def salidas():
    id = request.args.get('id')
    salidas = Salida.query.get(id)
    restul_salida = Salida_schema.dump(salidas)
    return jsonify(restul_salida)

@app.route('/actualizar_salida', methods=['POST'] )
def actualizar_salida():
    id = request.form['id']
    id_beneficiario = request.form['id_beneficiario']
    id_entrada = request.form['id_entrada']
    fecha = request.form['fecha']
    bodega = request.form['bodega']
    cantidad_peso = request.form['cantidad_peso']
    cantidad_unidades = request.form['cantidad_unidades']
    unidad_de_medida = request.form['unidad_de_medida']
    aporte_solidario = request.form['aporte_solidario']
    observaciones = request.form['observaciones']

    salida = Salida.query.get(id)
    salida.id_beneficiario = id_beneficiario
    salida.id_entrada = id_entrada
    salida.fecha = fecha
    salida.bodega = bodega
    salida.cantidad_peso = cantidad_peso
    salida.cantidad_unidades = cantidad_unidades
    salida.unidad_de_medida = unidad_de_medida
    salida.aporte_solidario = aporte_solidario
    salida.observaciones = observaciones

    db.session.commit()
    return redirect('/pagina_salidas')

@app.route('/pagina_benefactores', methods=['GET'])
def pagina_benefactores():
    if 'usuario' in session:
        all_benefactores = Benefactor.query.all()
        resultado_benefactores = Benefactores_schema.dump(all_benefactores)
        return render_template('pagina_benefactores.html', benefactores = resultado_benefactores, usuario = session['usuario'])
    else:
        return redirect('/')

@app.route('/nuevo_benefactor', methods=['POST'] )
def guardar_benefactor():
    nombre = request.form['nombre']
    contacto = request.form['contacto']
    direccion = request.form['direccion']
    
    Nuevo_benefactor = Benefactor(nombre, contacto, direccion)

    db.session.add(Nuevo_benefactor)
    db.session.commit()
    return redirect('/pagina_benefactores')

@app.route('/pagina_beneficiarios', methods=['GET'])
def pagina_beneficiarios():
    if 'usuario' in session:
        all_beneficiarios = Beneficiario.query.all()
        resultado_beneficiarios = Beneficiario_schema.dump(all_beneficiarios)
        return render_template('pagina_beneficiarios.html', beneficiarios = resultado_beneficiarios, usuario = session['usuario'])
    else:
        return redirect('/')

@app.route('/nuevo_beneficiario', methods=['POST'] )
def guardar_beneficiario():
    nombre = request.form['nombre']
    contacto = request.form['contacto']
    direccion = request.form['direccion']
    
    Nuevo_beneficiario = Beneficiario(nombre, contacto, direccion)

    db.session.add(Nuevo_beneficiario)
    db.session.commit()
    return redirect('/pagina_beneficiarios')

@app.route('/nueva_bodega', methods=['POST'] )
def guardar_bodega():
    nombre = request.form['nombre']
    
    Nuevo_bodega = Bodega(nombre)

    db.session.add(Nuevo_bodega)
    db.session.commit()
    return redirect('/inicio')

@app.route('/nueva_categoria', methods=['POST'] )
def guardar_categoria():
    id_bodega = request.form['id_bodega']
    descripcion = request.form['descripcion']
    
    Nuevo_categoria = Categoria(id_bodega, descripcion)

    db.session.add(Nuevo_categoria)
    db.session.commit()
    return redirect('/inicio')

@app.route('/nueva_subcategoria', methods=['POST'] )
def guardar_subcategoria():
    id_categoria = request.form['id_categoria']
    descripcion = request.form['descripcion']
    
    Nuevo_subcategoria = Subcategoria(id_categoria, descripcion)

    db.session.add(Nuevo_subcategoria)
    db.session.commit()
    return redirect('/inicio')

@app.route('/nuevo_vehiculo', methods=['POST'] )
def guardar_vehiculo():
    matricula = request.form['matricula']
    conductor = request.form['conductor']
    
    Nuevo_vehiculo = Vehiculo(matricula, conductor)

    db.session.add(Nuevo_vehiculo)
    db.session.commit()
    return redirect('/inicio')

@app.route('/nueva_merma', methods=['POST'] )
def guardar_merma():
    id_entrada = request.form['id_entrada']
    tipo = request.form['tipo']
    fecha = request.form['fecha']
    cantidad_peso = request.form['cantidad_peso']
    cantidad_unidades = request.form['cantidad_unidades']
    unidad_de_medida = request.form['unidad_de_medida']
    observaciones = request.form['observaciones']
    num_doc_merma_siigo = request.form['num_doc_merma_siigo']
    
    Nueva_merma = Merma(id_entrada, tipo, fecha, cantidad_peso, cantidad_unidades,
                        unidad_de_medida, observaciones, num_doc_merma_siigo)

    db.session.add(Nueva_merma)
    db.session.commit()
    return redirect('/inicio')

@app.route('/benefactores', methods=['GET'] )
def benefactores():
    id = request.args.get('id')
    benefactores = Benefactor.query.get(id)
    restul_benefactor = Benefactor_schema.dump(benefactores)
    return jsonify(restul_benefactor)

@app.route('/beneficiarios', methods=['GET'] )
def beneficiarios():
    id = request.args.get('id')
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

@app.route('/subcategorias', methods=['GET'] )
def categorias():
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

if __name__ == "__main__":
    app.run(debug=True)


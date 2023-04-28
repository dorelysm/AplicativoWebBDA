from flask import Flask, redirect, request, jsonify, json, session, render_template, make_response

from config.bd import app, db
from config.token import generar_token, verificar_token
from modelos.Benefactores import Benefactor, BenefactorSchema
from modelos.Usuario import Usuario, UsuarioSchema
from modelos.Beneficiarios import Beneficiario, BeneficiarioSchema
from modelos.Categoria import Categoria, CategoriaSchema
from modelos.Entradas import Entrada, EntradaSchema
from modelos.Salidas import Salida, SalidaSchema
from modelos.Blockchain import Blockchain
from modelos.Tokens import Token, TokenSchema


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

blockchain = Blockchain()

Token_schema = TokenSchema()
Tokens_schema = TokenSchema(many=True)

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
        return redirect('/pagina_entradas')
    else:
        return redirect('/')

@app.route('/pagina_entradas', methods=['GET'])
def pagina_entradas():
    if 'usuario' in session:
        all_entradas = Entrada.query.all()
        resultado_entradas = Entradas_schema.dump(all_entradas)
        return render_template('pagina_entradas.html', entradas = resultado_entradas, usuario = session['usuario'])
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
def guardar_entrada():
    id_benefactor = request.form['id_benefactor']
    id_categoria = request.form['id_categoria']
    fecha = request.form['fecha']
    cantidad_peso = request.form['cantidad_peso']
    cantidad_unidades = request.form['cantidad_unidades']
    unidad_de_medida = request.form['unidad_de_medida']
    estibas = request.form['estibas']
    ubicacion = request.form['ubicacion']
    bodega = request.form['bodega']
    observaciones = request.form['observaciones']
    
    nueva_donacion = Entrada(id_benefactor, id_categoria, fecha, cantidad_peso, cantidad_unidades, unidad_de_medida, estibas, ubicacion, bodega, observaciones)

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
    estibas = request.form['estibas']
    ubicacion = request.form['ubicacion']
    bodega = request.form['bodega']
    observaciones = request.form['observaciones']

    entrada = Entrada.query.get(id)
    entrada.id_benefactor = id_benefactor
    entrada.id_categoria = id_categoria
    entrada.fecha = fecha
    entrada.cantidad_peso = cantidad_peso
    entrada.cantidad_unidades = cantidad_unidades
    entrada.unidad_de_medida = unidad_de_medida
    entrada.estibas = estibas
    entrada.ubicacion = ubicacion
    entrada.bodega = bodega
    entrada.observaciones = observaciones

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

@app.route('/login', methods =['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = db.session.query(Usuario.id).filter(Usuario.email == email, Usuario.password == password).all()
    resultado = Usuarios_schema.dump(user)

    if len(resultado)>0:
        session['usuario'] = email

        token = generar_token(email, password)
        print('Token: ', token)
        print('Token contenido: ', token['token'])
        token_contenido = token['token']
        nuevo_token = Token(token_contenido)
        db.session.add(nuevo_token)
        db.session.commit()

        return redirect('/pagina_entradas')
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)


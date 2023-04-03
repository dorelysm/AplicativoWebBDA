from flask import Flask, redirect, request, jsonify, json, session, render_template

from config.bd import app, db
from modelos.Benefactores import Benefactor, BenefactorSchema
from modelos.Usuario import Usuario, UsuarioSchema
from modelos.Beneficiarios import Beneficiario, BeneficiarioSchema
from modelos.Categoria import Categoria, CategoriaSchema
from modelos.Entradas import Entrada, EntradaSchema
from modelos.Salidas import Salida, SalidaSchema


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

@app.route('/cerrar')
def cerrar():
    session.pop('usuario',None)
    return redirect('/')

@app.route('/guardar', methods=['POST'] )
def guardar_cultivo():
    id_benefactor = request.form['id_benefactos']
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

@app.route('/eliminar', methods=['GET'] )
def eliminar():
    id = request.args.get('id')
    entradas = Entrada.query.get(id)
    db.session.delete(entradas)
    db.session.commit()
    return Entrada_schema.dump(entradas)
"""
@app.route('/actualizar', methods=['POST'] )
def actualizar():
    id = request.form['id']
    #print('id: ', id)
    N_lote = request.form['N_lote']
    Fruta = request.form['Fruta']
    Existencias = request.form['Existencias']
    cultivo = Cultivo.query.get(id)
    cultivo.N_lote = N_lote
    cultivo.Fruta = Fruta
    cultivo.Existencias = Existencias
    db.session.commit()
    return redirect('/lcultivos')
"""
if __name__ == "__main__":
    app.run(debug=True)

